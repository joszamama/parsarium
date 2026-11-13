#include <meshioplusplus/formats/ply.hpp>

#include <cstdint>
#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    const auto mesh = meshioplusplus::read_ply(argv[1]);
    for (const auto block : mesh.CellRange()) {
        if (block.Type() != "triangle" || block.NumCells() != 1 ||
            block.NodesPerCell() != 3 || block.Conn().Dtype() != meshioplusplus::DType::Int64)
            continue;
        const std::int64_t* face = block.Conn().As<std::int64_t>();
        std::cout << "{\"vertices\":" << mesh.NumPoints()
                  << ",\"faces\":" << block.NumCells()
                  << ",\"face\":[" << face[0] << ',' << face[1] << ',' << face[2]
                  << "]}\n";
        return 0;
    }
    return 3;
}
