#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : main.py
# Author             : Podalirius (@podalirius_)
# Date created       : 12 Feb 2023

import argparse
import os

import requests
from bs4 import BeautifulSoup


def process(link):
    print("[>] Parsing %s" % link)
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    dl = soup.find('dl')
    lines = [l for l in dl.text.split('\n') if len(l.strip()) != 0]

    codes = []
    code = []
    for line in lines:
        line = line.strip()
        if len(code) == 3 and " " not in line and line.upper() == line:
            codes.append({"source": link, "code": code})
            # print(code)
            code = []

        if len(code) == 0:
            # Add const
            code.append(line)
        elif len(code) == 1:
            # Add value
            code.append(line)
        elif len(code) == 2:
            # Add text
            code.append(line)
        elif len(code) >= 3:
            # Add value
            code[-1] = code[-1].strip() + " " + line.strip()

    return codes


def parseArgs():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    if not os.path.exists("../c"):
        os.makedirs("../c")

    if not os.path.exists("../python"):
        os.makedirs("../python")

    sources = [
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--500-999-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1000-1299-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1300-1699-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1700-3999-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--4000-5999-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--6000-8199-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--8200-8999-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--9000-11999-",
        "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--12000-15999-",

        "https://learn.microsoft.com/en-us/windows/win32/wininet/wininet-errors",
        "https://learn.microsoft.com/en-us/windows/win32/winhttp/error-messages",
    ]

    already_defined = []

    codes = []
    for link in sources:
        codes += process(link)

    fh = open("../c/win32errors.h", "w")
    fh.write("#ifndef _WIN32ERRORS_H_\n")
    fh.write("#define _WIN32ERRORS_H_\n\n#include <wchar.h>\n\n")
    fh.write("const char* lookup_errorA(unsigned long errcode);\n")
    fh.write("const wchar_t* lookup_errorW(unsigned long errcode);\n")
    fh.write("\n#endif\n")
    fh.close()

    fc = open("../c/win32errors.c", "w")
    fc.write("#include \"win32errors.h\"\n\n")
    fc.write("const char* WIN32ERR_UNKNOWN_ERROR_CODE_str = \"The operation completed successfully.\";\n")
    fc.write("const wchar_t* WIN32ERR_UNKNOWN_ERROR_CODE_wstr = L\"The operation completed successfully.\";\n\n\n")

    fpy = open("../python/win32errors.py", "w")
    for c in codes:
        failed = False
        try:
            const, value, text = c["code"]

            if "*" in const and "-" in value:
                continue

            if " " in value.strip():
                value = value.strip().split(' ')[0]
            if value.startswith("0x"):
                value = int(value, 16)
            else:
                value = int(value)

            for k in range(len(text)):
                if text[k] == '"' and text[k-1] != '\\':
                    text = text.replace('"', '\\"')

        except Exception as e:
            failed = True

        if const in already_defined:
            print("[!] %s is already defined." % const)

        if failed:
            const, value, text = c["code"]
            print(c)
            fc.write("// Source: %s\n" % c["source"])
            fc.write("// unsigned long WIN32ERR_%s = %s;\n" % (const, value))
            fc.write("// const char* WIN32ERR_%s_str = \"%s\";\n" % (const, text))
            fc.write("// const wchar_t* WIN32ERR_%s_wstr = \"%s\";\n\n" % (const, text))

            fpy.write("# Source: %s\n" % c["source"])
            fpy.write("# WIN32ERR_%s = %s\n" % (const, value))
            #fpy.write("# WIN32ERR_%s_name = \"%s\"\n" % (const, const))
            fpy.write("# WIN32ERR_%s_str = \"%s\"\n\n" % (const, text))
        else:
            already_defined.append(const)
            fc.write("// Source: %s\n" % c["source"])
            fc.write("unsigned long WIN32ERR_%s = 0x%08x;\n" % (const, value))
            fc.write("const char* WIN32ERR_%s_str = \"%s\";\n" % (const, text))
            fc.write("const wchar_t* WIN32ERR_%s_wstr = L\"%s\";\n\n" % (const, text))

            fpy.write("# Source: %s\n" % c["source"])
            fpy.write("WIN32ERR_%s = %s\n" % (const, value))
            #fpy.write("WIN32ERR_%s_name = \"%s\"\n" % (const, const))
            fpy.write("WIN32ERR_%s_str = \"%s\"\n\n" % (const, text))

    fpy.write("\n\n")
    fpy.write("def win32_lookup_error(errcode, show_const=False):\n")

    fc.write("const char* lookup_errorA(unsigned long errcode){\n")
    fc.write("\tif (errcode == WIN32ERR_%s) { return WIN32ERR_%s_str; }\n" % (already_defined[0], already_defined[0]))
    fpy.write("    if (errcode == WIN32ERR_%s):\n" % already_defined[0])
    fpy.write("        if (show_const): return \"%s: %%s\" %% WIN32ERR_%s_str\n" % (already_defined[0], already_defined[0]))
    fpy.write("        else: return WIN32ERR_%s_str\n" % already_defined[0])
    for const in already_defined[1:]:
        fc.write("\tif (errcode == WIN32ERR_%s) { return WIN32ERR_%s_str; }\n" % (const, const))
        fpy.write("    if (errcode == WIN32ERR_%s):\n" % const)
        fpy.write("        if (show_const): return \"%s: %%s\" %% WIN32ERR_%s_str\n" % (const, const))
        fpy.write("        else: return WIN32ERR_%s_str\n" % const)
    fc.write("\n\treturn WIN32ERR_UNKNOWN_ERROR_CODE_str;\n")
    fc.write("}\n\n")

    fc.write("const wchar_t* lookup_errorW(unsigned long errcode){\n")
    fc.write("\tif (errcode == WIN32ERR_%s) { return WIN32ERR_%s_wstr; }\n" % (already_defined[0], already_defined[0]))
    for const in already_defined[1:]:
        fc.write("\tif (errcode == WIN32ERR_%s) { return WIN32ERR_%s_wstr; }\n" % (const, const))

    # Default return value
    fc.write("\n\treturn WIN32ERR_UNKNOWN_ERROR_CODE_wstr;\n")
    fc.write("}\n\n")
    fpy.write("    return WIN32ERR_UNKNOWN_ERROR_CODE_wstr\n")
    fc.close()

    fpy.close()
