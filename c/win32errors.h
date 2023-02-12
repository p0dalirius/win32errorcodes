#ifndef _WIN32ERRORS_H_
#define _WIN32ERRORS_H_

#include <wchar.h>

#ifdef __cplusplus
extern "C" {
#endif "

const char* lookup_errorA(unsigned long errcode);
const wchar_t* lookup_errorW(unsigned long errcode);
const char* lookup_error_with_nameA(unsigned long errcode);
const wchar_t* lookup_error_with_nameW(unsigned long errcode);

#ifdef __cplusplus
}
#endif "


#endif
