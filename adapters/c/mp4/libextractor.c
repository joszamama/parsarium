#include <extractor.h>
#include <stdio.h>
#include <string.h>

struct result {
    int mp4;
    int seconds;
    int width;
    int height;
    char title[64];
};

static int collect(void *context, const char *plugin, enum EXTRACTOR_MetaType type,
                   enum EXTRACTOR_MetaFormat format, const char *mime,
                   const char *data, size_t length) {
    (void)mime;
    if (strcmp(plugin, "qt") != 0 || format != EXTRACTOR_METAFORMAT_UTF8) return 0;
    struct result *result = context;
    char value[128];
    size_t count = length < sizeof(value) - 1 ? length : sizeof(value) - 1;
    memcpy(value, data, count);
    value[count] = '\0';
    if (type == EXTRACTOR_METATYPE_MIMETYPE) result->mp4 = strcmp(value, "video/mp4") == 0;
    if (type == EXTRACTOR_METATYPE_DURATION) sscanf(value, "%ds", &result->seconds);
    if (type == EXTRACTOR_METATYPE_IMAGE_DIMENSIONS)
        sscanf(value, "%dx%d", &result->width, &result->height);
    if (type == EXTRACTOR_METATYPE_TITLE) snprintf(result->title, sizeof(result->title), "%s", value);
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct EXTRACTOR_PluginList *plugin = EXTRACTOR_plugin_add(
        NULL, "qt", NULL, EXTRACTOR_OPTION_DEFAULT_POLICY);
    if (plugin == NULL) return 1;
    struct result result = {0};
    EXTRACTOR_extract(plugin, argv[1], NULL, 0, collect, &result);
    EXTRACTOR_plugin_remove_all(plugin);
    if (!result.mp4 || result.seconds < 1 || result.width < 1 || result.height < 1 || !result.title[0]) return 1;
    printf("{\"title\":\"%s\",\"duration_seconds\":%d,\"width\":%d,\"height\":%d}\n",
           result.title, result.seconds, result.width, result.height);
    return 0;
}
