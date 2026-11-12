#include <ghostscript/iapi.h>

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct capture {
    char bytes[256];
    size_t length;
};

static int append_output(void *handle, const char *bytes, int length) {
    struct capture *output = handle;
    if (length < 0 || output->length + (size_t)length >= sizeof output->bytes) return -1;
    memcpy(output->bytes + output->length, bytes, (size_t)length);
    output->length += (size_t)length;
    output->bytes[output->length] = '\0';
    return length;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    size_t length = strlen(argv[1]);
    if (length > (SIZE_MAX - 128) / 2) return 2;
    char *program = malloc(2 * length + 128);
    if (program == NULL) return 3;
    const char *prefix = "<<>> .PDFInit dup (";
    const char *suffix = ") exch .PDFFile dup .PDFInfo /NumPages get == .PDFClose";
    size_t used = strlen(prefix);
    memcpy(program, prefix, used);
    for (const char *p = argv[1]; *p; ++p) {
        if (*p == '(' || *p == ')' || *p == '\\') program[used++] = '\\';
        program[used++] = *p;
    }
    strcpy(program + used, suffix);

    struct capture output = {{0}, 0};
    void *instance = NULL;
    if (gsapi_new_instance(&instance, &output) != 0) return 4;
    if (gsapi_set_stdio(instance, NULL, append_output, append_output) != 0) return 5;
    if (gsapi_add_control_path(instance, GS_PERMIT_FILE_READING, argv[1]) != 0) return 6;
    char *arguments[] = {"gs", "-q", "-dNODISPLAY"};
    if (gsapi_init_with_args(instance, 3, arguments) != 0) return 7;
    int exit_code = 0;
    int status = gsapi_run_string(instance, program, 0, &exit_code);
    free(program);
    int shutdown = gsapi_exit(instance);
    gsapi_delete_instance(instance);
    if (status != 0 || exit_code != 0 || shutdown != 0) return 8;
    char *end = NULL;
    long pages = strtol(output.bytes, &end, 10);
    if (pages <= 0 || end == output.bytes) return 9;
    printf("{\"pages\":%ld}\n", pages);
    return 0;
}
