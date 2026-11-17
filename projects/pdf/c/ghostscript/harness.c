#include "harness.h"
#include "iapi.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* Fixed program: only the local temporary file is opened, by the PDF interpreter. */
static const char program_format[] =
    "<</QUIET true>> .PDFInit /parsarium_pdf exch def "
    "mark { (%s) parsarium_pdf .PDFFile "
    "parsarium_pdf .PDFInfo /NumPages get (PARSARIUM_PAGES=) print == } stopped "
    "cleartomark parsarium_pdf .PDFClose flush";

typedef struct Capture { char bytes[4096]; size_t length; } Capture;

static int capture_stdout(void *handle, const char *bytes, int length) {
    Capture *capture = handle;
    if (length <= 0) return length;
    size_t room = sizeof(capture->bytes) - 1 - capture->length;
    size_t n = (size_t)length < room ? (size_t)length : room;
    memcpy(capture->bytes + capture->length, bytes, n);
    capture->length += n;
    capture->bytes[capture->length] = '\0';
    return length;
}

static int discard_stderr(void *handle, const char *bytes, int length) {
    (void)handle; (void)bytes;
    return length;
}

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (8u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.pdf";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    char program[sizeof(program_format) + sizeof(path)];
    snprintf(program, sizeof(program), program_format, path);
    Capture capture = {{0}, 0};
    void *instance = NULL;
    int ok = 0;
    if (gsapi_new_instance(&instance, &capture) < 0) { unlink(path); return 0; }
    char *arguments[] = {"parsarium", "-q", "-dNODISPLAY", "-dSAFER"};
    if (gsapi_set_stdio(instance, NULL, capture_stdout, discard_stderr) == 0
        && gsapi_add_control_path(instance, GS_PERMIT_FILE_READING, path) == 0
        && gsapi_init_with_args(instance, 4, arguments) == 0) {
        int exit_code = 0;
        int status = gsapi_run_string(instance, program, 0, &exit_code);
        const char *marker = strstr(capture.bytes, "PARSARIUM_PAGES=");
        if (status == 0 && marker) {
            char *end = NULL;
            long pages = strtol(marker + strlen("PARSARIUM_PAGES="), &end, 10);
            if (end != marker + strlen("PARSARIUM_PAGES=") && *end == '\n' && pages >= 0 && pages <= 0x7fffffff) {
                result->pages = (int)pages;
                ok = 1;
            }
        }
    }
    gsapi_exit(instance);
    gsapi_delete_instance(instance);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
