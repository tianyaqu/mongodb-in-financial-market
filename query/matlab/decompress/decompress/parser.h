#include "tick.h"

extern "C" int parse_string(const char* market,const char* content,struct Tick** result, unsigned* len);
extern "C" void m_FreeMem(void* ptr);

