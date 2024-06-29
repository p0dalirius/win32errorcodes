#include <iostream>
#include <windows.h>

#include "../../win32errors.h"


int main()
{
    unsigned long errcode = 0x00003cfd;

    // https://stackoverflow.com/a/17386923
    wchar_t buf[4096];
    FormatMessageW(
        FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, // dwFlags
        NULL,                                                       // lpSource
        errcode,                                                    // dwMessageId
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),                  // dwLanguageId
        buf,                                                        // lpBuffer
        (sizeof(buf) / sizeof(wchar_t)),                            // nSize
        NULL                                                        // *Arguments
    );
    wprintf(L"[+] With builtin FormatMessageW():\r\n");
    wprintf(L"%s\r\n\n", buf);

    // Win32ErrorCodes
    wprintf(L"[+] With Win32ErrorCodes library:\r\n");
    wprintf(L"%s\r\n", lookup_errorW(errcode));
}
