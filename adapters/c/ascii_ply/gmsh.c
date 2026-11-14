#include <gmshc.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int error = 0;
    gmshInitialize(0, NULL, 0, 0, &error);
    if (error) return 3;
    gmshOptionSetNumber("General.Terminal", 0, &error);
    gmshOpen(argv[1], &error);
    if (error) {
        gmshFinalize(&error);
        return 4;
    }

    size_t *node_tags = NULL, node_count = 0;
    double *coords = NULL, *parameters = NULL;
    size_t coord_count = 0, parameter_count = 0;
    gmshModelMeshGetNodes(&node_tags, &node_count, &coords, &coord_count,
                          &parameters, &parameter_count, -1, -1, 0, 0, &error);
    if (error || !coords || coord_count != 3 * node_count) return 5;

    size_t *triangle_tags = NULL, *triangle_nodes = NULL;
    size_t triangle_count = 0, triangle_node_count = 0;
    gmshModelMeshGetElementsByType(2, &triangle_tags, &triangle_count,
                                   &triangle_nodes, &triangle_node_count,
                                   -1, 0, 1, &error);
    if (error || triangle_node_count != 3 * triangle_count) return 6;

    double x_sum = 0.0;
    for (size_t i = 0; i < node_count; ++i) x_sum += coords[3 * i];
    printf("{\"vertices\":%zu,\"triangles\":%zu,\"triangle_nodes\":%zu,\"x_sum\":%.1f}\n",
           node_count, triangle_count, triangle_node_count, x_sum);

    gmshFree(node_tags);
    gmshFree(coords);
    gmshFree(parameters);
    gmshFree(triangle_tags);
    gmshFree(triangle_nodes);
    gmshFinalize(&error);
    return error ? 7 : 0;
}
