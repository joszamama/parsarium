#include <boost/asio/buffer.hpp>
#include <boost/beast/http.hpp>

#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 1;
    const std::string bytes{std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>()};
    boost::beast::http::request_parser<boost::beast::http::empty_body> parser;
    boost::system::error_code error;
    const std::size_t consumed = parser.put(boost::asio::buffer(bytes), error);
    if (error || consumed != bytes.size() || !parser.is_done()) return 2;
    const auto& request = parser.get();
    std::cout << "{\"method\":\"" << request.method_string()
              << "\",\"path\":\"" << request.target()
              << "\",\"version\":\"" << request.version() / 10 << '.' << request.version() % 10
              << "\",\"host\":\"" << request[boost::beast::http::field::host] << "\"}\n";
}
