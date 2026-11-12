#include <physfs.h>
#include "report.h"
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2 || !PHYSFS_init(argv[0])) return 2;
    if (!PHYSFS_mount(argv[1], NULL, 1)) return 1;
    char **names = PHYSFS_enumerateFiles("/");
    if (!names || !names[0]) return 1;
    size_t count = 0;
    while (names[count]) count++;
    PHYSFS_File *file = PHYSFS_openRead(names[0]);
    if (!file) return 1;
    const PHYSFS_sint64 length = PHYSFS_fileLength(file);
    if (length < 0) return 1;
    unsigned char *content = (unsigned char *)malloc((size_t)length + 1);
    if (!content) return 1;
    if (PHYSFS_readBytes(file, content, (PHYSFS_uint64)length) != length) return 1;
    zip_report(count, names[0], content, (size_t)length);
    free(content);
    PHYSFS_close(file);
    PHYSFS_freeList(names);
    PHYSFS_deinit();
    return 0;
}
