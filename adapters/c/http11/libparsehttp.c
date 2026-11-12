#include <assert.h>
#include <parsehttp.h>
#include <stdio.h>
#include <string.h>
#include "control.h"

struct result {
    char method[16], path[256], query[128], version[16], host[128];
    int complete;
};

static void save(char *to, size_t capacity, const char *from) {
    if (snprintf(to, capacity, "%s", from) >= (int)capacity) {
        fprintf(stderr, "parsed field too long\n");
        _Exit(1);
    }
}

static void method(const char *value, void *arg) {
    struct result *out = arg;
    save(out->method, sizeof(out->method), value);
}
static void path(const char *value, void *arg) {
    struct result *out = arg;
    save(out->path, sizeof(out->path), value);
}
static void query(const char *value, void *arg) {
    struct result *out = arg;
    save(out->query, sizeof(out->query), value);
}
static void version(const char *value, void *arg) {
    struct result *out = arg;
    save(out->version, sizeof(out->version), value);
}
static void host(const char *value, int port, void *arg) {
    struct result *out = arg;
    if (port != 0) { fprintf(stderr, "unexpected control port\n"); _Exit(1); }
    save(out->host, sizeof(out->host), value);
}
static void complete(void *arg) { ((struct result *)arg)->complete = 1; }

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: libparsehttp control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct result out = {0};
    parsehttp_t parser;
    if (parse_init(&parser) != &parser || parse_version() != LIBPARSEHTTP_VERSION) return 1;
    parse_setarg(&parser, &out);
    parse_setcb_method(&parser, method);
    parse_setcb_path(&parser, path);
    parse_setcb_params(&parser, query);
    parse_setcb_version(&parser, version);
    parse_setcb_host(&parser, host);
    parse_setcb_complete(&parser, complete);
    int remaining = parse_process(&parser, buffer, (int)length);
    parse_free(&parser);
    if (remaining != 0 || !out.complete) { fprintf(stderr, "parse incomplete\n"); return 1; }
    printf("{\"method\":\"%s\",\"path\":\"%s\",\"query\":\"%s\",\"version\":\"%s\",\"host\":\"%s\"}\n",
           out.method, out.path, out.query, out.version, out.host);
    return 0;
}
