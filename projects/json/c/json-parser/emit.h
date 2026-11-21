/* Minimal JSON text emitter for printing a parser's value tree in the replay.
 * Integers print as integers; doubles always carry '.' or 'e', or are Infinity/NaN,
 * so the Python oracle can check integer versus float kinds and key order. */
#ifndef PARSARIUM_EMIT_H
#define PARSARIUM_EMIT_H
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void emit_string(FILE *out, const char *text, size_t length) {
    fputc('"', out);
    for (size_t i = 0; i < length; i++) {
        unsigned char c = (unsigned char)text[i];
        if (c == '"' || c == '\\') { fputc('\\', out); fputc(c, out); }
        else if (c < 0x20) fprintf(out, "\\u%04x", c);
        else fputc(c, out);
    }
    fputc('"', out);
}

static void emit_int(FILE *out, int64_t value) { fprintf(out, "%lld", (long long)value); }

static void emit_double(FILE *out, double value) {
    char text[64];
    /* Non-finite values (an out-of-range exponent the parser turned into
     * infinity) print as JavaScript-style Infinity/NaN tokens, which the
     * observer's JSON reader accepts, so the field stays a number. */
    if (isnan(value)) { fputs("NaN", out); return; }
    if (isinf(value)) { fputs(value > 0 ? "Infinity" : "-Infinity", out); return; }
    snprintf(text, sizeof text, "%.17g", value);
    if (!strpbrk(text, ".eEni")) strcat(text, ".0");
    fputs(text, out);
}
#endif
