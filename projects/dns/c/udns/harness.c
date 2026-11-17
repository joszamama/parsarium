/* Local DNS message bytes reach udns' documented raw-packet parsing routines: the header
 * accessor macros (dns_qid, dns_qr, ... dns_numar), dns_getdn for the question names and
 * dns_initparse/dns_nextrr for the resource records, with selection fields cleared so every
 * RR is returned. RDATA text uses udns' dns_ntop, dns_getdn and dns_dntop. No resolver
 * context is initialised and no socket is used. */
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>

#include <udns.h>

static void name_out(FILE *out, dnscc_t *dn) {
    char text[DNS_MAXNAME];
    if (dns_dntop(dn, text, sizeof(text)) <= 0) { fputs("?", out); return; }
    size_t length = strlen(text);
    for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)text[i]), out);
    if (length == 0 || text[length - 1] != '.') fputc('.', out);
}

static int rdata_out(FILE *out, dnscc_t *pkt, dnscc_t *end, const struct dns_rr *rr) {
    char text[64];
    dnsc_t dn[DNS_MAXDN];
    dnscc_t *cur = rr->dnsrr_dptr;
    fputc('"', out);
    switch (rr->dnsrr_typ) {
    case DNS_T_A:
        if (rr->dnsrr_dsz != 4 || !dns_ntop(AF_INET, rr->dnsrr_dptr, text, sizeof(text))) return -1;
        fputs(text, out);
        break;
    case DNS_T_AAAA:
        if (rr->dnsrr_dsz != 16 || !dns_ntop(AF_INET6, rr->dnsrr_dptr, text, sizeof(text))) return -1;
        fputs(text, out);
        break;
    case DNS_T_CNAME: case DNS_T_NS: case DNS_T_PTR:
        if (dns_getdn(pkt, &cur, end, dn, sizeof(dn)) <= 0 || cur != rr->dnsrr_dend) return -1;
        name_out(out, dn);
        break;
    case DNS_T_MX:
        if (rr->dnsrr_dsz < 3) return -1;
        fprintf(out, "%u ", dns_get16(cur));
        cur += 2;
        if (dns_getdn(pkt, &cur, end, dn, sizeof(dn)) <= 0 || cur != rr->dnsrr_dend) return -1;
        name_out(out, dn);
        break;
    default:
        return -1;
    }
    fputc('"', out);
    return 0;
}

static int section_out(FILE *out, struct dns_parse *p, int count, dnscc_t *pkt, dnscc_t *end) {
    struct dns_rr rr;
    int status = 0, i = 0, found;
    p->dnsp_rrl = count;
    fputc('[', out);
    while ((found = dns_nextrr(p, &rr)) > 0) {
        fprintf(out, "%s{\"name\":\"", i++ ? "," : "");
        name_out(out, rr.dnsrr_dn);
        fprintf(out, "\",\"type\":%u,\"class\":%u,\"ttl\":%u,\"rdata\":", (unsigned)rr.dnsrr_typ,
                (unsigned)rr.dnsrr_cls, rr.dnsrr_ttl);
        status |= rdata_out(out, pkt, end, &rr);
        fputc('}', out);
    }
    fputc(']', out);
    return found < 0 || i != count ? -1 : status;
}

/* udns has accessors for AD and CD but none for the reserved Z bit: z carries AD and CD. */
static int summarize(const uint8_t *data, size_t size, FILE *out) {
    if (!data || !out || size < DNS_HSIZE || size > 65535) return 1;
    dnscc_t *pkt = data, *end = data + size, *cur = dns_payload(pkt);
    dnsc_t qdn[DNS_MAXDN];
    unsigned qd = dns_numqd(pkt);
    if (qd == 0) return 1;
    {
        fprintf(out, "{\"id\":%u,\"qr\":%d,\"opcode\":%u,\"aa\":%d,\"tc\":%d,\"rd\":%d,\"ra\":%d,\"z\":%d,"
                "\"rcode\":%u,\"qdcount\":%u,\"ancount\":%u,\"nscount\":%u,\"arcount\":%u,\"questions\":[",
                dns_qid(pkt), dns_qr(pkt) ? 1 : 0, (unsigned)dns_opcode(pkt), dns_aa(pkt) ? 1 : 0,
                dns_tc(pkt) ? 1 : 0, dns_rd(pkt) ? 1 : 0, dns_ra(pkt) ? 1 : 0,
                (dns_ad(pkt) ? 2 : 0) | (dns_cd(pkt) ? 1 : 0), (unsigned)dns_rcode(pkt),
                dns_numqd(pkt), dns_numan(pkt), dns_numns(pkt), dns_numar(pkt));
    }
    dnscc_t *last = NULL;
    for (unsigned i = 0; i < qd; i++) {
        if (dns_getdn(pkt, &cur, end, qdn, sizeof(qdn)) <= 0 || cur + 4 > end) return 2;
        {
            fprintf(out, "%s{\"name\":\"", i ? "," : "");
            name_out(out, qdn);
            fprintf(out, "\",\"type\":%u,\"class\":%u}", dns_get16(cur), dns_get16(cur + 2));
        }
        last = cur;
        cur += 4;
    }
    struct dns_parse p;
    dns_initparse(&p, NULL, pkt, last, end);
    p.dnsp_qtyp = 0;  /* documented: 0 selects any type and class */
    p.dnsp_qcls = 0;
    int status = 0;
    fputs("],\"answers\":", out);
    status |= section_out(out, &p, dns_numan(pkt), pkt, end);
    fputs(",\"authority\":", out);
    status |= section_out(out, &p, dns_numns(pkt), pkt, end);
    fputs(",\"additional\":", out);
    status |= section_out(out, &p, dns_numar(pkt), pkt, end);
    fputs("}\n", out);
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
