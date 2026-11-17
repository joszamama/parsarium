/* Typed-tree JSON emitter shared by the C YAML harnesses.
 *
 * The parser supplies structure, decoded scalar text, the scalar style and
 * expanded aliases. Typing plain scalars is adapter-side: plain scalars are
 * resolved with the YAML 1.2 core-schema patterns (null, bool, int, float,
 * otherwise str); every quoted or block scalar is a str. The Parsarium YAML
 * controls only use plain scalars that type the same under YAML 1.1 and 1.2.
 *
 * Output encoding: ["map", [[key, node], ...]], ["seq", [...]], ["str", s],
 * ["int", decimal], ["float", shortest round-trip decimal], ["bool", b],
 * ["null"]. */
#ifndef PARSARIUM_YAML_TYPED_H
#define PARSARIUM_YAML_TYPED_H
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void typed_string(FILE *out, const char *text, size_t length) {
    fputc('"', out);
    for (size_t i = 0; i < length; i++) {
        unsigned char c = (unsigned char)text[i];
        if (c == '"' || c == '\\') { fputc('\\', out); fputc(c, out); }
        else if (c < 0x20) fprintf(out, "\\u%04x", c);
        else fputc(c, out);
    }
    fputc('"', out);
}

static int typed_equals(const char *text, size_t length, const char *word) {
    return strlen(word) == length && memcmp(text, word, length) == 0;
}

static int typed_digits(const char *text, size_t start, size_t end, const char *set) {
    if (start >= end) return 0;
    for (size_t i = start; i < end; i++)
        if (!strchr(set, text[i])) return 0;
    return 1;
}

/* YAML 1.2 core schema float: [-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)? */
static int typed_is_float(const char *t, size_t n) {
    size_t i = 0, digits = 0;
    if (i < n && (t[i] == '-' || t[i] == '+')) i++;
    while (i < n && t[i] >= '0' && t[i] <= '9') { i++; digits++; }
    if (i < n && t[i] == '.') {
        i++;
        while (i < n && t[i] >= '0' && t[i] <= '9') { i++; digits++; }
    }
    if (!digits) return 0;
    if (i < n && (t[i] == 'e' || t[i] == 'E')) {
        size_t exp = 0;
        i++;
        if (i < n && (t[i] == '-' || t[i] == '+')) i++;
        while (i < n && t[i] >= '0' && t[i] <= '9') { i++; exp++; }
        if (!exp) return 0;
    }
    return i == n;
}

static void typed_double(FILE *out, double value) {
    char text[64];
    for (int precision = 1; precision <= 17; precision++) {
        snprintf(text, sizeof text, "%.*g", precision, value);
        if (strtod(text, NULL) == value) break;
    }
    if (!strpbrk(text, ".eEni")) strcat(text, ".0");
    fputs(text, out);
}

/* Returns 0 on success, -1 if the scalar text cannot be typed. */
static int typed_scalar(FILE *out, const char *t, size_t n, int plain) {
    char buffer[128];
    if (!plain) { fputs("[\"str\",", out); typed_string(out, t, n); fputc(']', out); return 0; }
    if (n == 0 || typed_equals(t, n, "~") || typed_equals(t, n, "null") ||
            typed_equals(t, n, "Null") || typed_equals(t, n, "NULL")) {
        fputs("[\"null\"]", out); return 0;
    }
    if (typed_equals(t, n, "true") || typed_equals(t, n, "True") || typed_equals(t, n, "TRUE")) {
        fputs("[\"bool\",true]", out); return 0;
    }
    if (typed_equals(t, n, "false") || typed_equals(t, n, "False") || typed_equals(t, n, "FALSE")) {
        fputs("[\"bool\",false]", out); return 0;
    }
    if (n < sizeof buffer) {
        size_t sign = (t[0] == '-' || t[0] == '+');
        int base = 0;
        size_t start = 0;
        if (typed_digits(t, sign, n, "0123456789")) { base = 10; start = 0; }
        else if (n > 2 && t[0] == '0' && t[1] == 'o' && typed_digits(t, 2, n, "01234567")) { base = 8; start = 2; }
        else if (n > 2 && t[0] == '0' && t[1] == 'x' && typed_digits(t, 2, n, "0123456789abcdefABCDEF")) { base = 16; start = 2; }
        if (base) {
            memcpy(buffer, t + start, n - start);
            buffer[n - start] = 0;
            errno = 0;
            long long value = strtoll(buffer, NULL, base);
            if (errno) return -1;
            fprintf(out, "[\"int\",\"%lld\"]", value);
            return 0;
        }
        if (typed_is_float(t, n)) {
            memcpy(buffer, t, n);
            buffer[n] = 0;
            fputs("[\"float\",\"", out);
            typed_double(out, strtod(buffer, NULL));
            fputs("\"]", out);
            return 0;
        }
    }
    fputs("[\"str\",", out); typed_string(out, t, n); fputc(']', out);
    return 0;
}
#endif
