#include "LzmaLib.h"
#include "decompress.h"
#include "tick.h"

#include <stdlib.h>
#include <stdio.h>
#pragma warning( disable : 4996)

extern void m_FreeMem(void* ptr);
extern int parse_string(const char* market, const char* content, struct Tick** result, unsigned* len);


EXPORT int decompress(const char* market,unsigned char *compressed, struct TickData** buffer, unsigned int* out_len)
{
    unsigned char* content = (unsigned char*)(malloc(12*1024*1024));

    const char*ptr = (char*)compressed;

    char props[5] = { 0 };
    memcpy(props, ptr, 5);
    unsigned char*xprops = (unsigned char*)props;

    unsigned long long compress_len = 0;
    memcpy(&compress_len, ptr + 5, 8);
    SizeT xcompress_len = compress_len;
    const unsigned char* compress_ptr = (const unsigned char*)(ptr + 13);

    memset(content, 0, 12 * 1024 * 1024);
    size_t co_len = 12 * 1024 * 1024;

    int ret = LzmaUncompress(content, &co_len, compress_ptr, &xcompress_len, xprops, 5);

    ret = parse_string(market,content, (struct Tick**)buffer,out_len);
    
    free(content);

    return ret;
}

EXPORT void free_mem(void* ptr)
{
    m_FreeMem(ptr);
}


//test method,change the project to an application to use
int main()
{
    //bin.rar is in project dir
    FILE* fp1 = fopen("bin.rar", "rb");

    char* compressed = malloc(1024 * 1024);
    int len = 1024 * 1024;
    fread(compressed,sizeof(char),len,fp1);
    fclose(fp1);
    char* data = 0;
    unsigned out_len = 0;

    struct TickData* buffer = 0;
    decompress("CFFEX", compressed, &buffer,&out_len);
    free(compressed);

    for (int i = 0; i < out_len; i++)
    {
        struct TickData*ptr = buffer+i;
        //printf()
    }

    free_mem(buffer);

}