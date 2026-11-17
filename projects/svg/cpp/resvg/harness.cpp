#include "harness.h"
#include "resvg.h"
#include <cmath>
#include <cstdlib>
#include <memory>
#include <vector>
#include <unistd.h>

namespace {

constexpr std::size_t kMaxInput = 1u << 20;
constexpr std::size_t kMaxPixels = 4096u * 4096u;

struct OptionsDeleter { void operator()(resvg_options *p) const { resvg_options_destroy(p); } };
struct TreeDeleter { void operator()(resvg_render_tree *p) const { resvg_tree_destroy(p); } };

// The selected C API takes a local SVG path, so the bytes are written to a
// private temporary file that is removed when this object goes out of scope.
class LocalFile {
public:
    LocalFile(const std::uint8_t *data, std::size_t size) {
        int fd = mkstemps(path_, 4);
        if (fd < 0) return;
        created_ = true;
        std::size_t offset = 0;
        while (offset < size) {
            ssize_t n = write(fd, data + offset, size - offset);
            if (n <= 0) { close(fd); return; }
            offset += static_cast<std::size_t>(n);
        }
        ok_ = close(fd) == 0;
    }
    ~LocalFile() { if (created_) unlink(path_); }
    LocalFile(const LocalFile &) = delete;
    LocalFile &operator=(const LocalFile &) = delete;
    bool ok() const { return ok_; }
    const char *path() const { return path_; }

private:
    char path_[32] = "/tmp/parsarium-resvg-XXXXXX.svg";
    bool created_ = false, ok_ = false;
};

}  // namespace

bool parsarium_parse_svg(const std::uint8_t *data, std::size_t size, parsarium_svg_result &result) {
    result = parsarium_svg_result{};
    if (!data || !size || size > kMaxInput) return false;
    LocalFile file(data, size);
    if (!file.ok()) return false;

    std::unique_ptr<resvg_options, OptionsDeleter> options(resvg_options_create());
    if (!options) return false;
    resvg_render_tree *raw = nullptr;
    int32_t status = resvg_parse_tree_from_file(file.path(), options.get(), &raw);
    std::unique_ptr<resvg_render_tree, TreeDeleter> tree(raw);
    if (status != RESVG_OK || !tree) return false;

    resvg_size dimensions = resvg_get_image_size(tree.get());
    if (!std::isfinite(dimensions.width) || !std::isfinite(dimensions.height) ||
        dimensions.width <= 0 || dimensions.height <= 0 ||
        dimensions.width > 4096 || dimensions.height > 4096) return false;
    auto width = static_cast<unsigned>(std::ceil(dimensions.width));
    auto height = static_cast<unsigned>(std::ceil(dimensions.height));
    std::size_t pixels = static_cast<std::size_t>(width) * height;
    if (!width || !height || pixels > kMaxPixels) return false;

    std::vector<unsigned char> rgba(pixels * 4);
    resvg_render(tree.get(), resvg_transform_identity(), width, height,
                 reinterpret_cast<char *>(rgba.data()));
    result.width = width;
    result.height = height;
    result.first = {rgba[0], rgba[1], rgba[2]};
    if (pixels > 1) result.second = std::array<unsigned char, 3>{rgba[4], rgba[5], rgba[6]};
    return true;
}
