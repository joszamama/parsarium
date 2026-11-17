#define _GNU_SOURCE
#include "harness.h"
#include <gio/gio.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>

/* These signatures mirror the pinned Papers 51.1 public headers. Its umbrella
 * header requires an author-contact macro that this independent harness
 * cannot truthfully define. */
typedef struct _PpsDocument PpsDocument;
gboolean pps_init(void);
void pps_shutdown(void);
PpsDocument *pps_document_factory_get_document(const char *uri, GError **error);
gboolean pps_document_load(PpsDocument *document, const char *uri, GError **error);
gint pps_document_get_n_pages(PpsDocument *document);

int parsarium_parse_pdf_file(const char *path, int *pages) {
    if (!path || !pages) return 0;
    static int initialized;
    if (!initialized) {
        if (!pps_init()) return 0;
        initialized = 1;
    }
    GError *error = NULL;
    char *uri = g_filename_to_uri(path, NULL, &error);
    if (!uri) { g_clear_error(&error); return 0; }
    PpsDocument *document = pps_document_factory_get_document(uri, &error);
    if (!document) { g_clear_error(&error); g_free(uri); return 0; }
    int ok = pps_document_load(document, uri, &error);
    if (ok) *pages = pps_document_get_n_pages(document);
    g_clear_error(&error);
    g_object_unref(document);
    g_free(uri);
    return ok && *pages > 0;
}

int parsarium_parse_pdf_bytes(const uint8_t *data, size_t size, int *pages) {
    if (!data || !pages || size == 0 || size > (1u << 20)) return 0;
    char path[] = "/tmp/parsarium-papers-XXXXXX.pdf";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(fd, data + written, size - written);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) { close(fd); unlink(path); return 0; }
        written += (size_t)n;
    }
    if (close(fd) != 0) { unlink(path); return 0; }
    int ok = parsarium_parse_pdf_file(path, pages);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    int pages = 0;
    (void)parsarium_parse_pdf_bytes(data, size, &pages);
    return 0;
}
