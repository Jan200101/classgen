#include <cstdio>
#include <cstdint>

#include "class.hpp"

int main()
{
	ConCommandBase b;

	uintptr_t offset = (uintptr_t)(&b.m_pszName) - (uintptr_t)(&b);
	printf("m_pszName offset: %li\n", offset);
}