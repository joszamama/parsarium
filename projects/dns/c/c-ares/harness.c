/* Local DNS message bytes reach c-ares' documented ares_dns_parse(); the summary is read back
 * through the ares_dns_record_* and ares_dns_rr_* getters. No channel, socket or query is made. */
#include <arpa/inet.h>
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ares.h"

static void name_out(FILE *out, const char *name) {
    fputc('"', out);
    for (const char *p = name; *p; p++) fputc(tolower((unsigned char)*p), out);
    if (name[0] == '\0' || name[strlen(name) - 1] != '.') fputc('.', out);
    fputc('"', out);
}

static int rdata_out(FILE *out, const ares_dns_rr_t *rr) {
    char text[INET6_ADDRSTRLEN];
    switch (ares_dns_rr_get_type(rr)) {
    case ARES_REC_TYPE_A:
        inet_ntop(AF_INET, ares_dns_rr_get_addr(rr, ARES_RR_A_ADDR), text, sizeof text);
        fprintf(out, "\"%s\"", text);
        return 0;
    case ARES_REC_TYPE_AAAA:
        inet_ntop(AF_INET6, ares_dns_rr_get_addr6(rr, ARES_RR_AAAA_ADDR), text, sizeof text);
        fprintf(out, "\"%s\"", text);
        return 0;
    case ARES_REC_TYPE_CNAME:
        name_out(out, ares_dns_rr_get_str(rr, ARES_RR_CNAME_CNAME));
        return 0;
    case ARES_REC_TYPE_NS:
        name_out(out, ares_dns_rr_get_str(rr, ARES_RR_NS_NSDNAME));
        return 0;
    case ARES_REC_TYPE_PTR:
        name_out(out, ares_dns_rr_get_str(rr, ARES_RR_PTR_DNAME));
        return 0;
    case ARES_REC_TYPE_MX: {
        const char *exchange = ares_dns_rr_get_str(rr, ARES_RR_MX_EXCHANGE);
        size_t length = strlen(exchange);
        fprintf(out, "\"%u ", ares_dns_rr_get_u16(rr, ARES_RR_MX_PREFERENCE));
        for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)exchange[i]), out);
        if (length == 0 || exchange[length - 1] != '.') fputc('.', out);
        fputc('"', out);
        return 0;
    }
    case ARES_REC_TYPE_TXT: {
        size_t count = ares_dns_rr_get_abin_cnt(rr, ARES_RR_TXT_DATA);
        fputc('"', out);
        for (size_t i = 0; i < count; i++) {
            size_t length = 0;
            const unsigned char *data = ares_dns_rr_get_abin(rr, ARES_RR_TXT_DATA, i, &length);
            fprintf(out, "%s\\\"", i ? " " : "");
            fwrite(data, 1, length, out);
            fputs("\\\"", out);
        }
        fputc('"', out);
        return 0;
    }
    default:
        return -1;
    }
}

static int section_out(FILE *out, const ares_dns_record_t *record, ares_dns_section_t section) {
    size_t count = ares_dns_record_rr_cnt(record, section);
    fputc('[', out);
    for (size_t i = 0; i < count; i++) {
        const ares_dns_rr_t *rr = ares_dns_record_rr_get_const(record, section, i);
        fprintf(out, "%s{\"name\":", i ? "," : "");
        name_out(out, ares_dns_rr_get_name(rr));
        fprintf(out, ",\"type\":%u,\"class\":%u,\"ttl\":%u,\"rdata\":", (unsigned)ares_dns_rr_get_type(rr),
                (unsigned)ares_dns_rr_get_class(rr), ares_dns_rr_get_ttl(rr));
        if (rdata_out(out, rr)) return -1;
        fputc('}', out);
    }
    fputc(']', out);
    return 0;
}

/* c-ares keeps QR, AA, TC, RD, RA, AD and CD but not the reserved Z bit: z carries AD and CD. */
static int summarize(const uint8_t *data, size_t size, FILE *out) {
    ares_dns_record_t *record = NULL;
    if (!data || size == 0 || size > 65535) return 1;
    if (ares_dns_parse(data, size, 0, &record) != ARES_SUCCESS) return 2;
    unsigned short flags = ares_dns_record_get_flags(record);
    size_t questions = ares_dns_record_query_cnt(record);
    int status = 0;
    if (out) {
        fprintf(out, "{\"id\":%u,\"qr\":%d,\"opcode\":%u,\"aa\":%d,\"tc\":%d,\"rd\":%d,\"ra\":%d,\"z\":%d,"
                "\"rcode\":%u,\"qdcount\":%zu,\"ancount\":%zu,\"nscount\":%zu,\"arcount\":%zu,\"questions\":[",
                ares_dns_record_get_id(record), !!(flags & ARES_FLAG_QR),
                (unsigned)ares_dns_record_get_opcode(record), !!(flags & ARES_FLAG_AA), !!(flags & ARES_FLAG_TC),
                !!(flags & ARES_FLAG_RD), !!(flags & ARES_FLAG_RA),
                (!!(flags & ARES_FLAG_AD) << 1) | !!(flags & ARES_FLAG_CD),
                (unsigned)ares_dns_record_get_rcode(record), questions,
                ares_dns_record_rr_cnt(record, ARES_SECTION_ANSWER),
                ares_dns_record_rr_cnt(record, ARES_SECTION_AUTHORITY),
                ares_dns_record_rr_cnt(record, ARES_SECTION_ADDITIONAL));
        for (size_t i = 0; i < questions; i++) {
            const char *name = NULL;
            ares_dns_rec_type_t type;
            ares_dns_class_t klass;
            ares_dns_record_query_get(record, i, &name, &type, &klass);
            fprintf(out, "%s{\"name\":", i ? "," : "");
            name_out(out, name);
            fprintf(out, ",\"type\":%u,\"class\":%u}", (unsigned)type, (unsigned)klass);
        }
        fputs("],\"answers\":", out);
        status |= section_out(out, record, ARES_SECTION_ANSWER);
        fputs(",\"authority\":", out);
        status |= section_out(out, record, ARES_SECTION_AUTHORITY);
        fputs(",\"additional\":", out);
        status |= section_out(out, record, ARES_SECTION_ADDITIONAL);
        fputs("}\n", out);
    }
    ares_dns_record_destroy(record);
    return status ? 3 : 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    summarize(data, size, NULL);
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
