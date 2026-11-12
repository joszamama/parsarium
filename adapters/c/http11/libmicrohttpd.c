#include <microhttpd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>
#include "control.h"

struct result {
    pthread_mutex_t mutex;
    pthread_cond_t ready;
    int parsed;
    char method[32];
    char target[256];
    char version[32];
};

static enum MHD_Result on_request(void *closure, struct MHD_Connection *connection,
                                  const char *url, const char *method,
                                  const char *version, const char *upload,
                                  size_t *upload_size, void **request_closure) {
    (void)upload;
    (void)upload_size;
    (void)request_closure;
    struct result *result = closure;
    const char *query = MHD_lookup_connection_value(connection, MHD_GET_ARGUMENT_KIND, "x");
    pthread_mutex_lock(&result->mutex);
    if (!result->parsed && query &&
        snprintf(result->method, sizeof(result->method), "%s", method) < (int)sizeof(result->method) &&
        snprintf(result->target, sizeof(result->target), "%s?x=%s", url, query) < (int)sizeof(result->target) &&
        snprintf(result->version, sizeof(result->version), "%s", version) < (int)sizeof(result->version)) {
        result->parsed = 1;
        pthread_cond_signal(&result->ready);
    }
    pthread_mutex_unlock(&result->mutex);
    return MHD_YES;
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: libmicrohttpd control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct result result = {0};
    pthread_mutex_init(&result.mutex, NULL);
    pthread_cond_init(&result.ready, NULL);
    struct MHD_Daemon *daemon = MHD_start_daemon(MHD_USE_INTERNAL_POLLING_THREAD |
                                                  MHD_USE_NO_LISTEN_SOCKET, 0,
                                                  NULL, NULL, on_request, &result,
                                                  MHD_OPTION_END);
    if (!daemon) { fprintf(stderr, "libmicrohttpd daemon start failed\n"); return 1; }
    int sockets[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) return 1;
    struct sockaddr_in peer = {0};
    peer.sin_family = AF_INET;
    peer.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (MHD_add_connection(daemon, sockets[0], (struct sockaddr *)&peer, sizeof(peer)) != MHD_YES)
        return 1;
    if (write(sockets[1], buffer, length) != (ssize_t)length) return 1;
    struct timespec deadline;
    clock_gettime(CLOCK_REALTIME, &deadline);
    deadline.tv_sec += 5;
    pthread_mutex_lock(&result.mutex);
    while (!result.parsed && pthread_cond_timedwait(&result.ready, &result.mutex, &deadline) == 0) {}
    int parsed = result.parsed;
    if (parsed) {
        printf("{\"method\":\"%s\",\"path\":\"%s\",\"version\":\"%s\"}\n",
               result.method, result.target, result.version + 5);
    }
    pthread_mutex_unlock(&result.mutex);
    close(sockets[1]);
    MHD_stop_daemon(daemon);
    pthread_cond_destroy(&result.ready);
    pthread_mutex_destroy(&result.mutex);
    if (!parsed) { fprintf(stderr, "libmicrohttpd request callback not reached\n"); return 1; }
    return 0;
}
