#include "harness.h"
#include <xmlb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Raw-name summary of a libxmlb silo. libxmlb's XbBuilder feeds the source to
 * GLib's GMarkup parser (G_MARKUP_TREAT_CDATA_AS_TEXT) and stores elements,
 * attributes, text and tail strings in a compiled silo. Neither GMarkup nor
 * libxmlb implements Namespaces in XML: names are kept as written and xmlns
 * declarations are ordinary attributes. Comments and processing instructions
 * go to GMarkup's passthrough callback, which libxmlb does not set, so they
 * are not in the silo. Text is loaded with XB_BUILDER_SOURCE_FLAG_LITERAL_TEXT
 * so libxmlb does not rewrap it; the adapter trims each run.
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
static char *pair(const char *name, const char *value) {
    struct buffer b = {0}; int ok = 1;
    if (!name) name = "";
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
static void add_text(struct summary *s, const char *text) {
    if (text) append(&s->run, text, strlen(text), &s->ok);
}

/* Element, its attributes, its text, then each child followed by that child's tail. */
/*
 * xb_node_get_element returns NULL for a node without a silo node. When
 * GMarkup stores nothing, xb_silo_get_root still returns such a placeholder
 * root ("if there are no XbSiloNodes, still build a root XbNode"). It is not
 * an element, so it is skipped like any non-element; a silo with no element
 * is reported below as libxmlb's rejection.
 */
static void walk(struct summary *s, XbNode *node, int depth) {
    const char *element = xb_node_get_element(node);
    if (!element) return;
    flush(s);
    if (depth > s->max_depth) s->max_depth = depth;
    push(&s->elements, pair(element, NULL), &s->ok);
    XbNodeAttrIter iter;
    const char *name, *value;
    xb_node_attr_iter_init(&iter, node);
    while (s->ok && xb_node_attr_iter_next(&iter, &name, &value))
        push(&s->attributes, pair(name, value ? value : ""), &s->ok);
    add_text(s, xb_node_get_text(node));
    XbNode *child = xb_node_get_child(node);
    while (child && s->ok) {
        walk(s, child, depth + 1);
        add_text(s, xb_node_get_tail(child));
        XbNode *next = xb_node_get_next(child);
        g_object_unref(child);
        child = next;
    }
    if (child) g_object_unref(child);
    flush(s);
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

/* libxmlb reports a failed load or compile as a GError; keep its message. */
static char last_error[256];
const char *parsarium_xml_error(void) { return last_error; }

/* Load the bytes with xb_builder_source_load_xml, compile a silo, then walk its nodes. */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    last_error[0] = 0;
    if (!data || !size || size > (1u << 20)) return NULL;
    /* xb_builder_source_load_xml takes a NUL-terminated string, so input stops at the first NUL byte. */
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size); text[size] = 0;
    GError *error = NULL;
    XbBuilderSource *source = xb_builder_source_new();
    gboolean loaded = xb_builder_source_load_xml(source, text, XB_BUILDER_SOURCE_FLAG_LITERAL_TEXT, &error);
    free(text);
    XbSilo *silo = NULL;
    if (loaded) {
        XbBuilder *builder = xb_builder_new();
        xb_builder_import_source(builder, source);
        silo = xb_builder_compile(builder, XB_BUILDER_COMPILE_FLAG_NONE, NULL, &error);
        g_object_unref(builder);
    }
    g_object_unref(source);
    if (error)
        snprintf(last_error, sizeof(last_error), "%s failed: %s",
                 loaded ? "xb_builder_compile" : "xb_builder_source_load_xml", error->message);
    g_clear_error(&error);
    if (!silo) return NULL;
    struct summary s = {0}; s.ok = 1;
    XbNode *node = xb_silo_get_root(silo);
    while (node && s.ok) {
        walk(&s, node, 1);
        XbNode *next = xb_node_get_next(node);
        g_object_unref(node);
        node = next;
    }
    if (node) g_object_unref(node);
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
        snprintf(last_error, sizeof(last_error), "xb_builder_compile returned a silo without an element");
    }
    release(&s.elements); release(&s.attributes); release(&s.text);
    free(s.run.data);
    g_object_unref(silo);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
