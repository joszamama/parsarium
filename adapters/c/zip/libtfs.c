#include <tebako/fs/c_api.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2 || tebako_fs_init_from_file(argv[1], "/zip") != 0) return 2;
    tebako_dir_t directory = tebako_fs_opendir("/zip");
    if (!directory) return 3;
    char first_name[256] = {0};
    size_t entries = 0;
    struct tebako_c_dirent *entry;
    while ((entry = tebako_fs_readdir(directory)) != NULL) {
        if (entries == 0) memcpy(first_name, entry->d_name, sizeof first_name);
        entries++;
    }
    tebako_fs_closedir(directory);
    if (!entries) return 4;

    char path[sizeof first_name + 6];
    if (snprintf(path, sizeof path, "/zip/%s", first_name) >= sizeof path) return 5;
    int fd = tebako_fs_open(path, O_RDONLY);
    if (fd < 0) return 6;
    unsigned char content[256];
    ssize_t length = tebako_fs_read(fd, content, sizeof content);
    if (length < 0 || length == sizeof content) return 7;
    if (tebako_fs_read(fd, content + length, 1) != 0) return 8;
    zip_report(entries, first_name, content, (size_t)length);
    tebako_fs_close(fd);
    tebako_fs_unmount();
    return 0;
}
