#ifndef _WIN32ERRORS_H_
#define _WIN32ERRORS_H_

#include <wchar.h>

const char* lookup_errorA(unsigned long errcode);
const wchar_t* lookup_errorW(unsigned long errcode);

#endif
