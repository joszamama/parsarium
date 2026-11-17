#define _GNU_SOURCE
#include "harness.h"
#include <atril-document.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>

/* Atril's URI factory retains a GLib MIME string on a valid PDF. Keep
   AddressSanitizer and UndefinedBehaviorSanitizer active, but disable leak
   detection for this known upstream process-lifetime allocation. */
const char *__asan_default_options(void) { return "detect_leaks=0"; }

/* Atril's libtool link embeds Clang's profile runtime in the PDF backend.
   Ubuntu's libc exports __cxa_atexit but not atexit to dlopened modules.
   Export this registration bridge from the replay/fuzz executable so the
   backend can flush its own source profile at process exit. */
extern int __cxa_atexit(void (*)(void *), void *, void *);
struct exit_callback { void (*function)(void); };
static void invoke_exit_callback(void *context) {
    struct exit_callback *callback = context;
    callback->function();
    free(callback);
}
int atexit(void (*function)(void)) {
    struct exit_callback *callback = malloc(sizeof(*callback));
    if (!callback) return -1;
    callback->function = function;
    int rc = __cxa_atexit(invoke_exit_callback, callback, NULL);
    if (rc) free(callback);
    return rc;
}

int parsarium_parse_pdf_file(const char *path, int *pages) {
    if (!path || !pages) return 0;
    static int initialized;
    if (!initialized) {
        if (!ev_init()) return 0;
        initialized = 1;
    }
    /* Atril 1.28.2's factory takes a URI; the local GFile supplies it. */
    GFile *file = g_file_new_for_path(path);
    char *uri = g_file_get_uri(file);
    g_object_unref(file);
    GError *error = NULL;
    EvDocument *document = ev_document_factory_get_document(uri, &error);
    g_free(uri);
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
    char path[] = "/tmp/parsarium-atril-XXXXXX.pdf";
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
