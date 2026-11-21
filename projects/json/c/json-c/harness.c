#include "harness.h"

#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct text {
    const char *data;
    size_t size;
};

struct summary {
    size_t arrays, objects, booleans, nulls, max_depth;
    double *numbers;
    size_t number_count, number_capacity;
    struct text *strings;
    size_t string_count, string_capacity;
};

int parsarium_parse_json(const uint8_t *data, size_t size, struct json_object **out) {
    static int configured;
    struct json_tokener *tok;
    struct json_object *root;
    char *text;
    size_t end;
    int ok;
    *out = NULL;
    if (!data || size > (1u << 20)) return 0;
    if (!configured) {
        /* The Perl-like string hash has no random seed, so object table layout
         * and feedback repeat across runs. */
        json_global_set_string_hash(JSON_C_STR_HASH_PERLLIKE);
        configured = 1;
    }
    /* json_tokener_parse_ex documents that a caller at end of input passes the
     * final '\0' in len; copy the bytes so that terminator is in bounds. */
    text = malloc(size + 1);
    tok = json_tokener_new();
    if (!text || !tok) {
        free(text);
        if (tok) json_tokener_free(tok);
        return 0;
    }
    memcpy(text, data, size);
    text[size] = '\0';
    json_tokener_set_flags(tok, JSON_TOKENER_STRICT);
    root = json_tokener_parse_ex(tok, text, (int)size + 1);
    /* A JSON null root is a NULL json_object with json_tokener_success, so
     * success is reported separately from the object. */
    ok = json_tokener_get_error(tok) == json_tokener_success;
    if (ok) {
        /* Reject trailing bytes other than JSON whitespace. */
        for (end = json_tokener_get_parse_end(tok); end < size; end++) {
            char c = text[end];
            if (c != ' ' && c != '\t' && c != '\n' && c != '\r') {
                ok = 0;
                break;
            }
        }
    }
    if (!ok && root) {
        json_object_put(root);
        root = NULL;
    }
    json_tokener_free(tok);
    free(text);
    *out = root;
    return ok;
}

static int push_number(struct summary *s, double value) {
    if (s->number_count == s->number_capacity) {
        size_t capacity = s->number_capacity ? s->number_capacity * 2 : 16;
        double *grown = realloc(s->numbers, capacity * sizeof(*grown));
        if (!grown) return 0;
        s->numbers = grown;
        s->number_capacity = capacity;
    }
    s->numbers[s->number_count++] = value;
    return 1;
}

static int push_string(struct summary *s, const char *data, size_t size) {
    if (s->string_count == s->string_capacity) {
        size_t capacity = s->string_capacity ? s->string_capacity * 2 : 16;
        struct text *grown = realloc(s->strings, capacity * sizeof(*grown));
        if (!grown) return 0;
        s->strings = grown;
        s->string_capacity = capacity;
    }
    s->strings[s->string_count].data = data;
    s->strings[s->string_count++].size = size;
    return 1;
}

static int walk(struct json_object *value, size_t depth, struct summary *s) {
    size_t index, count;
    switch (json_object_get_type(value)) {
    case json_type_object:
        s->objects++;
        if (depth + 1 > s->max_depth) s->max_depth = depth + 1;
        {
            json_object_object_foreach(value, key, child) {
                (void)key;
                if (!walk(child, depth + 1, s)) return 0;
            }
        }
        return 1;
    case json_type_array:
        s->arrays++;
        if (depth + 1 > s->max_depth) s->max_depth = depth + 1;
        count = json_object_array_length(value);
        for (index = 0; index < count; index++)
            if (!walk(json_object_array_get_idx(value, index), depth + 1, s)) return 0;
        return 1;
    case json_type_string:
        return push_string(s, json_object_get_string(value),
                           (size_t)json_object_get_string_len(value));
    case json_type_int:
        return push_number(s, (double)json_object_get_int64(value));
    case json_type_double:
        return push_number(s, json_object_get_double(value));
    case json_type_boolean:
        s->booleans++;
        return 1;
    case json_type_null:
        s->nulls++;
        return 1;
    }
    return 0;
}

static int compare_numbers(const void *left, const void *right) {
    double a = *(const double *)left, b = *(const double *)right;
    return (a > b) - (a < b);
}

static int compare_texts(const void *left, const void *right) {
    const struct text *a = left, *b = right;
    size_t size = a->size < b->size ? a->size : b->size;
    int order = memcmp(a->data, b->data, size);
    if (order) return order;
    return (a->size > b->size) - (a->size < b->size);
}

