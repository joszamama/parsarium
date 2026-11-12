#include "control.h"
#include <libsoup/soup.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char bytes[4096];
    size_t length = read_control(argv[1], bytes, sizeof bytes - 1);
    bytes[length] = '\0';
    char *end = strstr(bytes, "\r\n\r\n");
    if (end == NULL) return 3;
    SoupMessageHeaders *headers = soup_message_headers_new(SOUP_MESSAGE_HEADERS_REQUEST);
    char *method = NULL;
    char *path = NULL;
    SoupHTTPVersion version = SOUP_HTTP_1_0;
    guint status = soup_headers_parse_request(bytes, (int)(end - bytes + 2),
                                               headers, &method, &path, &version);
    const char *host = soup_message_headers_get_one(headers, "Host");
    if (status != SOUP_STATUS_OK || method == NULL || path == NULL || host == NULL ||
        strcmp(method, "GET") || strcmp(path, "/parsarium?x=1") ||
        version != SOUP_HTTP_1_1 || strcmp(host, "example.test")) {
        fprintf(stderr, "libsoup did not parse the control request\n");
        g_free(method);
        g_free(path);
        soup_message_headers_unref(headers);
        return 4;
    }
    printf("{\"method\":\"%s\",\"path\":\"%s\",\"version\":\"1.1\",\"host\":\"%s\"}\n",
           method, path, host);
    g_free(method);
    g_free(path);
    soup_message_headers_unref(headers);
    return 0;
}
