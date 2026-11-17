#include "harness.h"
#include <Poco/Exception.h>
#include <Poco/Zip/ZipArchive.h>
#include <Poco/Zip/ZipStream.h>

#include <iterator>
#include <sstream>
#include <string>

bool parse_zip(const uint8_t* data, std::size_t size, ParseResult& out) {
  if (!data || !size || size > kMaxInputBytes) return false;
  const std::string bytes(reinterpret_cast<const char*>(data), size);
  std::istringstream input(bytes, std::ios::in | std::ios::binary);
  try {
    Poco::Zip::ZipArchive archive(input);
    const auto first = archive.headerBegin();
    if (first == archive.headerEnd()) return false;
    const Poco::Zip::ZipLocalFileHeader& header = first->second;
    const std::string name = header.getFileName();
    if (name.size() > kMaxNameBytes) return false;
    input.clear();
    Poco::Zip::ZipInputStream decoded(input, header);
    std::string content;
    char chunk[4096];
    while (decoded.read(chunk, sizeof(chunk)) || decoded.gcount() > 0) {
      content.append(chunk, static_cast<std::size_t>(decoded.gcount()));
      if (content.size() > kMaxContentBytes) return false;
    }
    if (decoded.bad() || !decoded.crcValid()) return false;
    out.entries = static_cast<std::size_t>(
        std::distance(archive.headerBegin(), archive.headerEnd()));
    out.name = name;
    out.content = std::move(content);
    return true;
  } catch (const Poco::Exception&) {
    return false;
  } catch (const std::exception&) {
    return false;
  }
}
