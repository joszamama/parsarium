# DNS message wire format (RFC 1035 section 4) as one local message.
# Either a standard query (one question, no records) or a response with one
# question and one to four answer records of type A, AAAA, CNAME, MX or TXT.
# The header counts are fixed by the alternative chosen, so QDCOUNT and
# ANCOUNT always match the sections. Each variable RDLENGTH is a 16-bit
# big-endian field that a constraint ties to its RDATA length; Fandango
# repairs it directly.
#
# Name compression (RFC 1035 section 4.1.4) is limited to one pointer
# target: the question name, which always starts at offset 12. An owner,
# CNAME target or MX exchange is either written in full or is the pointer
# C0 0C. Pointers into the middle of a name or to earlier records are not
# generated, because their offsets depend on the lengths before them.
# Labels come from a fixed lower-case set, so names stay short and valid.
# No EDNS0 OPT record, authority or additional section is generated.

import struct

def u16(n):
    return struct.pack('>H', n)

<start> ::= <query> | <response>

<query> ::= <id> <query_flags> b'\x00\x01' b'\x00\x00' b'\x00\x00' b'\x00\x00' <question>
<response> ::= <id> <response_flags> b'\x00\x01' <answers>

<answers> ::= <one_answer> | <two_answers> | <three_answers> | <four_answers>
<one_answer> ::= b'\x00\x01' b'\x00\x00' b'\x00\x00' <question> <rr>
<two_answers> ::= b'\x00\x02' b'\x00\x00' b'\x00\x00' <question> <rr> <rr>
<three_answers> ::= b'\x00\x03' b'\x00\x00' b'\x00\x00' <question> <rr> <rr> <rr>
<four_answers> ::= b'\x00\x04' b'\x00\x00' b'\x00\x00' <question> <rr> <rr> <rr> <rr>

<id> ::= <byte> <byte>
# QR=0, opcode 0 (QUERY), AA=0, TC=0, RD 0 or 1; RA=0, Z=0, RCODE 0.
<query_flags> ::= b'\x01\x00' | b'\x00\x00'
# QR=1, opcode 0, RD 1 or 0, RA 1 or 0, AA 0 or 1, RCODE 0 (NOERROR).
<response_flags> ::= b'\x81\x80' | b'\x85\x80' | b'\x81\x00' | b'\x80\x80'

<question> ::= <full_name> <qtype> <class_in>
<qtype> ::= b'\x00\x01' | b'\x00\x1c' | b'\x00\x05' | b'\x00\x0f' | b'\x00\x10'
<class_in> ::= b'\x00\x01'

<full_name> ::= <label>{1,3} b'\x00'
<label> ::= b'\x07example' | b'\x04test' | b'\x03www' | b'\x04mail' | b'\x02ns' | b'\x09parsarium'
<name> ::= <full_name> | b'\xc0\x0c'

<rr> ::= <name> (<rr_a> | <rr_aaaa> | <rr_cname> | <rr_mx> | <rr_txt>)
<ttl> ::= <byte> <byte> <byte> <byte>
<rr_a> ::= b'\x00\x01' <class_in> <ttl> b'\x00\x04' <byte>{4}
<rr_aaaa> ::= b'\x00\x1c' <class_in> <ttl> b'\x00\x10' <byte>{16}
<rr_cname> ::= b'\x00\x05' <class_in> <ttl> <rdlength> <cname_target>
<rr_mx> ::= b'\x00\x0f' <class_in> <ttl> <rdlength> <mx_rdata>
<rr_txt> ::= b'\x00\x10' <class_in> <ttl> <rdlength> <txt_rdata>
<cname_target> ::= <name>
<mx_rdata> ::= <byte> <byte> <name>
<txt_rdata> ::= <character_string>{1,3}
<character_string> ::= b'\x05hello' | b'\x09parsarium' | b'\x00' | b'\x03v=1'
<rdlength> ::= <byte> <byte>

where forall <r> in <rr_cname>: <r>.<rdlength> == u16(len(bytes(<r>.<cname_target>)))
where forall <r> in <rr_mx>: <r>.<rdlength> == u16(len(bytes(<r>.<mx_rdata>)))
where forall <r> in <rr_txt>: <r>.<rdlength> == u16(len(bytes(<r>.<txt_rdata>)))
