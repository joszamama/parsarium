#include "harness.h"

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

json_t *parsarium_parse_json(const uint8_t *data, size_t size) {
    static int seeded;
    json_error_t error;
    if (!data || size > (1u << 20)) return NULL;
    if (!seeded) {
        /* A fixed hash seed keeps object table layout and feedback repeatable. */
        json_object_seed(1);
        seeded = 1;
    }
    return json_loadb((const char *)data, size, 0, &error);
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

static int walk(json_t *value, size_t depth, struct summary *s) {
    const char *key;
    json_t *child;
    size_t index;
    switch (json_typeof(value)) {
    case JSON_OBJECT:
        s->objects++;
        if (depth + 1 > s->max_depth) s->max_depth = depth + 1;
        json_object_foreach(value, key, child)
            if (!walk(child, depth + 1, s)) return 0;
        return 1;
    case JSON_ARRAY:
        s->arrays++;
        if (depth + 1 > s->max_depth) s->max_depth = depth + 1;
        json_array_foreach(value, index, child)
            if (!walk(child, depth + 1, s)) return 0;
        return 1;
    case JSON_STRING:
        return push_string(s, json_string_value(value), json_string_length(value));
    case JSON_INTEGER:
        return push_number(s, (double)json_integer_value(value));
    case JSON_REAL:
        return push_number(s, json_real_value(value));
    case JSON_TRUE:
    case JSON_FALSE:
        s->booleans++;
        return 1;
    case JSON_NULL:
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

static void print_number(double value) {
    if (value == (double)(long long)value && value > -1e15 && value < 1e15)
        printf("%lld", (long long)value);
    else
        printf("%.17g", value);
}

void parsarium_print_tree(json_t *value) {
    const char *key;
    json_t *child;
    size_t index;
    int first = 1;
    switch (json_typeof(value)) {
    case JSON_OBJECT:
        putchar('{');
        json_object_foreach(value, key, child) {
            if (!first) putchar(',');
            first = 0;
            print_string(key, strlen(key));
            putchar(':');
            parsarium_print_tree(child);
        }
        putchar('}');
        break;
    case JSON_ARRAY:
        putchar('[');
        json_array_foreach(value, index, child) {
            if (index) putchar(',');
            parsarium_print_tree(child);
        }
        putchar(']');
        break;
    case JSON_STRING:
        print_string(json_string_value(value), json_string_length(value));
        break;
    case JSON_INTEGER:
        printf("%" JSON_INTEGER_FORMAT, json_integer_value(value));
        break;
    case JSON_REAL:
        printf("%.17g", json_real_value(value));
        break;
    case JSON_TRUE:
        fputs("true", stdout);
        break;
    case JSON_FALSE:
        fputs("false", stdout);
        break;
    case JSON_NULL:
        fputs("null", stdout);
        break;
    }
}

void parsarium_print_summary(json_t *root) {
    struct summary s = {0};
    const char *key;
    json_t *child;
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
    if (json_is_object(root)) {
        struct text *keys = calloc(json_object_size(root) + 1, sizeof(*keys));
        size_t count = 0;
        fputs("\"object\",\"strings\":[", stdout);
        for (size_t i = 0; i < s.string_count; i++) {
            if (i) putchar(',');
            print_string(s.strings[i].data, s.strings[i].size);
        }
        fputs("],\"top_level_keys\":[", stdout);
        if (keys) {
            json_object_foreach(root, key, child) {
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
    } else {
        fputs("\"array\",\"strings\":[", stdout);
        for (size_t i = 0; i < s.string_count; i++) {
            if (i) putchar(',');
            print_string(s.strings[i].data, s.strings[i].size);
        }
        printf("],\"top_level_items\":%zu}\n", json_array_size(root));
    }
    free(s.numbers);
    free(s.strings);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    json_t *root = parsarium_parse_json(data, size);
    if (root) {
        struct summary s = {0};
        (void)walk(root, 0, &s);
        free(s.numbers);
        free(s.strings);
        json_decref(root);
    }
    return 0;
}
