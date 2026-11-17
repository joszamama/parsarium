#include "harness.h"
#include <pdfdocumentreader.h>
#include <QCoreApplication>
#include <QByteArray>
#include <QString>

static void ensure_qt() {
    static int argc = 1;
    static char name[] = "parsarium";
    static char *argv[] = {name, nullptr};
    static QCoreApplication app(argc, argv);
    (void)app;
}

static bool count_pages(pdf::PDFDocumentReader &reader,
                        pdf::PDFDocument &document, std::size_t &pages) {
    if (reader.getReadingResult() != pdf::PDFDocumentReader::Result::OK) return false;
    const auto *catalog = document.getCatalog();
    if (!catalog) return false;
    pages = catalog->getPageCount();
    return pages > 0;
}

static pdf::PDFDocumentReader new_reader() {
    return pdf::PDFDocumentReader(nullptr, [](bool *ok) {
        *ok = false;
        return QString();
    }, false, false);
}

bool parsarium_parse_pdf_file(const char *path, std::size_t &pages) {
    if (!path) return false;
    ensure_qt();
    auto reader = new_reader();
    auto document = reader.readFromFile(QString::fromUtf8(path));
    return count_pages(reader, document, pages);
}

bool parsarium_parse_pdf_bytes(const std::uint8_t *data, std::size_t size, std::size_t &pages) {
    if (!data || size == 0 || size > (1u << 20)) return false;
    ensure_qt();
    auto reader = new_reader();
    auto bytes = QByteArray(reinterpret_cast<const char *>(data), static_cast<qsizetype>(size));
    auto document = reader.readFromBuffer(bytes);
    return count_pages(reader, document, pages);
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    std::size_t pages = 0;
    (void)parsarium_parse_pdf_bytes(data, size, pages);
    return 0;
}
