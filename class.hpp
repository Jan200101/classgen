#include <stdbool.h>

class IConCommandBaseAccessor;
class ConCommandBase;

// From r5reloaded
class ConCommandBase
{
public:
	bool HasFlags(int nFlags);
	void AddFlags(int nFlags);
	void RemoveFlags(int nFlags);

	bool IsCommand(void) const;
	bool IsRegistered(void) const;
	bool IsFlagSet(int nFlags) const;
	static bool IsFlagSet(ConCommandBase* pCommandBase, int nFlags); // For hooking to engine's implementation.

	int GetFlags(void) const;
	ConCommandBase* GetNext(void) const;
	const char* GetHelpText(void) const;

	char* CopyString(const char* szFrom) const;

	void* m_pConCommandBaseVTable; // 0x0000
	ConCommandBase* m_pNext; // 0x0008
	bool m_bRegistered; // 0x0010
	char pad_0011[7]; // 0x0011 <- 3 bytes padding + unk int32.
	const char* m_pszName; // 0x0018
	const char* m_pszHelpString; // 0x0020
	int m_nFlags; // 0x0028
	ConCommandBase* s_pConCommandBases; // 0x002C
	IConCommandBaseAccessor* s_pAccessor; // 0x0034
}; // Size: 0x0040
