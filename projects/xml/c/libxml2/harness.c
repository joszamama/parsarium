#include "harness.h"
#include <libxml/parser.h>
#include <libxml/xmlreader.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct list { char **items; size_t len, cap; };
struct buffer { char *data; size_t len, cap; };
struct summary {
    struct list elements, attributes, namespaces, text;
    struct buffer run;
    int declarations, max_depth, ok;
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
/* Render the reader's namespace URI and local name as {uri}local[=value]. */
static char *clark(const xmlChar *uri, const xmlChar *local, const xmlChar *value) {
    struct buffer b = {0}; int ok = 1;
    if (!local) return NULL;
    if (uri) { append(&b, "{", 1, &ok); append(&b, (const char *)uri, strlen((const char *)uri), &ok); append(&b, "}", 1, &ok); }
    append(&b, (const char *)local, strlen((const char *)local), &ok);
    if (value) { append(&b, "=", 1, &ok); append(&b, (const char *)value, strlen((const char *)value), &ok); }
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

static const char XMLNS_URI[] = "http://www.w3.org/2000/xmlns/";

static void on_element(struct summary *s, xmlTextReaderPtr reader) {
    push(&s->elements, clark(xmlTextReaderConstNamespaceUri(reader), xmlTextReaderConstLocalName(reader), NULL), &s->ok);
    int depth = xmlTextReaderDepth(reader) + 1;
    if (depth > s->max_depth) s->max_depth = depth;
    while (xmlTextReaderMoveToNextAttribute(reader) == 1) {
        const xmlChar *uri = xmlTextReaderConstNamespaceUri(reader), *value = xmlTextReaderConstValue(reader);
        if (uri && !strcmp((const char *)uri, XMLNS_URI)) {
            s->declarations++;
            if (!value || !*value) continue;
            size_t i = 0;
            while (i < s->namespaces.len && strcmp(s->namespaces.items[i], (const char *)value)) i++;
            if (i == s->namespaces.len) push(&s->namespaces, strdup((const char *)value), &s->ok);
            continue;
        }
        push(&s->attributes, clark(uri, xmlTextReaderConstLocalName(reader), value ? value : (const xmlChar *)""), &s->ok);
    }
    xmlTextReaderMoveToElement(reader);
}

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
static void quiet(void *user, const xmlError *error) { (void)user; (void)error; }

/* Pull the whole byte buffer through a namespace-aware xmlTextReader (xmlReaderForMemory, xmlTextReaderRead). */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    if (!data || !size || size > (1u << 20)) return NULL;
    xmlTextReaderPtr reader = xmlReaderForMemory((const char *)data, (int)size, NULL, "UTF-8", XML_PARSE_NONET | XML_PARSE_NO_XXE);
    if (!reader) return NULL;
    xmlTextReaderSetStructuredErrorHandler(reader, quiet, NULL);
    struct summary s = {0}; s.ok = 1;
    int status;
    while ((status = xmlTextReaderRead(reader)) == 1) {
        switch (xmlTextReaderNodeType(reader)) {
        case XML_READER_TYPE_ELEMENT: flush(&s); on_element(&s, reader); break;
        case XML_READER_TYPE_END_ELEMENT: case XML_READER_TYPE_COMMENT: case XML_READER_TYPE_PROCESSING_INSTRUCTION: flush(&s); break;
        case XML_READER_TYPE_TEXT: case XML_READER_TYPE_CDATA: case XML_READER_TYPE_WHITESPACE: case XML_READER_TYPE_SIGNIFICANT_WHITESPACE: {
            const xmlChar *value = xmlTextReaderConstValue(reader);
            if (value) append(&s.run, (const char *)value, strlen((const char *)value), &s.ok);
            break;
        }
        default: break;
        }
    }
    flush(&s);
    char *out = NULL;
    if (status == 0 && s.ok && s.elements.len) {
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
    xmlFreeTextReader(reader);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
