#include <htp/htp.h>
#include <stdio.h>
#include <string.h>
#include "control.h"

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: libhtp control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    htp_cfg_t *config = htp_config_create();
    if (!config) return 1;
    htp_connp_t *parser = htp_connp_create(config);
    if (!parser) return 1;
    htp_connp_open(parser, "127.0.0.1", 12345, "127.0.0.1", 80, NULL);
    int status = htp_connp_req_data(parser, NULL, buffer, length);
    htp_conn_t *connection = htp_connp_get_connection(parser);
    htp_tx_t *tx = connection && htp_list_size(connection->transactions) == 1
        ? htp_list_get(connection->transactions, 0) : NULL;
    if (status != HTP_STREAM_DATA || htp_connp_req_data_consumed(parser) != length ||
        !tx || !tx->request_method || !tx->request_uri || !tx->request_protocol ||
        !tx->request_headers || bstr_len(tx->request_protocol) < 5 ||
        memcmp(bstr_ptr(tx->request_protocol), "HTTP/", 5) != 0) {
        fprintf(stderr, "libhtp request parse failed: %d\n", status);
        htp_connp_destroy_all(parser);
        htp_config_destroy(config);
        return 1;
    }
    printf("{\"method\":\"%.*s\",\"path\":\"%.*s\",\"version\":\"%.*s\"}\n",
           (int)bstr_len(tx->request_method), bstr_ptr(tx->request_method),
           (int)bstr_len(tx->request_uri), bstr_ptr(tx->request_uri),
           (int)(bstr_len(tx->request_protocol) - 5), bstr_ptr(tx->request_protocol) + 5);
    htp_connp_destroy_all(parser);
    htp_config_destroy(config);
    return 0;
}
