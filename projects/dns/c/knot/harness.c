/* Local DNS message bytes reach libknot's documented knot_pkt_new(wire, len, NULL) and
 * knot_pkt_parse(); the summary is read back with the libknot wire, packet-section and
 * rrset getters, knot_dname_to_str and knot_rrset_txt_dump_data. No resolver or socket is used. */
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <libknot/libknot.h>

static void name_out(FILE *out, const knot_dname_t *name) {
    char *text = knot_dname_to_str_alloc(name);
    if (!text) { fputs("?", out); return; }
    size_t length = strlen(text);
    for (size_t i = 0; i < length; i++) fputc(tolower((unsigned char)text[i]), out);
    if (length == 0 || text[length - 1] != '.') fputc('.', out);
    free(text);
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

static int rdata_out(FILE *out, const knot_rrset_t *rrset) {
    char text[1024];
    switch (rrset->type) {
    case KNOT_RRTYPE_A: case KNOT_RRTYPE_AAAA: case KNOT_RRTYPE_CNAME: case KNOT_RRTYPE_NS:
    case KNOT_RRTYPE_PTR: case KNOT_RRTYPE_MX: case KNOT_RRTYPE_TXT:
        break;
    default:
        return -1;
    }
    if (knot_rrset_txt_dump_data(rrset, 0, text, sizeof(text), &KNOT_DUMP_STYLE_DEFAULT) < 0) return -1;
    fputc('"', out);
    if (rrset->type == KNOT_RRTYPE_TXT) json_text(out, (const unsigned char *)text, strlen(text));
    else for (const char *p = text; *p; p++) fputc(tolower((unsigned char)*p), out);
    fputc('"', out);
    return 0;
}

static int section_out(FILE *out, const knot_pkt_t *packet, knot_section_t id) {
    const knot_pktsection_t *section = knot_pkt_section(packet, id);
    int status = 0;
    fputc('[', out);
    for (uint16_t i = 0; i < section->count; i++) {
        const knot_rrset_t *rrset = knot_pkt_rr(section, i);
        fprintf(out, "%s{\"name\":\"", i ? "," : "");
        name_out(out, rrset->owner);
        fprintf(out, "\",\"type\":%u,\"class\":%u,\"ttl\":%u,\"rdata\":", (unsigned)rrset->type,
                (unsigned)rrset->rclass, (unsigned)rrset->ttl);
        status |= rdata_out(out, rrset);
        fputc('}', out);
    }
    fputc(']', out);
    return status;
}

static int summarize(const uint8_t *data, size_t size, FILE *out) {
    if (!data || size == 0 || size > 65535) return 1;
    uint8_t *wire = malloc(size);
    if (!wire) return 1;
    memcpy(wire, data, size);
    knot_pkt_t *packet = knot_pkt_new(wire, (uint16_t)size, NULL);
    if (!packet) { free(wire); return 1; }
    int status = 0;
    if (knot_pkt_parse(packet, 0) != KNOT_EOK) {
        status = 2;
    } else if (out) {
        const uint8_t *h = packet->wire;
        /* libknot exposes the reserved Z bit, AD and CD separately. */
        int z = (knot_wire_get_z(h) ? 4 : 0) | (knot_wire_get_ad(h) ? 2 : 0) | (knot_wire_get_cd(h) ? 1 : 0);
        fprintf(out, "{\"id\":%u,\"qr\":%d,\"opcode\":%u,\"aa\":%d,\"tc\":%d,\"rd\":%d,\"ra\":%d,\"z\":%d,"
                "\"rcode\":%u,\"qdcount\":%u,\"ancount\":%u,\"nscount\":%u,\"arcount\":%u,\"questions\":[",
                (unsigned)knot_wire_get_id(h), knot_wire_get_qr(h) ? 1 : 0, (unsigned)knot_wire_get_opcode(h),
                knot_wire_get_aa(h) ? 1 : 0, knot_wire_get_tc(h) ? 1 : 0, knot_wire_get_rd(h) ? 1 : 0,
                knot_wire_get_ra(h) ? 1 : 0, z, (unsigned)knot_wire_get_rcode(h),
                (unsigned)knot_wire_get_qdcount(h), (unsigned)knot_wire_get_ancount(h),
                (unsigned)knot_wire_get_nscount(h), (unsigned)knot_wire_get_arcount(h));
        if (knot_wire_get_qdcount(h) > 0) {
            fputs("{\"name\":\"", out);
            name_out(out, knot_pkt_qname(packet));
            fprintf(out, "\",\"type\":%u,\"class\":%u}", (unsigned)knot_pkt_qtype(packet),
                    (unsigned)knot_pkt_qclass(packet));
        }
        fputs("],\"answers\":", out);
        status |= section_out(out, packet, KNOT_ANSWER);
        fputs(",\"authority\":", out);
        status |= section_out(out, packet, KNOT_AUTHORITY);
        fputs(",\"additional\":", out);
        status |= section_out(out, packet, KNOT_ADDITIONAL);
        fputs("}\n", out);
        status = status ? 3 : 0;
    }
    knot_pkt_free(packet);
    free(wire);
    return status;
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
