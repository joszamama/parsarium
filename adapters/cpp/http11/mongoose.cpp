#include <mongoose.h>
#include <stdio.h>
#include "control.h"

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: mongoose control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct mg_http_message message;
    int consumed = mg_http_parse(buffer, length, &message);
    if (consumed != (int)length || message.proto.len != 8) {
        fprintf(stderr, "Mongoose HTTP parse failed\n");
        return 1;
    }
    printf("{\"method\":\"%.*s\",\"path\":\"%.*s?%.*s\",\"version\":\"%.*s\"}\n",
           (int)message.method.len, message.method.buf,
           (int)message.uri.len, message.uri.buf,
           (int)message.query.len, message.query.buf,
           (int)(message.proto.len - 5), message.proto.buf + 5);
    return 0;
}
