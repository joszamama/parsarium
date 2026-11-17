// Local DNS message bytes reach libtins' documented Tins::DNS(const uint8_t*, uint32_t)
// constructor; the summary is read through its header, query and resource getters.
// libtins is built without libpcap; no socket or capture is opened.
#include <tins/dns.h>

#include <algorithm>
#include <cctype>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::string absolute(std::string name) {
    std::transform(name.begin(), name.end(), name.begin(),
                   [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    if (name.empty() || name.back() != '.') name += '.';
    return name;
}

std::string quote(const std::string& value) {
    std::string out = "\"";
    for (char c : value) {
        if (c == '"' || c == '\\') out += '\\';
        out += c;
    }
    return out + "\"";
}

std::string rdata(const Tins::DNS::resource& record) {
    switch (record.query_type()) {
    case Tins::DNS::A:
    case Tins::DNS::AAAA:
        return record.data();  // libtins IPv4Address/IPv6Address text
    case Tins::DNS::CNAME:
    case Tins::DNS::NS:
    case Tins::DNS::PTR:
        return absolute(record.data());
    case Tins::DNS::MX:
        return std::to_string(record.preference()) + " " + absolute(record.data());
    default:
        throw std::runtime_error("record type outside the control subset");
    }
}

std::string records(const Tins::DNS::resources_type& list) {
    std::ostringstream out;
    out << '[';
    for (std::size_t i = 0; i < list.size(); ++i) {
        const auto& record = list[i];
        out << (i ? "," : "") << "{\"name\":" << quote(absolute(record.dname()))
            << ",\"type\":" << record.query_type() << ",\"class\":" << record.query_class()
            << ",\"ttl\":" << record.ttl() << ",\"rdata\":" << quote(rdata(record)) << '}';
    }
    out << ']';
    return out.str();
}

std::string summarize(const uint8_t* data, std::size_t size) {
    if (!data || size == 0 || size > 65535) throw std::runtime_error("input outside harness limit");
    Tins::DNS dns(data, static_cast<uint32_t>(size));
    const auto queries = dns.queries();
    const auto answers = dns.answers();
    const auto authority = dns.authority();
    const auto additional = dns.additional();
    std::ostringstream out;
    out << "{\"id\":" << dns.id() << ",\"qr\":" << (dns.type() == Tins::DNS::RESPONSE ? 1 : 0)
        << ",\"opcode\":" << int(dns.opcode()) << ",\"aa\":" << int(dns.authoritative_answer())
        << ",\"tc\":" << int(dns.truncated()) << ",\"rd\":" << int(dns.recursion_desired())
        << ",\"ra\":" << int(dns.recursion_available())
        << ",\"z\":" << ((int(dns.z()) << 2) | (int(dns.authenticated_data()) << 1) | int(dns.checking_disabled()))
        << ",\"rcode\":" << int(dns.rcode()) << ",\"qdcount\":" << queries.size()
        << ",\"ancount\":" << answers.size() << ",\"nscount\":" << authority.size()
        << ",\"arcount\":" << additional.size() << ",\"questions\":[";
    for (std::size_t i = 0; i < queries.size(); ++i) {
        out << (i ? "," : "") << "{\"name\":" << quote(absolute(queries[i].dname()))
            << ",\"type\":" << int(queries[i].query_type()) << ",\"class\":" << int(queries[i].query_class()) << '}';
    }
    out << "],\"answers\":" << records(answers) << ",\"authority\":" << records(authority)
        << ",\"additional\":" << records(additional) << '}';
    return out.str();
}

}  // namespace

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, std::size_t size) {
    try { summarize(data, size); } catch (const std::exception&) {}
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 3;
    std::vector<uint8_t> data((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    try {
        std::puts(summarize(data.data(), data.size()).c_str());
    } catch (const std::exception& error) {
        std::fprintf(stderr, "%s\n", error.what());
        return 5;
    }
    return 0;
}
#endif
