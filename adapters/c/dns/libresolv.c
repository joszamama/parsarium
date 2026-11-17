/* Standard/runtime path: local DNS message bytes reach the C library resolver's message parser,
 * ns_initparse()/ns_parserr() from <arpa/nameser.h> (glibc libresolv), with the ns_msg_* and
 * ns_rr_* accessors. RDATA names are expanded with ns_name_uncompress and addresses formatted
 * with inet_ntop. No resolver is initialised, nothing is queried and no socket is used. */
#include <arpa/inet.h>
#include <arpa/nameser.h>
#include <ctype.h>
#include <resolv.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void text_out(FILE *out, const char *text) {
    size_t length = strlen(text);
    for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)text[i]), out);
    if (length == 0 || text[length - 1] != '.') fputc('.', out);
}

static int name_at(FILE *out, ns_msg *handle, const unsigned char *at) {
    char text[NS_MAXDNAME];
    if (ns_name_uncompress(ns_msg_base(*handle), ns_msg_end(*handle), at, text, sizeof(text)) < 0) return -1;
    text_out(out, text);
    return 0;
}

static int rdata_out(FILE *out, ns_msg *handle, ns_rr *rr) {
    char text[64];
    const unsigned char *rdata = ns_rr_rdata(*rr);
    int status = 0;
    fputc('"', out);
    switch (ns_rr_type(*rr)) {
    case ns_t_a:
        if (ns_rr_rdlen(*rr) != 4 || !inet_ntop(AF_INET, rdata, text, sizeof(text))) return -1;
        fputs(text, out);
        break;
    case ns_t_aaaa:
        if (ns_rr_rdlen(*rr) != 16 || !inet_ntop(AF_INET6, rdata, text, sizeof(text))) return -1;
        fputs(text, out);
        break;
    case ns_t_cname: case ns_t_ns: case ns_t_ptr:
        status = name_at(out, handle, rdata);
        break;
    case ns_t_mx:
        if (ns_rr_rdlen(*rr) < 3) return -1;
        fprintf(out, "%u ", ns_get16(rdata));
        status = name_at(out, handle, rdata + 2);
        break;
    default:
        return -1;
    }
    fputc('"', out);
    return status;
}

static int section_out(FILE *out, ns_msg *handle, ns_sect section, int question) {
    int status = 0;
    fputc('[', out);
    for (int i = 0; i < ns_msg_count(*handle, section); i++) {
        ns_rr rr;
        if (ns_parserr(handle, section, i, &rr) < 0) return -1;
        fprintf(out, "%s{\"name\":\"", i ? "," : "");
        text_out(out, ns_rr_name(rr));
        fprintf(out, "\",\"type\":%u,\"class\":%u", (unsigned)ns_rr_type(rr), (unsigned)ns_rr_class(rr));
        if (!question) {
            fprintf(out, ",\"ttl\":%u,\"rdata\":", (unsigned)ns_rr_ttl(rr));
            status |= rdata_out(out, handle, &rr);
        }
        fputc('}', out);
    }
    fputc(']', out);
    return status;
}

/* ns_msg_getflag exposes ns_f_z, ns_f_ad and ns_f_cd separately; z carries all three. */
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    unsigned char data[65536];
    size_t size = fread(data, 1, sizeof(data), file);
    fclose(file);
    ns_msg handle;
    if (ns_initparse(data, (int)size, &handle) < 0) return 4;
    int z = (ns_msg_getflag(handle, ns_f_z) ? 4 : 0) | (ns_msg_getflag(handle, ns_f_ad) ? 2 : 0)
        | (ns_msg_getflag(handle, ns_f_cd) ? 1 : 0);
    printf("{\"id\":%u,\"qr\":%d,\"opcode\":%d,\"aa\":%d,\"tc\":%d,\"rd\":%d,\"ra\":%d,\"z\":%d,\"rcode\":%d,"
           "\"qdcount\":%d,\"ancount\":%d,\"nscount\":%d,\"arcount\":%d,\"questions\":",
           (unsigned)ns_msg_id(handle), ns_msg_getflag(handle, ns_f_qr), ns_msg_getflag(handle, ns_f_opcode),
           ns_msg_getflag(handle, ns_f_aa), ns_msg_getflag(handle, ns_f_tc), ns_msg_getflag(handle, ns_f_rd),
           ns_msg_getflag(handle, ns_f_ra), z, ns_msg_getflag(handle, ns_f_rcode),
           ns_msg_count(handle, ns_s_qd), ns_msg_count(handle, ns_s_an), ns_msg_count(handle, ns_s_ns),
           ns_msg_count(handle, ns_s_ar));
    int status = section_out(stdout, &handle, ns_s_qd, 1);
    fputs(",\"answers\":", stdout);
    status |= section_out(stdout, &handle, ns_s_an, 0);
    fputs(",\"authority\":", stdout);
    status |= section_out(stdout, &handle, ns_s_ns, 0);
    fputs(",\"additional\":", stdout);
    status |= section_out(stdout, &handle, ns_s_ar, 0);
    fputs("}\n", stdout);
    return status ? 5 : 0;
}
