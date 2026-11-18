/* Typed-tree output helpers for the Parsarium TOML protocol (catalog/toml/PROTOCOL.md).
 * Values come from the parser's own API; these helpers only format them. */
#ifndef PARSARIUM_TOML_EMIT_H
#define PARSARIUM_TOML_EMIT_H

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void emit_json_string(const char *s, size_t len) {
    putchar('"');
    for (size_t i = 0; i < len; i++) {
        unsigned char c = (unsigned char)s[i];
        switch (c) {
        case '"': fputs("\\\"", stdout); break;
        case '\\': fputs("\\\\", stdout); break;
        case '\b': fputs("\\b", stdout); break;
        case '\f': fputs("\\f", stdout); break;
        case '\n': fputs("\\n", stdout); break;
        case '\r': fputs("\\r", stdout); break;
        case '\t': fputs("\\t", stdout); break;
        default:
            if (c < 0x20 || c == 0x7f) printf("\\u%04x", c);
            else putchar(c);
        }
    }
    putchar('"');
}

static void emit_scalar(const char *type, const char *value, size_t len) {
    fputs("{\"type\":\"", stdout);
    fputs(type, stdout);
    fputs("\",\"value\":", stdout);
    emit_json_string(value, len);
    putchar('}');
}

static void emit_scalar_text(const char *type, const char *value) {
    emit_scalar(type, value, strlen(value));
}

static void emit_integer(int64_t value) {
    char text[32];
    snprintf(text, sizeof text, "%" PRId64, value);
    emit_scalar_text("integer", text);
}

/* Shortest round-trip digits (%.{1..17}g style search on %e), rewritten positionally
 * with at least one fractional digit: 1e3 -> 1000.0, 1.5625e-2 -> 0.015625. */
static int format_float(double value, char *out, size_t size) {
    char sci[64];
    int precision;
    for (precision = 0; precision <= 16; precision++) {
        snprintf(sci, sizeof sci, "%.*e", precision, value);
        if (strtod(sci, NULL) == value) break;
    }
    if (precision > 16) return -1;
    const char *p = sci;
    int negative = 0;
    if (*p == '-') { negative = 1; p++; }
    char digits[32];
    size_t n = 0;
    for (; *p && *p != 'e'; p++)
        if (*p >= '0' && *p <= '9') digits[n++] = *p;
    if (*p != 'e' || n == 0) return -1;
    int exponent = atoi(p + 1);
    while (n > 1 && digits[n - 1] == '0') n--;
    digits[n] = 0;
    char integer[400], fraction[400];
    size_t ni = 0, nf = 0;
    if (exponent >= 0) {
        for (int i = 0; i <= exponent; i++)
            integer[ni++] = (size_t)i < n ? digits[i] : '0';
        for (size_t i = (size_t)exponent + 1; i < n; i++) fraction[nf++] = digits[i];
    } else {
        integer[ni++] = '0';
        for (int i = 0; i < -exponent - 1; i++) fraction[nf++] = '0';
        for (size_t i = 0; i < n; i++) fraction[nf++] = digits[i];
    }
    while (nf > 1 && fraction[nf - 1] == '0') nf--;
    if (nf == 0) fraction[nf++] = '0';
    integer[ni] = 0;
    fraction[nf] = 0;
    int written = snprintf(out, size, "%s%s.%s", negative ? "-" : "", integer, fraction);
    return written > 0 && (size_t)written < size ? 0 : -1;
}

static int emit_float(double value) {
    char text[900];
    if (format_float(value, text, sizeof text)) return -1;
    emit_scalar_text("float", text);
    return 0;
}

/* Fraction of a second from microseconds: significant digits only, empty when zero. */
static void format_fraction(long usec, char *out) {
    if (usec <= 0) { out[0] = 0; return; }
    char digits[8];
    snprintf(digits, sizeof digits, "%06ld", usec);
    size_t n = 6;
    while (n > 0 && digits[n - 1] == '0') n--;
    digits[n] = 0;
    sprintf(out, ".%s", digits);
}

static int64_t days_from_civil(int64_t y, int64_t m, int64_t d) {
    y -= m <= 2;
    int64_t era = (y >= 0 ? y : y - 399) / 400;
    int64_t yoe = y - era * 400;
    int64_t doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    int64_t doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + doe - 719468;
}

static void civil_from_days(int64_t z, int *year, int *month, int *day) {
    z += 719468;
    int64_t era = (z >= 0 ? z : z - 146096) / 146097;
    int64_t doe = z - era * 146097;
    int64_t yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    int64_t y = yoe + era * 400;
    int64_t doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    int64_t mp = (5 * doy + 2) / 153;
    int64_t d = doy - (153 * mp + 2) / 5 + 1;
    int64_t m = mp + (mp < 10 ? 3 : -9);
    *year = (int)(y + (m <= 2));
    *month = (int)m;
    *day = (int)d;
}

/* Offset date-time -> UTC instant "YYYY-MM-DDTHH:MM:SS[.fraction]Z". */
static void emit_offset_datetime(int year, int month, int day, int hour, int minute,
                                 int second, long usec, int offset_minutes) {
    int64_t seconds = days_from_civil(year, month, day) * 86400 + hour * 3600 + minute * 60
                      + second - (int64_t)offset_minutes * 60;
    int64_t days = seconds >= 0 ? seconds / 86400 : -((-seconds + 86399) / 86400);
    int64_t rest = seconds - days * 86400;
    int y, m, d;
    civil_from_days(days, &y, &m, &d);
    char fraction[16], text[64];
    format_fraction(usec, fraction);
    snprintf(text, sizeof text, "%04d-%02d-%02dT%02d:%02d:%02d%sZ", y, m, d,
             (int)(rest / 3600), (int)(rest % 3600 / 60), (int)(rest % 60), fraction);
    emit_scalar_text("datetime", text);
}

static void emit_local_datetime(int year, int month, int day, int hour, int minute,
                                int second, long usec) {
    char fraction[16], text[64];
    format_fraction(usec, fraction);
    snprintf(text, sizeof text, "%04d-%02d-%02dT%02d:%02d:%02d%s", year, month, day,
             hour, minute, second, fraction);
    emit_scalar_text("datetime-local", text);
}

static void emit_local_date(int year, int month, int day) {
    char text[32];
    snprintf(text, sizeof text, "%04d-%02d-%02d", year, month, day);
    emit_scalar_text("date-local", text);
}

static void emit_local_time(int hour, int minute, int second, long usec) {
    char fraction[16], text[32];
    format_fraction(usec, fraction);
    snprintf(text, sizeof text, "%02d:%02d:%02d%s", hour, minute, second, fraction);
    emit_scalar_text("time-local", text);
}

#endif
