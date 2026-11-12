#include <Poco/Net/HTTPRequest.h>

#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 1;
    Poco::Net::HTTPRequest request;
    request.read(file);
    const std::string version = request.getVersion();
    if (version.rfind("HTTP/", 0) != 0) return 2;
    std::cout << "{\"method\":\"" << request.getMethod()
              << "\",\"path\":\"" << request.getURI()
              << "\",\"version\":\"" << version.substr(5)
              << "\",\"host\":\"" << request.getHost() << "\"}\n";
}
