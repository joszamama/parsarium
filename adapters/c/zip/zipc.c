#include <stdio.h>
#include <string.h>
#include "zipc.h"

static void json_string(const unsigned char *bytes, size_t length) {
    putchar('"');
    for (size_t i = 0; i < length; ++i) {
        unsigned char ch = bytes[i];
        if (ch == '"' || ch == '\\') { putchar('\\'); putchar(ch); }
        else if (ch == '\n') fputs("\\n", stdout);
        else if (ch == '\r') fputs("\\r", stdout);
        else if (ch == '\t') fputs("\\t", stdout);
        else if (ch < 0x20) printf("\\u%04x", ch);
        else putchar(ch);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    zipc_t *archive = zipcOpen(argv[1], "r");
    if (!archive) return 3;
    zipc_file_t *file = zipcOpenFile(archive, "hello.txt");
    if (!file) { zipcClose(archive); return 4; }
    unsigned char content[1024];
    size_t size = 0;
    ssize_t count;
    while (size < sizeof(content) &&
           (count = zipcFileRead(file, content + size, sizeof(content) - size)) > 0)
        size += (size_t)count;
    if (count < 0 || zipcFileFinish(file) < 0 || zipcClose(archive) < 0)
        return 5;
    fputs("{\"content\":", stdout);
    json_string(content, size);
    puts("}");
    return 0;
}
