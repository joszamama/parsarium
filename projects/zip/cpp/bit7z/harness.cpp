#include "harness.h"

#include <bit7z/bit7zlibrary.hpp>
#include <bit7z/bitarchivereader.hpp>
#include <bit7z/bitformat.hpp>

#include <cstdint>
#include <exception>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

// The SevenZip 26.04 shared library is built from source in the image and is
// also a DT_NEEDED dependency of the harness binaries, so its instrumentation
// is registered at process start. Bit7zLibrary's dlopen of the same path
// returns that already-loaded module.
#ifndef PARSARIUM_SEVENZIP_LIBRARY
#error "PARSARIUM_SEVENZIP_LIBRARY must name the pinned SevenZip 7z.so"
#endif

static const bit7z::Bit7zLibrary& sevenzip() {
  static const bit7z::Bit7zLibrary library{PARSARIUM_SEVENZIP_LIBRARY};
  return library;
}

// BitArchiveReader's documented local-file API takes a path, so the bytes are
// written to a private temporary directory first and removed afterwards.
static bool write_file(const std::string& path, const uint8_t* data, std::size_t size) {
  const int fd = open(path.c_str(), O_CREAT | O_EXCL | O_WRONLY, 0600);
  if (fd < 0) return false;
  bool written = true;
  for (std::size_t offset = 0; offset < size;) {
    const ssize_t count = write(fd, data + offset, size - offset);
    if (count <= 0) { written = false; break; }
    offset += static_cast<std::size_t>(count);
  }
  if (close(fd) != 0) written = false;
  return written;
}

static bool read_archive(const std::string& path, ParseResult& out) {
  bit7z::BitArchiveReader archive{sevenzip(), path, bit7z::BitFormat::Zip};
  const std::uint32_t count = archive.itemsCount();
  if (count == 0) {
    out = {};
    return true;
  }
  const bit7z::BitArchiveItemOffset item = archive.itemAt(0);
  // Bound decoded output. The declared size comes from the central directory.
  // SevenZip passes it to the decoder as an output limit except for entries
  // with a data descriptor (ZipHandler.cpp useUnpackLimit), where it decodes
  // to end of stream into bit7z's growing buffer. SevenZip reports unpacked
  // progress through bit7z's progress callback, and returning false aborts
  // the extraction. The abort lands at the decoder's next progress report
  // (Deflate: every 1 MiB of output), so the buffer can briefly exceed the cap
  // by one decoder step before the final size check below.
  if (item.size() > kMaxContentBytes) return false;
  archive.setProgressCallback([](std::uint64_t done) { return done <= kMaxContentBytes; });
  bit7z::buffer_t content;
  archive.extractTo(content, 0);
  if (content.size() > kMaxContentBytes) return false;
  out.entries = count;
  out.name = item.name();
  out.content.assign(reinterpret_cast<const char*>(content.data()), content.size());
  return true;
}

bool parse_zip(const uint8_t* data, std::size_t size, ParseResult& out) {
  if (!data || !size || size > kMaxInputBytes) return false;
  char directory[] = "/tmp/parsarium-bit7z-XXXXXX";
  if (!mkdtemp(directory)) return false;
  const std::string path = std::string(directory) + "/input.zip";
  bool ok = false;
  if (write_file(path, data, size)) {
    // bit7z reports open and extraction failures as BitException.
    try {
      ok = read_archive(path, out);
    } catch (const std::exception&) {
      ok = false;
    }
  }
  unlink(path.c_str());
  rmdir(directory);
  return ok;
}
