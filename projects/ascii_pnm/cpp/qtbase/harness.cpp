#include "harness.h"
#include <QColor>
#include <QImage>
#include <QImageReader>
#include <QString>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

static void store(const QColor &color, unsigned char out[4]) {
    out[0] = color.red(); out[1] = color.green(); out[2] = color.blue(); out[3] = color.alpha();
}

int parsarium_parse_ascii_pnm(const uint8_t *data, size_t size, struct parsarium_ascii_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += size_t(n);
    }
    close(fd);
    QImage image;
    {
        // Force QtBase's built-in QPpmHandler; never fall back to content sniffing.
        QImageReader reader(QString::fromLocal8Bit(path), "ppm");
        reader.setAutoDetectImageFormat(false);
        reader.setAllocationLimit(64);
        image = reader.read();
    }
    unlink(path);
    if (image.isNull() || image.width() < 1 || image.height() < 1) return 0;
    result->width = unsigned(image.width());
    result->height = unsigned(image.height());
    store(image.pixelColor(0, 0), result->first);
    if (image.width() > 1) {
        result->second_present = 1;
        store(image.pixelColor(1, 0), result->second);
    }
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ascii_pnm_result result;
    (void)parsarium_parse_ascii_pnm(data, size, &result);
    return 0;
}
