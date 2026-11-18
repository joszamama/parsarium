#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "dtd.h"
#include "input.h"
#include "namespaces.h"
#include "xmlparser.h"

/*
 * RXP 1.5.0 as documented in doc/Manual: NewParser(), ParserSetFlag(p, XMLNamespaces, 1)
 * and ReturnComments, NewExternalEntity(0, 0, file, 0, 0) / EntityOpen / ParserPush, then
 * ReadXBit until XBIT_eof. With XMLNamespaces on, RXP resolves names itself: a start bit's
 * ns_element_definition and each attribute's ns_definition carry the namespace (nsname)
 * and local name. RXP does not return namespace declarations as attributes and documents
 * no declaration API (ns_dict is "not yet documented"), so this summary has no
 * declaration count; "namespaces" lists the URIs carried by expanded names, as for the
 * Python defusedxml path. Characters are UTF-16 (CHAR_SIZE 16) and are converted here.
 */

struct list { char **items; size_t len, cap; };
struct buffer { char *data; size_t len, cap; };
struct summary {
    struct list elements, attributes, namespaces, text;
    struct buffer run;
    int depth, max_depth, ok;
};

static int compare(const void *a, const void *b);

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
/* Append a NUL-terminated UTF-16 RXP string as UTF-8. */
static void append16(struct buffer *b, const Char *s, int *ok) {
    if (!s) return;
    for (size_t i = 0; s[i]; i++) {
        unsigned long c = s[i];
        if (c >= 0xD800 && c <= 0xDBFF && s[i + 1] >= 0xDC00 && s[i + 1] <= 0xDFFF) {
            c = 0x10000 + ((c - 0xD800) << 10) + (s[i + 1] - 0xDC00);
            i++;
        }
        char u[4]; size_t n;
        if (c < 0x80) { u[0] = (char)c; n = 1; }
        else if (c < 0x800) { u[0] = (char)(0xC0 | (c >> 6)); u[1] = (char)(0x80 | (c & 0x3F)); n = 2; }
        else if (c < 0x10000) { u[0] = (char)(0xE0 | (c >> 12)); u[1] = (char)(0x80 | ((c >> 6) & 0x3F)); u[2] = (char)(0x80 | (c & 0x3F)); n = 3; }
        else { u[0] = (char)(0xF0 | (c >> 18)); u[1] = (char)(0x80 | ((c >> 12) & 0x3F)); u[2] = (char)(0x80 | ((c >> 6) & 0x3F)); u[3] = (char)(0x80 | (c & 0x3F)); n = 4; }
        append(b, u, n, ok);
    }
}
static void note_uri(struct summary *s, const char *uri) {
    for (size_t i = 0; i < s->namespaces.len; i++) if (!strcmp(s->namespaces.items[i], uri)) return;
    push(&s->namespaces, strdup(uri), &s->ok);
}
/* {uri}local when RXP resolved a namespace, else the name as RXP holds it. */
static char *expanded(struct summary *s, Namespace ns, const Char *local, const Char *raw, const Char *value) {
    struct buffer b = {0}; int ok = 1;
    if (ns && ns->nsname && ns->nsname[0]) {
        struct buffer u = {0};
        append16(&u, ns->nsname, &ok);
        if (ok && u.data) note_uri(s, u.data);
        append(&b, "{", 1, &ok); if (u.data) append(&b, u.data, u.len, &ok); append(&b, "}", 1, &ok);
        free(u.data);
        append16(&b, local, &ok);
    } else {
        append16(&b, local ? local : raw, &ok);
    }
    if (value) { append(&b, "=", 1, &ok); append16(&b, value, &ok); }
    if (!ok) { free(b.data); return NULL; }
    if (!b.data) return strdup("");
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
static void start_bit(struct summary *s, XBit bit) {
    flush(s);
    NSElementDefinition nse = bit->ns_element_definition;
    push(&s->elements, expanded(s, nse ? nse->RXP_NAMESPACE : NULL, nse ? nse->name : NULL,
                                bit->element_definition->name, NULL), &s->ok);
    if (++s->depth > s->max_depth) s->max_depth = s->depth;
    /* RXP links a start tag's attributes in reverse source order (each new attribute is prepended),
       so the element's run is reversed back to source order. An unprefixed attribute is a per-element-type
       attribute (its NSAttributeDefinition has a non-null "element" field, Manual: namespaces.h):
       RXP files it under the element's namespace, which Namespaces in XML does not, so it is
       reported by its local name with no namespace. Prefixed (global) attributes keep RXP's URI. */
    size_t first = s->attributes.len;
    for (Attribute a = bit->attributes; a; a = a->next) {
        NSAttributeDefinition nsa = a->ns_definition;
        Namespace ns = nsa && !nsa->element ? nsa->RXP_NAMESPACE : NULL;
        push(&s->attributes, expanded(s, ns, nsa ? nsa->name : NULL, a->definition->name, a->value), &s->ok);
    }
    for (size_t i = first, j = s->attributes.len; s->ok && j > i + 1; i++, j--) {
        char *swap = s->attributes.items[i];
        s->attributes.items[i] = s->attributes.items[j - 1];
        s->attributes.items[j - 1] = swap;
    }
}

static void quiet(XBit bit, void *arg) { (void)bit; (void)arg; }

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
    /* RXP opens documents by system identifier; the local bytes go to a private temporary file. */
    char path[] = "/tmp/parsarium-rxp-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return NULL;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(fd, data + written, size - written);
        if (n <= 0) break;
        written += (size_t)n;
    }
    close(fd);
    if (written != size) { unlink(path); return NULL; }
    if (init_parser() < 0) { unlink(path); return NULL; }
    Parser p = NewParser();
    if (!p) { unlink(path); return NULL; }
    ParserSetFlag(p, XMLNamespaces, 1);
    ParserSetFlag(p, ReturnComments, 1);
    ParserSetWarningCallback(p, quiet);
    Entity ent = NewExternalEntity(0, 0, path, 0, 0);
    InputSource source = ent ? EntityOpen(ent) : NULL;
    struct summary s = {0}; s.ok = 1;
    int parsed = 0;
    if (source && ParserPush(p, source) != -1) {
        for (;;) {
            XBit bit = ReadXBit(p);
            if (bit->type == XBIT_eof) { parsed = 1; FreeXBit(bit); break; }
            if (bit->type == XBIT_error) { FreeXBit(bit); break; }
            switch (bit->type) {
            case XBIT_start: case XBIT_empty:
                start_bit(&s, bit);
                if (bit->type == XBIT_empty) { flush(&s); s.depth--; }
                break;
            case XBIT_end: flush(&s); s.depth--; break;
            case XBIT_pcdata: append16(&s.run, bit->pcdata_chars, &s.ok); break;
            case XBIT_cdsect: append16(&s.run, bit->cdsect_chars, &s.ok); break;
            case XBIT_comment: case XBIT_pi: flush(&s); break;
            default: break;
            }
            FreeXBit(bit);
        }
    }
    flush(&s);
    char *out = NULL;
    if (parsed && s.ok && s.elements.len) {
        qsort(s.namespaces.items, s.namespaces.len, sizeof(char *), compare);
        struct buffer b = {0}; int ok = 1; char num[64];
        append(&b, "{", 1, &ok); array(&b, "attributes", &s.attributes, &ok);
        append(&b, ",", 1, &ok); array(&b, "elements", &s.elements, &ok);
        snprintf(num, sizeof(num), ",\"max_depth\":%d,", s.max_depth);
        append(&b, num, strlen(num), &ok); array(&b, "namespaces", &s.namespaces, &ok);
        append(&b, ",\"root\":", 8, &ok); quote(&b, s.elements.items[0], &ok);
        append(&b, ",", 1, &ok); array(&b, "text", &s.text, &ok); append(&b, "}", 1, &ok);
        if (ok) out = b.data; else free(b.data);
    }
    release(&s.elements); release(&s.attributes); release(&s.namespaces); release(&s.text);
    free(s.run.data);
    FreeDtd(p->dtd);
    FreeParser(p);
    /* The document entity is the caller's (NewExternalEntity); the parser does not own it. */
    if (ent) FreeEntity(ent);
    unlink(path);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
