/* Local DNS message bytes reach dns.c's public packet API: the bytes are copied into a
 * struct dns_packet made by dns_p_make (data/end, as the release's own `parse-packet`
 * command does), dns_p_study indexes the sections, dns_header() exposes the header and
 * dns_rr_grep (dns_rr_foreach) walks every question and record in packet order.
 * Names come from dns_d_expand and RDATA text from dns_any_parse + dns_any_print. No
 * resolver object is created and no socket is used. */
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

#include "dns.h"

static void text_out(FILE *out, const char *text, size_t length) {
    for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)text[i]), out);
    if (length == 0 || text[length - 1] != '.') fputc('.', out);
}

static int name_out(FILE *out, unsigned short at, struct dns_packet *P) {
    char name[DNS_D_MAXNAME + 1];
    int error = 0;
    size_t length = dns_d_expand(name, sizeof(name), at, P, &error);
    if (!length || length >= sizeof(name) || error) { fputs("?", out); return -1; }
    text_out(out, name, length);
    return 0;
}

/* Writes text inside a JSON string: quotes and backslashes escaped, other bytes outside
 * printable ASCII as \u00XX. */
static void json_text(FILE *out, const unsigned char *text, size_t length) {
    for (size_t i = 0; i < length; i++) {
        unsigned char c = text[i];
        if (c == '"' || c == '\\') { fputc('\\', out); fputc(c, out); }
        else if (c < 0x20 || c > 0x7e) fprintf(out, "\\u%04x", c);
        else fputc(c, out);
    }
}

static int rdata_out(FILE *out, struct dns_rr *rr, struct dns_packet *P) {
    union dns_any any;
    char text[sizeof(any) * 2];
    int error;
    dns_any_init(&any, sizeof(any));
    if ((error = dns_any_parse(&any, rr, P))) return -1;
    size_t length = dns_any_print(text, sizeof(text), &any, rr->type);
    if (!length || length >= sizeof(text)) return -1;
    fputc('"', out);
    switch (rr->type) {
    case DNS_T_CNAME: case DNS_T_NS: case DNS_T_PTR:
        text_out(out, text, length);
        break;
    case DNS_T_MX: {
        /* dns_any_print renders "<preference> <exchange>" */
        const char *space = memchr(text, ' ', length);
        if (!space) return -1;
        fwrite(text, 1, (size_t)(space - text) + 1, out);
        text_out(out, space + 1, length - (size_t)(space - text) - 1);
        break;
    }
    case DNS_T_A: case DNS_T_AAAA:
        fwrite(text, 1, length, out);
        break;
    case DNS_T_TXT:
        /* dns_txt_parse joins the character-strings; dns_any_print quotes the result. */
        json_text(out, (const unsigned char *)text, length);
        break;
    default:
        return -1;
    }
    fputc('"', out);
    return 0;
}

static const char *const section_names[] = {"answers", "authority", "additional"};

static int summarize(const uint8_t *data, size_t size, FILE *out) {
    if (!data || !out || size < 12 || size > 65535) return 1;
    int error = 0;
    struct dns_packet *P = dns_p_make(size, &error);
    if (!P) return 1;
    memcpy(P->data, data, size);
    P->end = size;
    int status = 0;
    if ((error = dns_p_study(P))) { free(P); return 2; }
    struct dns_header *h = dns_header(P);
    fprintf(out, "{\"id\":%u,\"qr\":%u,\"opcode\":%u,\"aa\":%u,\"tc\":%u,\"rd\":%u,\"ra\":%u,\"z\":%u,"
            "\"rcode\":%u,\"qdcount\":%u,\"ancount\":%u,\"nscount\":%u,\"arcount\":%u,\"questions\":[",
            (unsigned)ntohs(h->qid), (unsigned)h->qr, (unsigned)h->opcode, (unsigned)h->aa,
            (unsigned)h->tc, (unsigned)h->rd, (unsigned)h->ra, (unsigned)h->unused,
            (unsigned)dns_p_rcode(P), dns_p_count(P, DNS_S_QD), dns_p_count(P, DNS_S_AN),
            dns_p_count(P, DNS_S_NS), dns_p_count(P, DNS_S_AR));
    static const enum dns_section sections[] = {DNS_S_AN, DNS_S_NS, DNS_S_AR};
    unsigned questions = 0;
    struct dns_rr rr;
    dns_rr_foreach(&rr, P, .section = DNS_S_QD, .sort = &dns_rr_i_packet) {
        fprintf(out, "%s{\"name\":\"", questions++ ? "," : "");
        status |= name_out(out, rr.dn.p, P);
        fprintf(out, "\",\"type\":%u,\"class\":%u}", (unsigned)rr.type, (unsigned)rr.class);
    }
    fputs("]", out);
    for (size_t s = 0; s < 3; s++) {
        unsigned count = 0;
        fprintf(out, ",\"%s\":[", section_names[s]);
        dns_rr_foreach(&rr, P, .section = sections[s], .sort = &dns_rr_i_packet) {
            fprintf(out, "%s{\"name\":\"", count++ ? "," : "");
            status |= name_out(out, rr.dn.p, P);
            fprintf(out, "\",\"type\":%u,\"class\":%u,\"ttl\":%u,\"rdata\":", (unsigned)rr.type,
                    (unsigned)rr.class, rr.ttl);
            status |= rdata_out(out, &rr, P);
            fputc('}', out);
        }
        fputc(']', out);
        if (count != dns_p_count(P, sections[s])) status = -1;
    }
    fputs("}\n", out);
    if (questions != dns_p_count(P, DNS_S_QD)) status = -1;
    free(P);
    return status ? 3 : 0;
}

/* The fuzz entry runs the same parse and formatting path into /dev/null. */
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
