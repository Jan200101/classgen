#include <stdio.h>
#include <stdint.h>

#include "class.h"

int main()
{
	ConCommandBase b;

	uintptr_t offset = (uintptr_t)(&b.m_pszName) - (uintptr_t)(&b);
	printf("m_pszName offset: %li\n", offset);
}