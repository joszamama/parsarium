#include <tag_c.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    TagLib_File *file = taglib_file_new(argv[1]);
    if (file == NULL || !taglib_file_is_valid(file)) {
        if (file != NULL) taglib_file_free(file);
        return 1;
    }
    TagLib_Tag *tag = taglib_file_tag(file);
    const TagLib_AudioProperties *properties = taglib_file_audioproperties(file);
    if (tag == NULL || properties == NULL) {
        taglib_file_free(file);
        return 1;
    }
    char *title = taglib_tag_title(tag);
    int seconds = taglib_audioproperties_length(properties);
    printf("{\"title\":\"%s\",\"duration_seconds\":%d}\n", title, seconds);
    taglib_tag_free_strings();
    taglib_file_free(file);
    return 0;
}
