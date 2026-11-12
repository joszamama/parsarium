#include <lowzip.h>
#include "report.h"
#include <limits.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    unsigned char *bytes;
    unsigned int length;
} input_bytes;

static unsigned int read_byte(void *opaque, unsigned int offset) {
    const input_bytes *input = (const input_bytes *) opaque;
    return offset < input->length ? input->bytes[offset] : 0x100U;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file || fseek(file, 0, SEEK_END) != 0) return 1;
    const long length = ftell(file);
    if (length < 0 || (unsigned long) length > UINT_MAX || fseek(file, 0, SEEK_SET) != 0) return 1;
    input_bytes input = {(unsigned char *) malloc((size_t) length + 1), (unsigned int) length};
    if (!input.bytes || fread(input.bytes, 1, (size_t) length, file) != (size_t) length) return 1;
    fclose(file);

    lowzip_state state = {0};
    state.udata = &input;
    state.read_callback = read_byte;
    state.zip_length = input.length;
    lowzip_init_archive(&state);
    if (state.have_error) return 1;
    size_t count = 0;
    while (lowzip_locate_file(&state, (int) count, NULL)) count++;
    if (count == 0) return 1;
    lowzip_file *entry = lowzip_locate_file(&state, 0, NULL);
    if (!entry || state.have_error) return 1;
    char name[sizeof(entry->filename)];
    memcpy(name, entry->filename, sizeof(name));
    const size_t output_length = entry->uncompressed_size;
    unsigned char *output = (unsigned char *) malloc(output_length + 1);
    if (!output) return 1;
    state.output_start = output;
    state.output_end = output + output_length;
    state.output_next = output;
    lowzip_get_data(&state);
    if (state.have_error || state.output_next != state.output_end) return 1;
    zip_report(count, name, output, output_length);
    free(output);
    free(input.bytes);
    return 0;
}
