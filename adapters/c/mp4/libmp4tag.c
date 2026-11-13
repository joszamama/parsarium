#include <libmp4tag.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int error = 0;
    libmp4tag_t *file = mp4tag_open(argv[1], &error);
    if (file == NULL) return 1;
    if (mp4tag_parse(file) != MP4TAG_OK) {
        mp4tag_free(file);
        return 1;
    }
    mp4tagpub_t title = {0};
    if (mp4tag_get_tag_by_name(file, "\xC2\xA9nam", &title) != MP4TAG_OK ||
        title.data == NULL || strcmp(title.data, "Parsarium") != 0) {
        mp4tag_free(file);
        return 1;
    }
    printf("{\"title\":\"%s\",\"duration_ms\":%lld}\n",
           title.data, (long long)mp4tag_duration(file));
    mp4tag_free(file);
    return 0;
}
