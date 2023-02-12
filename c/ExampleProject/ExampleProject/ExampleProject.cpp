#include <iostream>

extern "C" {
#include "../../win32errors.h"
}

int main()
{
    wprintf(lookup_errorW(0));
}
