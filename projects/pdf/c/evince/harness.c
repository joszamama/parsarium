#define _GNU_SOURCE
#include "harness.h"
#include <evince-document.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>

static int ensure_evince(void) {
    static int initialized;
    if (!initialized) {
        if (!ev_init()) return 0;
        initialized = 1;
    }
    return 1;
}

int parsarium_parse_pdf_file(const char *path, int *pages) {
    if (!path || !pages) return 0;
    if (!ensure_evince()) return 0;
    GFile *file = g_file_new_for_path(path);
    GError *error = NULL;
    EvDocument *document = ev_document_factory_get_document_for_gfile(
        file, EV_DOCUMENT_LOAD_FLAG_NONE, NULL, &error);
    g_object_unref(file);
    if (!document) {
        g_clear_error(&error);
        return 0;
    }
    *pages = ev_document_get_n_pages(document);
    g_object_unref(document);
    g_clear_error(&error);
    return *pages > 0;
}

static int parsarium_parse_pdf_fd(int fd, int *pages) {
    if (!ensure_evince()) { close(fd); return 0; }
    GError *error = NULL;
    /* The factory consumes fd on success and failure. Its PDF backend calls
       Poppler's local-fd parser, without creating a SyncTeX sidecar scanner. */
    EvDocument *document = ev_document_factory_get_document_for_fd(
        fd, "application/pdf", EV_DOCUMENT_LOAD_FLAG_NONE, NULL, &error);
    if (!document) {
        g_clear_error(&error);
        return 0;
    }
    *pages = ev_document_get_n_pages(document);
    g_object_unref(document);
    g_clear_error(&error);
    return *pages > 0;
}

int parsarium_parse_pdf_bytes(const uint8_t *data, size_t size, int *pages) {
    if (!data || !pages || size == 0 || size > (1u << 20)) return 0;
    char path[] = "/tmp/parsarium-evince-XXXXXX.pdf";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(fd, data + written, size - written);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) { close(fd); unlink(path); return 0; }
        written += (size_t)n;
    }
    if (lseek(fd, 0, SEEK_SET) < 0) { close(fd); unlink(path); return 0; }
    int ok = parsarium_parse_pdf_fd(fd, pages);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    int pages = 0;
    (void)parsarium_parse_pdf_bytes(data, size, &pages);
    return 0;
}
