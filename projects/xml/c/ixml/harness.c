#include "harness.h"
#include <ixml.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Raw-name summary of pupnp's IXML DOM tree. ixmlParseBufferEx builds a DOM
 * whose node names are the qualified names as written (prefix:local), with
 * xmlns/xmlns:* declarations kept as attributes in source order. IXML also
 * fills namespaceURI fields, but not conformantly (the default namespace is
 * not inherited below a prefixed root, an xmlns="" undeclaration is not
 * applied to its own element, and prefixed attributes get no URI), so its URIs
 * are not reported and the adapter resolves nothing itself.
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
/* name or name=value as stored by IXML. */
static char *pair(const char *name, const char *value) {
    struct buffer b = {0}; int ok = 1;
    if (!name) return NULL;
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

/* Document-order walk: text and CDATA nodes extend a run; any other node ends it. */
static void walk(struct summary *s, IXML_Node *node, int depth) {
    for (; node && s->ok; node = ixmlNode_getNextSibling(node)) {
        const char *value;
        switch (ixmlNode_getNodeType(node)) {
        case eELEMENT_NODE: {
            flush(s);
            if (depth + 1 > s->max_depth) s->max_depth = depth + 1;
            push(&s->elements, pair(ixmlNode_getNodeName(node), NULL), &s->ok);
            IXML_NamedNodeMap *attrs = ixmlNode_getAttributes(node);
            if (attrs) {
                unsigned long count = ixmlNamedNodeMap_getLength(attrs);
                for (unsigned long i = 0; i < count && s->ok; i++) {
                    IXML_Node *a = ixmlNamedNodeMap_item(attrs, i);
                    value = a ? ixmlNode_getNodeValue(a) : NULL;
                    push(&s->attributes, a ? pair(ixmlNode_getNodeName(a), value ? value : "") : NULL, &s->ok);
                }
                ixmlNamedNodeMap_free(attrs);
            }
            walk(s, ixmlNode_getFirstChild(node), depth + 1);
            flush(s);
            break;
        }
        case eTEXT_NODE:
        case eCDATA_SECTION_NODE:
            if ((value = ixmlNode_getNodeValue(node))) append(&s->run, value, strlen(value), &s->ok);
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

/* IXML reports failures only as an IXML_ERRORCODE; keep its name for the caller. */
static char last_error[96];
const char *parsarium_xml_error(void) { return last_error; }
static const char *code_name(int code) {
    switch (code) {
    case IXML_INDEX_SIZE_ERR: return "IXML_INDEX_SIZE_ERR";
    case IXML_DOMSTRING_SIZE_ERR: return "IXML_DOMSTRING_SIZE_ERR";
    case IXML_HIERARCHY_REQUEST_ERR: return "IXML_HIERARCHY_REQUEST_ERR";
    case IXML_WRONG_DOCUMENT_ERR: return "IXML_WRONG_DOCUMENT_ERR";
    case IXML_INVALID_CHARACTER_ERR: return "IXML_INVALID_CHARACTER_ERR";
    case IXML_NO_DATA_ALLOWED_ERR: return "IXML_NO_DATA_ALLOWED_ERR";
    case IXML_NO_MODIFICATION_ALLOWED_ERR: return "IXML_NO_MODIFICATION_ALLOWED_ERR";
    case IXML_NOT_FOUND_ERR: return "IXML_NOT_FOUND_ERR";
    case IXML_NOT_SUPPORTED_ERR: return "IXML_NOT_SUPPORTED_ERR";
    case IXML_INUSE_ATTRIBUTE_ERR: return "IXML_INUSE_ATTRIBUTE_ERR";
    case IXML_INVALID_STATE_ERR: return "IXML_INVALID_STATE_ERR";
    case IXML_SYNTAX_ERR: return "IXML_SYNTAX_ERR";
    case IXML_INVALID_MODIFICATION_ERR: return "IXML_INVALID_MODIFICATION_ERR";
    case IXML_NAMESPACE_ERR: return "IXML_NAMESPACE_ERR";
    case IXML_INVALID_ACCESS_ERR: return "IXML_INVALID_ACCESS_ERR";
    case IXML_NO_SUCH_FILE: return "IXML_NO_SUCH_FILE";
    case IXML_INSUFFICIENT_MEMORY: return "IXML_INSUFFICIENT_MEMORY";
    case IXML_FILE_DONE: return "IXML_FILE_DONE";
    case IXML_INVALID_PARAMETER: return "IXML_INVALID_PARAMETER";
    case IXML_FAILED: return "IXML_FAILED";
    case IXML_INVALID_ITEM_NUMBER: return "IXML_INVALID_ITEM_NUMBER";
    default: return "unknown IXML_ERRORCODE";
    }
}

/* Parse the whole byte buffer with ixmlParseBufferEx, then walk IXML's DOM. */
char *parsarium_parse_xml(const uint8_t *data, size_t size) {
    last_error[0] = 0;
    if (!data || !size || size > (1u << 20)) return NULL;
    /* ixmlParseBufferEx takes a NUL-terminated string, so input stops at the first NUL byte. */
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size); text[size] = 0;
    IXML_Document *doc = NULL;
    int err = ixmlParseBufferEx(text, &doc);
    free(text);
    if (err != IXML_SUCCESS || !doc) {
        snprintf(last_error, sizeof(last_error), "ixmlParseBufferEx failed: %s (%d)", code_name(err), err);
        if (doc) ixmlDocument_free(doc);
        return NULL;
    }
    struct summary s = {0}; s.ok = 1;
    walk(&s, ixmlNode_getFirstChild((IXML_Node *)doc), 0);
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
        snprintf(last_error, sizeof(last_error), "ixmlParseBufferEx returned a document without an element");
    }
    release(&s.elements); release(&s.attributes); release(&s.text);
    free(s.run.data);
    ixmlDocument_free(doc);
    return out;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    free(parsarium_parse_xml(data, size));
    return 0;
}
