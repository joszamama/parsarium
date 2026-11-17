/* Local DNS message bytes reach getdns' documented getdns_wire2msg_dict(); the summary is read
 * back from the returned message dict with getdns_dict_get_* / getdns_list_get_*, names with
 * getdns_convert_dns_name_to_fqdn and addresses with getdns_display_ip_address. No context is
 * created, nothing is resolved and no socket is used. */
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <getdns/getdns.h>
#include <getdns/getdns_extra.h>

static int name_out(FILE *out, const getdns_dict *dict, const char *key) {
    getdns_bindata *name = NULL;
    char *text = NULL;
    if (getdns_dict_get_bindata(dict, key, &name) || getdns_convert_dns_name_to_fqdn(name, &text)) return -1;
    size_t length = strlen(text);
    for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)text[i]), out);
    if (length == 0 || text[length - 1] != '.') fputc('.', out);
    free(text);
    return 0;
}

static int address_out(FILE *out, const getdns_dict *rdata, const char *key) {
    getdns_bindata *address = NULL;
    if (getdns_dict_get_bindata(rdata, key, &address)) return -1;
    char *text = getdns_display_ip_address(address);
    if (!text) return -1;
    fputs(text, out);
    free(text);
    return 0;
}

static int rdata_out(FILE *out, const getdns_dict *rr, uint32_t type) {
    getdns_dict *rdata = NULL;
    uint32_t preference = 0;
    int status = 0;
    if (getdns_dict_get_dict(rr, "rdata", &rdata)) return -1;
    fputc('"', out);
    switch (type) {
    case GETDNS_RRTYPE_A: status = address_out(out, rdata, "ipv4_address"); break;
    case GETDNS_RRTYPE_AAAA: status = address_out(out, rdata, "ipv6_address"); break;
    case GETDNS_RRTYPE_CNAME: status = name_out(out, rdata, "cname"); break;
    case GETDNS_RRTYPE_NS: status = name_out(out, rdata, "nsdname"); break;
    case GETDNS_RRTYPE_PTR: status = name_out(out, rdata, "ptrdname"); break;
    case GETDNS_RRTYPE_MX:
        if (getdns_dict_get_int(rdata, "preference", &preference)) return -1;
        fprintf(out, "%u ", preference);
        status = name_out(out, rdata, "exchange");
        break;
    default:
        return -1;
    }
    fputc('"', out);
    return status;
}

static int section_out(FILE *out, const getdns_dict *msg, const char *key) {
    getdns_list *list = NULL;
    size_t count = 0;
    int status = 0;
    if (getdns_dict_get_list(msg, key, &list) || getdns_list_get_length(list, &count)) return -1;
    fputc('[', out);
    for (size_t i = 0; i < count; i++) {
        getdns_dict *rr = NULL;
        uint32_t type = 0, rrclass = 0, ttl = 0;
        if (getdns_list_get_dict(list, i, &rr) || getdns_dict_get_int(rr, "type", &type)
            || getdns_dict_get_int(rr, "class", &rrclass) || getdns_dict_get_int(rr, "ttl", &ttl)) return -1;
        fprintf(out, "%s{\"name\":\"", i ? "," : "");
        status |= name_out(out, rr, "name");
        fprintf(out, "\",\"type\":%u,\"class\":%u,\"ttl\":%u,\"rdata\":", type, rrclass, ttl);
        status |= rdata_out(out, rr, type);
        fputc('}', out);
    }
    fputc(']', out);
    return status;
}

static uint32_t header(const getdns_dict *msg, const char *key, int *status) {
    char path[32];
    uint32_t value = 0;
    snprintf(path, sizeof(path), "/header/%s", key);
    if (getdns_dict_get_int(msg, path, &value)) *status = -1;
    return value;
}

/* getdns reports the reserved Z bit, AD and CD as separate header fields; z carries all three. */
static int summarize(const uint8_t *data, size_t size, FILE *out) {
    getdns_dict *msg = NULL;
    if (!data || !out || size == 0 || size > 65535) return 1;
    if (getdns_wire2msg_dict(data, size, &msg) != GETDNS_RETURN_GOOD) return 2;
    int status = 0;
    uint32_t z = (header(msg, "z", &status) ? 4 : 0) | (header(msg, "ad", &status) ? 2 : 0)
        | (header(msg, "cd", &status) ? 1 : 0);
    fprintf(out, "{\"id\":%u,\"qr\":%u,\"opcode\":%u,\"aa\":%u,\"tc\":%u,\"rd\":%u,\"ra\":%u,\"z\":%u,"
            "\"rcode\":%u,", header(msg, "id", &status), header(msg, "qr", &status),
            header(msg, "opcode", &status), header(msg, "aa", &status), header(msg, "tc", &status),
            header(msg, "rd", &status), header(msg, "ra", &status), z, header(msg, "rcode", &status));
    uint32_t qdcount = header(msg, "qdcount", &status);
    fprintf(out, "\"qdcount\":%u,\"ancount\":%u,\"nscount\":%u,\"arcount\":%u,\"questions\":[", qdcount,
            header(msg, "ancount", &status), header(msg, "nscount", &status), header(msg, "arcount", &status));
    getdns_dict *question = NULL;
    if (!getdns_dict_get_dict(msg, "question", &question)) {
        uint32_t qtype = 0, qclass = 0;
        fputs("{\"name\":\"", out);
        status |= name_out(out, question, "qname");
        if (getdns_dict_get_int(question, "qtype", &qtype) || getdns_dict_get_int(question, "qclass", &qclass))
            status = -1;
        fprintf(out, "\",\"type\":%u,\"class\":%u}", qtype, qclass);
    } else if (qdcount) {
        status = -1;
    }
    fputs("],\"answers\":", out);
    status |= section_out(out, msg, "answer");
    fputs(",\"authority\":", out);
    status |= section_out(out, msg, "authority");
    fputs(",\"additional\":", out);
    status |= section_out(out, msg, "additional");
    fputs("}\n", out);
    getdns_dict_destroy(msg);
    return status ? 3 : 0;
}

/* The fuzz entry runs the same parse and dict walk into /dev/null. */
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    static FILE *sink;
    if (!sink) sink = fopen("/dev/null", "w");
    if (sink) summarize(data, size, sink);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc(65536);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, 65536, file);
    fclose(file);
    int status = summarize(data, size, stdout);
    free(data);
    return status;
}
#endif
