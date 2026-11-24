#include "harness.h"
#include <nxml.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Raw-name summary of libnxml's tree. libnxml always runs its own namespace
 * pass after parsing: it removes a bound prefix from element and attribute
 * names and points the node's ns field at that declaration (prefix and URI).
 * The adapter only re-joins the stored prefix and local name into the
 * qualified name as written; it resolves no namespace itself. libnxml's URIs
 * are not reported because the same pass also puts unprefixed attributes in
 * the default namespace, which Namespaces in XML does not.
 */

struct list { char **items; size_t len, cap; };
struct buffer { char *data; size_t len, cap; };
struct summary { struct list elements, attributes, text; struct buffer run; int max_depth, ok; };

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
/* prefix:local as written when libnxml bound a prefix, else the stored name; optional =value. */
static char *qname(const nxml_namespace_t *ns, const char *local, const char *value) {
    struct buffer b = {0}; int ok = 1;
    if (ns && ns->prefix) { append(&b, ns->prefix, strlen(ns->prefix), &ok); append(&b, ":", 1, &ok); }
    append(&b, local, strlen(local), &ok);
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

/* Document-order walk; text and CDATA nodes are NXML_TYPE_TEXT, comments and PIs end a text run. */
static void walk(struct summary *s, nxml_data_t *node, int depth) {
    for (; node && s->ok; node = node->next) {
        switch (node->type) {
        case NXML_TYPE_ELEMENT:
            flush(s);
            if (depth + 1 > s->max_depth) s->max_depth = depth + 1;
            push(&s->elements, qname(node->ns, node->value, NULL), &s->ok);
            for (nxml_attr_t *a = node->attributes; a && s->ok; a = a->next)
                push(&s->attributes, qname(a->ns, a->name, a->value ? a->value : ""), &s->ok);
            walk(s, node->children, depth + 1);
            flush(s);
            break;
        case NXML_TYPE_TEXT:
            if (node->value) append(&s->run, node->value, strlen(node->value), &s->ok);
            break;
        default:
            flush(s);
            break;
        }
    }
}

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

/* libnxml reports a failed parse as an nxml_error_t and the line it reached; keep both. */
static char last_error[160];
const char *parsarium_xml_error(void) { return last_error; }

/* Parse the whole byte buffer with nxml_parse_buffer, then walk libnxml's tree. */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    last_error[0] = 0;
    if (!data || !size || size > (1u << 20)) return NULL;
    /* nxml_parse_buffer takes a char buffer and an explicit size; keep a NUL after it. */
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size); text[size] = 0;
    nxml_t *doc = NULL;
    if (nxml_new(&doc) != NXML_OK) { free(text); return NULL; }
    nxml_error_t err = nxml_parse_buffer(doc, text, size);
    free(text);
    if (err != NXML_OK) {
        int line = 0;
        nxml_line_error(doc, &line);
        snprintf(last_error, sizeof(last_error), "nxml_parse_buffer failed: %s (line %d)", nxml_strerror(doc, err), line);
        nxml_free(doc);
        return NULL;
    }
    struct summary s = {0}; s.ok = 1;
    walk(&s, doc->data, 0);
    flush(&s);
    char *out = NULL;
    if (s.ok && s.elements.len) {
        struct buffer b = {0}; int ok = 1; char num[64];
        append(&b, "{", 1, &ok); array(&b, "attributes", &s.attributes, &ok);
        append(&b, ",", 1, &ok); array(&b, "elements", &s.elements, &ok);
        snprintf(num, sizeof(num), ",\"max_depth\":%d,\"root\":", s.max_depth);
        append(&b, num, strlen(num), &ok); quote(&b, s.elements.items[0], &ok);
        append(&b, ",", 1, &ok); array(&b, "text", &s.text, &ok); append(&b, "}", 1, &ok);
        if (ok) out = b.data; else free(b.data);
    } else if (s.ok) {
        snprintf(last_error, sizeof(last_error), "nxml_parse_buffer returned a document without an element");
    }
    release(&s.elements); release(&s.attributes); release(&s.text);
    free(s.run.data);
    nxml_free(doc);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
