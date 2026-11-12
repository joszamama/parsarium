#include <libwebsockets.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include "control.h"

struct result { int parsed; char method[16]; char path[256]; char query[64]; char host[128]; };

static int on_http(struct lws *wsi, enum lws_callback_reasons reason, void *user,
                   void *in, size_t length) {
    (void)user;
    struct result *result = lws_context_user(lws_get_context(wsi));
    if (reason != LWS_CALLBACK_HTTP) return 0;
    if (lws_hdr_total_length(wsi, WSI_TOKEN_GET_URI) > 0)
        snprintf(result->method, sizeof(result->method), "GET");
    if (length >= sizeof(result->path)) return 1;
    memcpy(result->path, in, length);
    result->path[length] = 0;
    if (lws_get_urlarg_by_name_safe(wsi, "x", result->query, sizeof(result->query)) < 0)
        return 1;
    if (lws_hdr_copy(wsi, result->host, sizeof(result->host), WSI_TOKEN_HOST) < 0)
        return 1;
    result->parsed = 1;
    return 1;
}

static const struct lws_protocols protocols[] = {
    {.name = "http", .callback = on_http},
    {0}
};

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: libwebsockets control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct result result = {0};
    struct lws_context_creation_info info = {0};
    info.port = CONTEXT_PORT_NO_LISTEN_SERVER;
    info.protocols = protocols;
    info.user = &result;
    info.vhost_name = "parsarium";
    info.gid = -1;
    info.uid = -1;
    lws_set_log_level(0, NULL);
    struct lws_context *context = lws_create_context(&info);
    if (!context) return 1;
    int sockets[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) return 1;
    struct lws_vhost *vhost = lws_get_vhost_by_name(context, "parsarium");
    if (!vhost) return 1;
    struct lws *adopted = lws_adopt_socket_vhost_readbuf(vhost, sockets[0], buffer, length);
    if (!adopted && !result.parsed) return 1;
    if (result.parsed) {
        printf("{\"method\":\"%s\",\"path\":\"%s?x=%s\",\"host\":\"%s\"}\n",
               result.method, result.path, result.query, result.host);
    }
    close(sockets[1]);
    lws_context_destroy(context);
    if (!result.parsed) { fprintf(stderr, "libwebsockets HTTP callback not reached\n"); return 1; }
    return 0;
}
