#include "harness.h"
#include <QByteArray>
#include <QImage>
#include <QPainter>
#include <QSvgRenderer>
#include <cstring>

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    QSvgRenderer renderer;
    if (!renderer.load(QByteArray(reinterpret_cast<const char *>(data), int(size))) || !renderer.isValid()) return 0;
    const QSize dimensions = renderer.defaultSize();
    if (dimensions.width() < 1 || dimensions.height() < 1 || dimensions.width() > 4096 || dimensions.height() > 4096) return 0;
    QImage image(dimensions, QImage::Format_RGBA8888);
    if (image.isNull()) return 0;
    image.fill(Qt::transparent);
    QPainter painter(&image);
    renderer.render(&painter);
    painter.end();
    const QColor first = image.pixelColor(0, 0);
    result->width = unsigned(dimensions.width());
    result->height = unsigned(dimensions.height());
    result->first[0] = first.red(); result->first[1] = first.green(); result->first[2] = first.blue();
    if (dimensions.width() > 1) {
        const QColor second = image.pixelColor(dimensions.width() - 1, 0);
        result->second_present = 1;
        result->second[0] = second.red(); result->second[1] = second.green(); result->second[2] = second.blue();
    }
    return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
