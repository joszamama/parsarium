#include "harness.h"
#include <mxml.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Mini-XML does not implement Namespaces in XML: it reports element and
 * attribute names as written (prefix:local) and keeps xmlns declarations as
 * ordinary attributes. This adapter resolves them itself from mxml's parsed
 * tree with an in-scope binding stack, so the expanded names below are adapter
 * output over mxml's qnames, not namespace processing by mxml.
 */

struct list { char **items; size_t len, cap; };
struct buffer { char *data; size_t len, cap; };
struct binding { const char *prefix; size_t prefix_len; const char *uri; };
struct summary {
    struct list elements, attributes, namespaces, text;
    struct buffer run;
    struct binding *bindings; size_t nbindings, cbindings;
    size_t *scopes; size_t nscopes, cscopes;
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
static int grow(void **items, size_t *cap, size_t len, size_t size) {
    if (len < *cap) return 1;
    size_t next = *cap ? *cap * 2 : 16;
    void *data = realloc(*items, next * size);
    if (!data) return 0;
    *items = data; *cap = next;
    return 1;
}
/* Render a resolved name as {uri}local[=value]; an empty or absent URI means no namespace. */
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

static const char XML_URI[] = "http://www.w3.org/XML/1998/namespace";

/* Innermost binding for a prefix ("" is the default namespace); NULL when unbound. */
static const char *lookup(const struct summary *s, const char *prefix, size_t len) {
    if (len == 3 && !strncmp(prefix, "xml", 3)) return XML_URI;
    for (size_t i = s->nbindings; i-- > 0;)
        if (s->bindings[i].prefix_len == len && !strncmp(s->bindings[i].prefix, prefix, len)) return s->bindings[i].uri;
    return NULL;
}
/* Split an mxml qname and resolve it; unprefixed attributes have no namespace. */
static char *resolve(struct summary *s, const char *qname, const char *value, int attribute) {
    const char *colon = strchr(qname, ':');
    if (!colon) return clark(attribute ? NULL : lookup(s, "", 0), qname, value);
    const char *uri = lookup(s, qname, (size_t)(colon - qname));
    if (!uri || !*uri || !colon[1]) return NULL;
    return clark(uri, colon + 1, value);
}

static void on_element(struct summary *s, mxml_node_t *node, int depth) {
    size_t count = mxmlElementGetAttrCount(node);
    if (!grow((void **)&s->scopes, &s->cscopes, s->nscopes, sizeof(*s->scopes))) { s->ok = 0; return; }
    s->scopes[s->nscopes++] = s->nbindings;
    if (depth > s->max_depth) s->max_depth = depth;
    /* Declarations on an element apply to its own name and attributes, so bind them first. */
    for (size_t i = 0; i < count && s->ok; i++) {
        const char *name = NULL, *value = mxmlElementGetAttrByIndex(node, i, &name);
        if (!name) { s->ok = 0; break; }
        if (!value) value = "";
        const char *prefix;
        if (!strcmp(name, "xmlns")) prefix = "";
        else if (!strncmp(name, "xmlns:", 6) && name[6]) prefix = name + 6;
        else continue;
        if (!grow((void **)&s->bindings, &s->cbindings, s->nbindings, sizeof(*s->bindings))) { s->ok = 0; break; }
        s->bindings[s->nbindings++] = (struct binding){prefix, strlen(prefix), value};
        s->declarations++;
        if (!*value) continue;
        size_t j = 0;
        while (j < s->namespaces.len && strcmp(s->namespaces.items[j], value)) j++;
        if (j == s->namespaces.len) push(&s->namespaces, strdup(value), &s->ok);
    }
    push(&s->elements, resolve(s, mxmlGetElement(node), NULL, 0), &s->ok);
    for (size_t i = 0; i < count && s->ok; i++) {
        const char *name = NULL, *value = mxmlElementGetAttrByIndex(node, i, &name);
        if (!strcmp(name, "xmlns") || !strncmp(name, "xmlns:", 6)) continue;
        push(&s->attributes, resolve(s, name, value ? value : "", 1), &s->ok);
    }
}

/* Visit mxml's tree in document order without recursion. With a NULL top node,
 * mxml makes the <?xml ...?> declaration the parent of the rest of the document,
 * so children of any node are walked; only element nodes add depth or scope. */
static void walk(struct summary *s, mxml_node_t *node) {
    int depth = 0;
    while (node && s->ok) {
        mxml_type_t type = mxmlGetType(node);
        const char *value;
        switch (type) {
        case MXML_TYPE_ELEMENT: flush(s); on_element(s, node, ++depth); break;
        case MXML_TYPE_OPAQUE: if ((value = mxmlGetOpaque(node))) append(&s->run, value, strlen(value), &s->ok); break;
        case MXML_TYPE_CDATA: if ((value = mxmlGetCDATA(node))) append(&s->run, value, strlen(value), &s->ok); break;
        default: flush(s); break;
        }
        if (!s->ok) break;
        mxml_node_t *child = mxmlGetFirstChild(node);
        if (child) { node = child; continue; }
        /* Leave finished nodes until one has a next sibling; the top node's parent is NULL. */
        while (node) {
            if (mxmlGetType(node) == MXML_TYPE_ELEMENT) { flush(s); depth--; s->nbindings = s->scopes[--s->nscopes]; }
            mxml_node_t *next = mxmlGetNextSibling(node);
            if (next) { node = next; break; }
            node = mxmlGetParent(node);
        }
    }
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
static void quiet(void *user, const char *message) { (void)user; (void)message; }

/* Load the whole byte buffer as one string with mxmlLoadString (opaque text values), then walk the tree. */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    if (!data || !size || size > (1u << 20)) return NULL;
    /* mxmlLoadString takes a NUL-terminated string, so input stops at the first NUL byte. */
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size); text[size] = 0;
    mxml_options_t *options = mxmlOptionsNew();
    if (!options) { free(text); return NULL; }
    mxmlOptionsSetTypeValue(options, MXML_TYPE_OPAQUE);
    mxmlOptionsSetErrorCallback(options, quiet, NULL);
    mxml_node_t *tree = mxmlLoadString(NULL, options, text);
    mxmlOptionsDelete(options);
    free(text);
    if (!tree) return NULL;
    struct summary s = {0}; s.ok = 1;
    walk(&s, tree);
    flush(&s);
    char *out = NULL;
    if (s.ok && s.elements.len) {
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
    free(s.run.data); free(s.bindings); free(s.scopes);
    mxmlDelete(tree);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
