#include "harness.h"

#include <karchivedirectory.h>
#include <karchivefile.h>
#include <kzip.h>
#include <kzipfileentry.h>

#include <QByteArray>
#include <QLoggingCategory>
#include <QString>
#include <QStringList>

#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

// KZip's documented local-file API takes a path, so the bytes are written to
// a private temporary directory first and removed after the archive closes.
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

static bool read_archive(const std::string& path, std::size_t input_size, ParseResult& out) {
  KZip archive(QString::fromLocal8Bit(path.data(), static_cast<qsizetype>(path.size())));
  if (!archive.open(QIODevice::ReadOnly)) return false;
  const KArchiveDirectory* root = archive.directory();
  if (!root) return false;
  QStringList names = root->entries();
  if (names.isEmpty()) {
    out.entries = 0;
    out.name.clear();
    out.content.clear();
    archive.close();
    return true;
  }
  // entries() follows QHash order; sorting keeps the reported entry stable.
  names.sort();
  const KArchiveFile* file = root->file(names.first());
  const auto* entry = dynamic_cast<const KZipFileEntry*>(file);
  if (!entry) return false;
  // Bound decoded output before KArchiveFile::data(). KZip takes sizes from
  // the central directory without checking them against the file, and
  // QIODevice::readAll allocates the device's declared size up front. A stored
  // entry is read through a device of compressedSize() bytes, so that size is
  // capped by the input length. A deflated entry stops at the declared size()
  // when it is nonzero but reads to end of stream when it is zero, so that
  // case is rejected. Other methods have no KZip decoder and data() would be
  // empty.
  const qint64 declared = entry->size();
  const qint64 compressed = entry->compressedSize();
  if (declared < 0 || declared > static_cast<qint64>(kMaxContentBytes)) return false;
  if (compressed < 0 || compressed > static_cast<qint64>(input_size)) return false;
  if (entry->encoding() != 0 && entry->encoding() != 8) return false;
  if (entry->encoding() == 8 && declared == 0 && compressed > 0) return false;
  const QByteArray content = file->data();
  if (content.size() > static_cast<qsizetype>(kMaxContentBytes)) return false;
  const QByteArray name = names.first().toUtf8();
  out.entries = static_cast<std::size_t>(names.size());
  out.name.assign(name.constData(), static_cast<std::size_t>(name.size()));
  out.content.assign(content.constData(), static_cast<std::size_t>(content.size()));
  archive.close();
  return true;
}

bool parse_zip(const uint8_t* data, std::size_t size, ParseResult& out) {
  if (!data || !size || size > kMaxInputBytes) return false;
  static const bool quiet = [] {
    // KArchive reports malformed archives through the kf.archive category.
    QLoggingCategory::setFilterRules(QStringLiteral("kf.archive*=false"));
    return true;
  }();
  (void)quiet;
  char directory[] = "/tmp/parsarium-karchive-XXXXXX";
  if (!mkdtemp(directory)) return false;
  const std::string path = std::string(directory) + "/input.zip";
  const bool ok = write_file(path, data, size) && read_archive(path, size, out);
  unlink(path.c_str());
  rmdir(directory);
  return ok;
}
