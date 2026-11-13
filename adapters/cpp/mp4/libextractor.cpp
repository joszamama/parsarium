#include <extractor.h>
#include <cstdio>
#include <cstring>

struct Result {
    int mp4;
    int seconds;
    int width;
    int height;
    char title[64];
};

static int collect(void *context, const char *plugin, EXTRACTOR_MetaType type,
                   EXTRACTOR_MetaFormat format, const char *mime,
                   const char *data, size_t length) {
    (void)mime;
    if (std::strcmp(plugin, "qt") != 0 || format != EXTRACTOR_METAFORMAT_UTF8) return 0;
    auto *result = static_cast<Result *>(context);
    char value[128];
    size_t count = length < sizeof(value) - 1 ? length : sizeof(value) - 1;
    std::memcpy(value, data, count);
    value[count] = '\0';
    if (type == EXTRACTOR_METATYPE_MIMETYPE) result->mp4 = std::strcmp(value, "video/mp4") == 0;
    if (type == EXTRACTOR_METATYPE_DURATION) std::sscanf(value, "%ds", &result->seconds);
    if (type == EXTRACTOR_METATYPE_IMAGE_DIMENSIONS)
        std::sscanf(value, "%dx%d", &result->width, &result->height);
    if (type == EXTRACTOR_METATYPE_TITLE) std::snprintf(result->title, sizeof(result->title), "%s", value);
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    EXTRACTOR_PluginList *plugin = EXTRACTOR_plugin_add(
        nullptr, "qt", nullptr, EXTRACTOR_OPTION_DEFAULT_POLICY);
    if (plugin == nullptr) return 1;
    Result result = {};
    EXTRACTOR_extract(plugin, argv[1], nullptr, 0, collect, &result);
    EXTRACTOR_plugin_remove_all(plugin);
    if (!result.mp4 || result.seconds < 1 || result.width < 1 || result.height < 1 || !result.title[0]) return 1;
    std::printf("{\"title\":\"%s\",\"duration_seconds\":%d,\"width\":%d,\"height\":%d}\n",
                result.title, result.seconds, result.width, result.height);
    return 0;
}
