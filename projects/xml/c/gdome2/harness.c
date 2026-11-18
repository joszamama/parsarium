#include "harness.h"
#include <gdome.h>
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
/* Render {uri}local[=value]; a NULL or empty URI means no namespace. */
static char *clark(const char *uri, const char *local, const char *value) {
    struct buffer b = {0}; int ok = 1;
    if (uri && *uri) { append(&b, "{", 1, &ok); append(&b, uri, strlen(uri), &ok); append(&b, "}", 1, &ok); }
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
/* Copy a DOMString's UTF-8 text and drop the reference; NULL stays NULL. */
static char *take(GdomeDOMString *str) {
    if (!str) return NULL;
    char *copy = strdup(str->str ? str->str : "");
    gdome_str_unref(str);
    return copy;
}

#define XMLNS_URI "http://www.w3.org/2000/xmlns/"

static void walk(struct summary *s, GdomeNode *node, int depth) {
    GdomeException exc = 0;
    unsigned short type = gdome_n_nodeType(node, &exc);
    if (type == GDOME_TEXT_NODE || type == GDOME_CDATA_SECTION_NODE) {
        char *value = take(gdome_n_nodeValue(node, &exc));
        if (value) { append(&s->run, value, strlen(value), &s->ok); free(value); }
        return;
    }
    if (type != GDOME_ELEMENT_NODE) { flush(s); return; }
    flush(s);
    if (depth > s->max_depth) s->max_depth = depth;
    char *uri = take(gdome_n_namespaceURI(node, &exc)), *local = take(gdome_n_localName(node, &exc));
    if (!local) local = take(gdome_n_nodeName(node, &exc));
    push(&s->elements, local ? clark(uri, local, NULL) : NULL, &s->ok);
    free(uri); free(local);
    GdomeNamedNodeMap *attrs = gdome_n_attributes(node, &exc);
    unsigned long count = attrs ? gdome_nnm_length(attrs, &exc) : 0;
    for (unsigned long i = 0; i < count && s->ok; i++) {
        GdomeNode *attr = gdome_nnm_item(attrs, i, &exc);
        if (!attr) { s->ok = 0; break; }
        char *auri = take(gdome_n_namespaceURI(attr, &exc)), *alocal = take(gdome_n_localName(attr, &exc));
        char *name = take(gdome_n_nodeName(attr, &exc)), *value = take(gdome_n_nodeValue(attr, &exc));
        if (!name || !value) s->ok = 0;
        else if ((auri && !strcmp(auri, XMLNS_URI)) || !strcmp(name, "xmlns") || !strncmp(name, "xmlns:", 6)) {
            /* gdome2 exposes namespace declarations as attributes in the xmlns namespace. */
            s->declarations++;
            int seen = !*value;
            for (size_t k = 0; !seen && k < s->namespaces.len; k++) seen = !strcmp(s->namespaces.items[k], value);
            if (!seen) push(&s->namespaces, strdup(value), &s->ok);
        } else push(&s->attributes, clark(auri, alocal ? alocal : name, value), &s->ok);
        free(auri); free(alocal); free(name); free(value);
        gdome_n_unref(attr, &exc);
    }
    if (attrs) gdome_nnm_unref(attrs, &exc);
    GdomeNode *child = gdome_n_firstChild(node, &exc);
    while (child && s->ok) {
        walk(s, child, depth + 1);
        GdomeNode *next = gdome_n_nextSibling(child, &exc);
        gdome_n_unref(child, &exc);
        child = next;
    }
    if (child) gdome_n_unref(child, &exc);
    flush(s);
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

/* gdome_di_createDocFromMemory(GDOME_LOAD_PARSING) on a NUL-terminated copy of the local bytes, then a
   DOM Level 2 walk from gdome_doc_documentElement with namespaceURI/localName, attributes and child nodes. */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    if (!data || !size || size > (1u << 20) || memchr(data, 0, size)) return NULL;
    char *copy = malloc(size + 1);
    if (!copy) return NULL;
    memcpy(copy, data, size); copy[size] = 0;
    GdomeException exc = 0;
    GdomeDOMImplementation *impl = gdome_di_mkref();
    GdomeDocument *doc = impl ? gdome_di_createDocFromMemory(impl, copy, GDOME_LOAD_PARSING, &exc) : NULL;
    struct summary s = {0}; s.ok = 1;
    char *out = NULL;
    GdomeElement *root = doc ? gdome_doc_documentElement(doc, &exc) : NULL;
    if (root) {
        walk(&s, (GdomeNode *)root, 1);
        gdome_el_unref(root, &exc);
    }
    if (root && s.ok && s.elements.len) {
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
    if (doc) gdome_doc_unref(doc, &exc);
    if (impl) gdome_di_unref(impl, &exc);
    free(copy);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
