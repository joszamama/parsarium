#include "harness.h"

#include <glib.h>

static GLogWriterOutput discard_log(GLogLevelFlags, const GLogField *, gsize, gpointer) {
    return G_LOG_WRITER_HANDLED;
}

extern "C" int LLVMFuzzerInitialize(int *, char ***) {
    g_log_set_writer_func(discard_log, nullptr, nullptr);
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    ParsariumHttpResult result{};
    parsarium_parse_http(data, size, &result);
    return 0;
}
