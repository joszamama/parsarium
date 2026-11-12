#include <KZip>
#include <KArchiveDirectory>
#include <KArchiveFile>
#include "../../c/zip/report.h"
#include <QByteArray>
#include <QString>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    KZip archive(QString::fromUtf8(argv[1]));
    if (!archive.open(QIODevice::ReadOnly)) return 1;
    const KArchiveDirectory *root = archive.directory();
    if (!root) return 1;
    const QStringList names = root->entries();
    if (names.empty()) return 1;
    const KArchiveFile *file = root->file(names[0]);
    if (!file) return 1;
    const QByteArray content = file->data();
    const QByteArray name = names[0].toUtf8();
    zip_report(names.size(), name.constData(),
               reinterpret_cast<const unsigned char *>(content.constData()), content.size());
    archive.close();
    return 0;
}
