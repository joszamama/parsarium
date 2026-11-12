#include <qarchivememoryextractor.hpp>
#include <qarchivememoryextractoroutput.hpp>
#include "../../c/zip/report.h"
#include <QCoreApplication>
#include <QJsonObject>
#include <QString>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    QCoreApplication app(argc, argv);
    QArchive::MemoryExtractor extractor(QString::fromUtf8(argv[1]));
    QObject::connect(&extractor, &QArchive::MemoryExtractor::finished,
                     [&](QArchive::MemoryExtractorOutput *output) {
        const auto &files = output->getFiles();
        if (files.empty()) { delete output; app.exit(1); return; }
        const QByteArray name = files[0].fileInformation().value("FileName").toString().toUtf8();
        const QByteArray content = files[0].buffer()->data();
        zip_report(files.size(), name.constData(),
                   reinterpret_cast<const unsigned char *>(content.constData()), content.size());
        delete output;
        app.exit(0);
    });
    QObject::connect(&extractor, &QArchive::MemoryExtractor::error,
                     [&](short) { app.exit(1); });
    extractor.start();
    return app.exec();
}
