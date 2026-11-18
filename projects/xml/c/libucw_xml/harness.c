#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <ucw/lib.h>
#include <ucw/fastbuf.h>
#include <ucw-xml/xml.h>

/*
 * LibUCW 6.5's XML parser (ucw-xml) through its documented pull interface
 * (ucw-xml/xml.h, ucw-xml/doc/xml.txt): xml_init(), xml_ns_enable(), the
 * XML_ALLOC_ALL DOM flags, xml_push_fastbuf() over a read-only memory fastbuf
 * (fbbuf_init_read) of the local bytes, then xml_next() until EOF with
 * ctx.pull = CHARS | STAG | ETAG | COMMENT | PI, and xml_cleanup().
 * With namespaces enabled, each element and attribute carries a namespace ID
 * resolved by ucw-xml (xml_ns_by_id gives the URI) and a local name. ucw-xml
 * keeps namespace declarations as attributes: "xmlns:p" in the xmlns namespace
 * (XML_NS_XMLNS) and the default "xmlns" with no namespace; they are counted
 * as declarations and not reported as attributes. Attributes are reported in
 * ucw-xml's list order (source order on the controls).
 */

struct list { char **items; size_t len, cap; };
struct buffer { char *data; size_t len, cap; };
struct summary {
    struct list elements, attributes, namespaces, text;
    struct buffer run;
    int depth, declarations, max_depth, ok, failed;
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
static char *expanded(struct xml_context *ctx, uint ns, const char *local, const char *value) {
    struct buffer b = {0}; int ok = 1;
    if (ns != XML_NS_NONE) {
        const char *uri = xml_ns_by_id(ctx, ns);
        append(&b, "{", 1, &ok); append(&b, uri, strlen(uri), &ok); append(&b, "}", 1, &ok);
    }
    append(&b, local, strlen(local), &ok);
    if (value) { append(&b, "=", 1, &ok); append(&b, value, strlen(value), &ok); }
    if (!ok) { free(b.data); return NULL; }
    return b.data;
}
static void flush(struct summary *s) {
    if (!s->run.len) return;
    const char *start = s->run.data, *end = s->run.data + s->run.len;
    while (start < end && strchr(" \t\r\n", *start)) start++;
    while (end > start && strchr(" \t\r\n", end[-1])) end--;
    if (end > start) push(&s->text, strndup(start, (size_t)(end - start)), &s->ok);
    s->run.len = 0;
}
static void note_uri(struct summary *s, const char *uri) {
    if (!*uri) return;
    for (size_t i = 0; i < s->namespaces.len; i++) if (!strcmp(s->namespaces.items[i], uri)) return;
    push(&s->namespaces, strdup(uri), &s->ok);
}
static void start_tag(struct xml_context *ctx, struct summary *s) {
    struct xml_node *e = ctx->node;
    flush(s);
    push(&s->elements, expanded(ctx, e->ns, e->name, NULL), &s->ok);
    if (e->ns != XML_NS_NONE) note_uri(s, xml_ns_by_id(ctx, e->ns));
    if (++s->depth > s->max_depth) s->max_depth = s->depth;
    XML_ATTR_FOR_EACH(a, e) {
        if (a->ns == XML_NS_XMLNS || (a->ns == XML_NS_NONE && !strcmp(a->name, "xmlns"))) {
            s->declarations++;
            note_uri(s, a->val);
            continue;
        }
        push(&s->attributes, expanded(ctx, a->ns, a->name, a->val), &s->ok);
    }
}

static struct summary *current;
static void on_problem(struct xml_context *ctx) { (void)ctx; if (current) current->failed = 1; }

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

char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    if (!data || !size || size > (1u << 20)) return NULL;
    byte *copy = malloc(size);
    if (!copy) return NULL;
    memcpy(copy, data, size);
    struct summary s = {0}; s.ok = 1;
    current = &s;
    struct xml_context ctx;
    xml_init(&ctx);
    ctx.h_warn = ctx.h_error = ctx.h_fatal = on_problem;
    ctx.flags |= XML_ALLOC_ALL;
    xml_ns_enable(&ctx);
    struct fastbuf *fb = malloc(sizeof(*fb));
    if (!fb) { free(copy); xml_cleanup(&ctx); return NULL; }
    fbbuf_init_read(fb, copy, size, 0);
    xml_push_fastbuf(&ctx, fb);
    ctx.pull = XML_PULL_CHARS | XML_PULL_STAG | XML_PULL_ETAG | XML_PULL_COMMENT | XML_PULL_PI;
    uint state;
    while ((state = xml_next(&ctx))) {
        switch (state) {
        case XML_STATE_STAG: start_tag(&ctx, &s); break;
        case XML_STATE_ETAG: flush(&s); s.depth--; break;
        case XML_STATE_CHARS: append(&s.run, ctx.node->text, ctx.node->len, &s.ok); break;
        case XML_STATE_COMMENT: case XML_STATE_PI: flush(&s); break;
        default: break;
        }
    }
    flush(&s);
    char *out = NULL;
    if (!ctx.err_code && !s.failed && s.ok && s.elements.len) {
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
    xml_cleanup(&ctx);
    current = NULL;
    free(fb);
    free(copy);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
