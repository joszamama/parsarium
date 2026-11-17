/* Local DNS message bytes reach ldns' documented ldns_wire2pkt(); the summary is read back
 * with the ldns_pkt_* and ldns_rr_* getters and ldns_rdf2str. No resolver or socket is used. */
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <ldns/ldns.h>

static void lower_name_out(FILE *out, const char *text) {
    size_t length = strlen(text);
    for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)text[i]), out);
    if (length == 0 || text[length - 1] != '.') fputc('.', out);
}

static int rdf_text(FILE *out, const ldns_rdf *rdf, int is_name) {
    char *text = ldns_rdf2str(rdf);
    if (!text) return -1;
    if (is_name) lower_name_out(out, text); else fputs(text, out);
    free(text);
    return 0;
}

static int rdata_out(FILE *out, const ldns_rr *rr) {
    int status = 0;
    fputc('"', out);
    switch (ldns_rr_get_type(rr)) {
    case LDNS_RR_TYPE_A:
    case LDNS_RR_TYPE_AAAA:
        status = rdf_text(out, ldns_rr_rdf(rr, 0), 0);
        break;
    case LDNS_RR_TYPE_CNAME:
    case LDNS_RR_TYPE_NS:
    case LDNS_RR_TYPE_PTR:
        status = rdf_text(out, ldns_rr_rdf(rr, 0), 1);
        break;
    case LDNS_RR_TYPE_MX:
        status = rdf_text(out, ldns_rr_rdf(rr, 0), 0);
        fputc(' ', out);
        status |= rdf_text(out, ldns_rr_rdf(rr, 1), 1);
        break;
    default:
        return -1;
    }
    fputc('"', out);
    return status;
}

static int section_out(FILE *out, const ldns_rr_list *list, int question) {
    size_t count = ldns_rr_list_rr_count(list);
    int status = 0;
    fputc('[', out);
    for (size_t i = 0; i < count; i++) {
        const ldns_rr *rr = ldns_rr_list_rr(list, i);
        fprintf(out, "%s{\"name\":\"", i ? "," : "");
        status |= rdf_text(out, ldns_rr_owner(rr), 1);
        fprintf(out, "\",\"type\":%u,\"class\":%u", (unsigned)ldns_rr_get_type(rr), (unsigned)ldns_rr_get_class(rr));
        if (!question) {
            fprintf(out, ",\"ttl\":%u,\"rdata\":", (unsigned)ldns_rr_ttl(rr));
            status |= rdata_out(out, rr);
        }
        fputc('}', out);
    }
    fputc(']', out);
    return status;
}

/* ldns keeps AD and CD but has no getter for the reserved Z bit: z carries AD and CD. */
static int summarize(const uint8_t *data, size_t size, FILE *out) {
    ldns_pkt *packet = NULL;
    if (!data || size == 0 || size > 65535) return 1;
    if (ldns_wire2pkt(&packet, data, size) != LDNS_STATUS_OK) return 2;
    int status = 0;
    if (out) {
        fprintf(out, "{\"id\":%u,\"qr\":%d,\"opcode\":%u,\"aa\":%d,\"tc\":%d,\"rd\":%d,\"ra\":%d,\"z\":%d,"
                "\"rcode\":%u,\"qdcount\":%u,\"ancount\":%u,\"nscount\":%u,\"arcount\":%u,\"questions\":",
                (unsigned)ldns_pkt_id(packet), ldns_pkt_qr(packet), (unsigned)ldns_pkt_get_opcode(packet),
                ldns_pkt_aa(packet), ldns_pkt_tc(packet), ldns_pkt_rd(packet), ldns_pkt_ra(packet),
                (ldns_pkt_ad(packet) << 1) | ldns_pkt_cd(packet), (unsigned)ldns_pkt_get_rcode(packet),
                (unsigned)ldns_pkt_qdcount(packet), (unsigned)ldns_pkt_ancount(packet),
                (unsigned)ldns_pkt_nscount(packet), (unsigned)ldns_pkt_arcount(packet));
        status |= section_out(out, ldns_pkt_question(packet), 1);
        fputs(",\"answers\":", out);
        status |= section_out(out, ldns_pkt_answer(packet), 0);
        fputs(",\"authority\":", out);
        status |= section_out(out, ldns_pkt_authority(packet), 0);
        fputs(",\"additional\":", out);
        status |= section_out(out, ldns_pkt_additional(packet), 0);
        fputs("}\n", out);
    }
    ldns_pkt_free(packet);
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
