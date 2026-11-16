#include "harness.h"

#include <vtkCellArray.h>
#include <vtkIdList.h>
#include <vtkNew.h>
#include <vtkObject.h>
#include <vtkPLYReader.h>
#include <vtkPolyData.h>

#include <cstdlib>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return false;
    static const bool quiet = [] {
        vtkObject::GlobalWarningDisplayOff();
        return true;
    }();
    (void)quiet;
    char path[] = "/tmp/parsarium-vtk-XXXXXX.ply";
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

    vtkNew<vtkPLYReader> reader;
    reader->SetFileName(path);
    reader->Update();
    unlink(path);
    // vtkPLYReader leaves the output without points when the header or the
    // vertex x/y/z properties cannot be read.
    vtkPolyData *mesh = reader->GetOutput();
    if (!mesh || !mesh->GetPoints()) return false;
    result->vertices = mesh->GetNumberOfPoints();
    result->faces = mesh->GetNumberOfPolys();
    result->face.clear();
    if (result->faces != 0) {
        vtkNew<vtkIdList> ids;
        mesh->GetPolys()->GetCellAtId(0, ids);
        for (vtkIdType i = 0; i < ids->GetNumberOfIds(); ++i)
            result->face.push_back(ids->GetId(i));
    }
    return true;
}
