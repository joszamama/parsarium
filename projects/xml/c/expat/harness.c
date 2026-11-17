#include "harness.h"
#include <expat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct list { char **items; size_t len, cap; };
struct buffer { char *data; size_t len, cap; };
struct summary {
    struct list elements, attributes, namespaces, text;
    struct buffer run;
    int depth, declarations, max_depth, ok;
};

static void reserve(struct buffer *b, size_t extra, int *ok) {
    if (!*ok || b->len + extra + 1 <= b->cap) return;
    size_t cap = b->cap ? b->cap : 64;
    while (cap < b->len + extra + 1) cap *= 2;
    char *data = realloc(b->data, cap);
    if (!data) { *ok = 0; return; }
    b->data = data; b->cap = cap;
}
static void append(struct buffer *b, const char *s, size_t n, int *ok) {
    reserve(b, n, ok);
    if (!*ok) return;
    memcpy(b->data + b->len, s, n); b->len += n; b->data[b->len] = 0;
}
static void push(struct list *l, char *item, int *ok) {
    if (!item) { *ok = 0; return; }
    if (*ok && l->len == l->cap) {
        size_t cap = l->cap ? l->cap * 2 : 8;
        char **items = realloc(l->items, cap * sizeof(*items));
        if (items) { l->items = items; l->cap = cap; } else *ok = 0;
    }
    if (*ok) l->items[l->len++] = item; else free(item);
}
static void release(struct list *l) {
    for (size_t i = 0; i < l->len; i++) free(l->items[i]);
    free(l->items);
}
/* Expat reports "uri local" with the ' ' separator; render {uri}local[=value]. */
static char *clark(const XML_Char *name, const XML_Char *value) {
    struct buffer b = {0}; int ok = 1;
    const char *sep = strchr(name, ' ');
    if (sep) {
        append(&b, "{", 1, &ok); append(&b, name, (size_t)(sep - name), &ok); append(&b, "}", 1, &ok);
        name = sep + 1;
    }
    append(&b, name, strlen(name), &ok);
    if (value) { append(&b, "=", 1, &ok); append(&b, value, strlen(value), &ok); }
    if (!ok) { free(b.data); return NULL; }
    return b.data;
}
/* Trimmed non-empty run of character data between markup becomes one segment. */
static void flush(struct summary *s) {
    if (!s->run.len) return;
    const char *start = s->run.data, *end = s->run.data + s->run.len;
    while (start < end && strchr(" \t\r\n", *start)) start++;
    while (end > start && strchr(" \t\r\n", end[-1])) end--;
    if (end > start) push(&s->text, strndup(start, (size_t)(end - start)), &s->ok);
    s->run.len = 0;
}

static void on_start(void *user, const XML_Char *name, const XML_Char **attributes) {
    struct summary *s = user;
    flush(s);
    push(&s->elements, clark(name, NULL), &s->ok);
    if (++s->depth > s->max_depth) s->max_depth = s->depth;
    for (size_t i = 0; attributes[i]; i += 2) push(&s->attributes, clark(attributes[i], attributes[i + 1]), &s->ok);
}
static void on_end(void *user, const XML_Char *name) {
    struct summary *s = user; (void)name;
    flush(s);
    s->depth--;
}
static void on_namespace(void *user, const XML_Char *prefix, const XML_Char *uri) {
    struct summary *s = user; (void)prefix;
    s->declarations++;
    if (!uri || !*uri) return;
    for (size_t i = 0; i < s->namespaces.len; i++) if (!strcmp(s->namespaces.items[i], uri)) return;
    push(&s->namespaces, strdup(uri), &s->ok);
}
static void on_text(void *user, const XML_Char *text, int len) {
    struct summary *s = user;
    append(&s->run, text, (size_t)len, &s->ok);
}
static void on_comment(void *user, const XML_Char *data) { (void)data; flush(user); }
static void on_pi(void *user, const XML_Char *target, const XML_Char *data) { (void)target; (void)data; flush(user); }

static int compare(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }
static void quote(struct buffer *b, const char *s, int *ok) {
    append(b, "\"", 1, ok);
    for (; *s; s++) {
        unsigned char c = (unsigned char)*s; char esc[8];
        if (c == '"' || c == '\\') { esc[0] = '\\'; esc[1] = (char)c; append(b, esc, 2, ok); }
        else if (c < 0x20) { snprintf(esc, sizeof(esc), "\\u%04x", c); append(b, esc, 6, ok); }
        else append(b, s, 1, ok);
    }
    append(b, "\"", 1, ok);
}
static void array(struct buffer *b, const char *key, const struct list *l, int *ok) {
    quote(b, key, ok); append(b, ":[", 2, ok);
    for (size_t i = 0; i < l->len; i++) { if (i) append(b, ",", 1, ok); quote(b, l->items[i], ok); }
    append(b, "]", 1, ok);
}

/* Parse the whole byte buffer with a namespace-processing expat parser (XML_ParserCreateNS, XML_Parse isFinal). */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    if (!data || !size || size > (1u << 20)) return NULL;
    XML_Parser parser = XML_ParserCreateNS("UTF-8", ' ');
    if (!parser) return NULL;
    /* A fixed non-zero salt replaces expat's per-parser random hash salt so repeated runs take the same paths. */
    XML_SetHashSalt(parser, 0x5041525341524955UL);
    struct summary s = {0}; s.ok = 1;
    XML_SetUserData(parser, &s);
    XML_SetElementHandler(parser, on_start, on_end);
    XML_SetStartNamespaceDeclHandler(parser, on_namespace);
    XML_SetCharacterDataHandler(parser, on_text);
    XML_SetCommentHandler(parser, on_comment);
    XML_SetProcessingInstructionHandler(parser, on_pi);
    int parsed = XML_Parse(parser, (const char *)data, (int)size, XML_TRUE) == XML_STATUS_OK;
    flush(&s);
    char *out = NULL;
    if (parsed && s.ok && s.elements.len) {
        qsort(s.namespaces.items, s.namespaces.len, sizeof(char *), compare);
        struct buffer b = {0}; int ok = 1; char num[64];
        append(&b, "{", 1, &ok); array(&b, "attributes", &s.attributes, &ok);
        append(&b, ",", 1, &ok); array(&b, "elements", &s.elements, &ok);
        snprintf(num, sizeof(num), ",\"max_depth\":%d,\"namespace_declarations\":%d,", s.max_depth, s.declarations);
        append(&b, num, strlen(num), &ok); array(&b, "namespaces", &s.namespaces, &ok);
        append(&b, ",\"root\":", 8, &ok); quote(&b, s.elements.items[0], &ok);
        append(&b, ",", 1, &ok); array(&b, "text", &s.text, &ok); append(&b, "}", 1, &ok);
        if (ok) out = b.data; else free(b.data);
    }
    release(&s.elements); release(&s.attributes); release(&s.namespaces); release(&s.text);
    free(s.run.data);
    XML_ParserFree(parser);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
