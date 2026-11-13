#include <vtkCell.h>
#include <vtkNew.h>
#include <vtkPLYReader.h>
#include <vtkPolyData.h>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  vtkNew<vtkPLYReader> reader;
  reader->SetFileName(argv[1]);
  reader->Update();
  vtkPolyData *mesh = reader->GetOutput();
  if (!mesh || mesh->GetNumberOfPoints() != 3 || mesh->GetNumberOfPolys() != 1)
    return 1;
  vtkCell *face = mesh->GetCell(0);
  if (!face || face->GetNumberOfPoints() != 3) return 1;
  std::printf("{\"vertices\":%lld,\"faces\":%lld,\"face\":[%lld,%lld,%lld]}\n",
              static_cast<long long>(mesh->GetNumberOfPoints()),
              static_cast<long long>(mesh->GetNumberOfPolys()),
              static_cast<long long>(face->GetPointId(0)),
              static_cast<long long>(face->GetPointId(1)),
              static_cast<long long>(face->GetPointId(2)));
  return 0;
}
