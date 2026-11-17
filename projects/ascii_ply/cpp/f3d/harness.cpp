#include "harness.h"

#include <engine.h>
#include <exception.h>
#include <log.h>
#include <scene.h>
#include <types.h>

#include <cstdlib>
#include <filesystem>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return false;
    // The native plugin is linked statically into libf3d; autoload registers
    // its readers, including PLYReader, with the reader factory.
    static const bool ready = [] {
        f3d::log::setVerboseLevel(f3d::log::VerboseLevel::QUIET);
        f3d::engine::autoloadPlugins();
        return true;
    }();
    (void)ready;
    // F3D selects the reader by file extension and then checks content.
    char path[] = "/tmp/parsarium-f3d-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) {
            close(fd);
            unlink(path);
            return false;
        }
        written += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) {
        unlink(path);
        return false;
    }

    bool loaded = false;
    try {
        f3d::engine engine = f3d::engine::createNone();
        f3d::scene &scene = engine.getScene();
        scene.add(std::filesystem::path(path));
        const f3d::scene_info_t info = scene.getSceneInfo();
        result->files = info.numberOfFiles;
        result->actors = info.numberOfActors;
        result->points = info.numberOfPoints;
        result->cells = info.numberOfCells;
        loaded = true;
    } catch (const f3d::exception &) {
        // scene::add reports unsupported content and reader failures as
        // load_failure_exception, a subclass of f3d::exception.
    }
    unlink(path);
    return loaded;
}
