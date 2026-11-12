#include <quazip.h>
#include <quazipfile.h>
#include "../../c/zip/report.h"
#include <QByteArray>
#include <QString>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    QuaZip archive(QString::fromUtf8(argv[1]));
    if (!archive.open(QuaZip::mdUnzip)) return 1;
    const QStringList names = archive.getFileNameList();
    if (names.empty() || !archive.setCurrentFile(names[0])) return 1;
    QuaZipFile file(&archive);
    if (!file.open(QIODevice::ReadOnly)) return 1;
    const QByteArray content = file.readAll();
    const QByteArray name = names[0].toUtf8();
    zip_report(names.size(), name.constData(),
               reinterpret_cast<const unsigned char *>(content.constData()), content.size());
    file.close();
    archive.close();
    return 0;
}