static void print_string(const char *data, size_t size) {
    putchar('"');
    for (size_t i = 0; i < size; i++) {
        unsigned char c = (unsigned char)data[i];
        if (c == '"' || c == '\\') printf("\\%c", c);
        else if (c < 0x20) printf("\\u%04x", c);
        else putchar(c);
    }
    putchar('"');
}

/* Non-finite doubles (an out-of-range exponent json-c turned into infinity)
 * print as Infinity/-Infinity/NaN, which the observer's JSON reader accepts. */
static int print_nonfinite(double value) {
    if (isnan(value)) fputs("NaN", stdout);
    else if (isinf(value)) fputs(value > 0 ? "Infinity" : "-Infinity", stdout);
    else return 0;
    return 1;
}

static void print_number(double value) {
    if (print_nonfinite(value)) return;
    if (value == (double)(long long)value && value > -1e15 && value < 1e15)
        printf("%lld", (long long)value);
    else
        printf("%.17g", value);
}

void parsarium_print_tree(struct json_object *value) {
    size_t index, count;
    int first = 1;
    switch (json_object_get_type(value)) {
    case json_type_object:
        putchar('{');
        {
            json_object_object_foreach(value, key, child) {
                if (!first) putchar(',');
                first = 0;
                print_string(key, strlen(key));
                putchar(':');
                parsarium_print_tree(child);
            }
        }
        putchar('}');
        break;
    case json_type_array:
        putchar('[');
        count = json_object_array_length(value);
        for (index = 0; index < count; index++) {
            if (index) putchar(',');
            parsarium_print_tree(json_object_array_get_idx(value, index));
        }
        putchar(']');
        break;
    case json_type_string:
        print_string(json_object_get_string(value), (size_t)json_object_get_string_len(value));
        break;
    case json_type_int:
        printf("%" PRId64, json_object_get_int64(value));
        break;
    case json_type_double:
        if (!print_nonfinite(json_object_get_double(value)))
            printf("%.17g", json_object_get_double(value));
        break;
    case json_type_boolean:
        fputs(json_object_get_boolean(value) ? "true" : "false", stdout);
        break;
    case json_type_null:
        fputs("null", stdout);
        break;
    }
}

void parsarium_print_summary(struct json_object *root) {
    struct summary s = {0};
    if (!walk(root, 0, &s)) {
        free(s.numbers);
        free(s.strings);
        return;
    }
    qsort(s.numbers, s.number_count, sizeof(*s.numbers), compare_numbers);
    qsort(s.strings, s.string_count, sizeof(*s.strings), compare_texts);
    printf("{\"arrays\":%zu,\"booleans\":%zu,\"max_depth\":%zu,\"nulls\":%zu,\"numbers\":[",
           s.arrays, s.booleans, s.max_depth, s.nulls);
    for (size_t i = 0; i < s.number_count; i++) {
        if (i) putchar(',');
        print_number(s.numbers[i]);
    }
    printf("],\"objects\":%zu,\"root\":", s.objects);
    if (json_object_is_type(root, json_type_object)) {
        struct text *keys = calloc(json_object_object_length(root) + 1, sizeof(*keys));
        size_t count = 0;
        fputs("\"object\",\"strings\":[", stdout);
        for (size_t i = 0; i < s.string_count; i++) {
            if (i) putchar(',');
            print_string(s.strings[i].data, s.strings[i].size);
        }
        fputs("],\"top_level_keys\":[", stdout);
        if (keys) {
            json_object_object_foreach(root, key, child) {
                (void)child;
                keys[count].data = key;
                keys[count++].size = strlen(key);
            }
            qsort(keys, count, sizeof(*keys), compare_texts);
            for (size_t i = 0; i < count; i++) {
                if (i) putchar(',');
                print_string(keys[i].data, keys[i].size);
            }
        }
        fputs("]}\n", stdout);
        free(keys);
    } else if (json_object_is_type(root, json_type_array)) {
        fputs("\"array\",\"strings\":[", stdout);
        for (size_t i = 0; i < s.string_count; i++) {
            if (i) putchar(',');
            print_string(s.strings[i].data, s.strings[i].size);
        }
        printf("],\"top_level_items\":%zu}\n", json_object_array_length(root));
    } else {
        /* A scalar root (RFC 8259 allows any value) has no top-level members. */
        fputs("\"scalar\",\"strings\":[", stdout);
        for (size_t i = 0; i < s.string_count; i++) {
            if (i) putchar(',');
            print_string(s.strings[i].data, s.strings[i].size);
        }
        fputs("]}\n", stdout);
    }
    free(s.numbers);
    free(s.strings);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct json_object *root;
    if (parsarium_parse_json(data, size, &root) && root) {
        struct summary s = {0};
        (void)walk(root, 0, &s);
        free(s.numbers);
        free(s.strings);
        json_object_put(root);
    }
    return 0;
}
