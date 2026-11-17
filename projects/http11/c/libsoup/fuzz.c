#include "harness.h"

#include <glib.h>

static GLogWriterOutput discard_log(GLogLevelFlags level, const GLogField *fields,
                                    gsize n_fields, gpointer user_data) {
    (void)level; (void)fields; (void)n_fields; (void)user_data;
    return G_LOG_WRITER_HANDLED;
}

int LLVMFuzzerInitialize(int *argc, char ***argv) {
    (void)argc; (void)argv;
    g_log_set_writer_func(discard_log, NULL, NULL);
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_result result;
    if (parsarium_parse_http(data, size, &result)) parsarium_http_result_clear(&result);
    return 0;
}
