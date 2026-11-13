#include <math.h>
#include <stdio.h>
#include <string.h>
#define NANOSVG_IMPLEMENTATION
#include "nanosvg.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    NSVGimage *image = nsvgParseFromFile(argv[1], "px", 96.0f);
    if (image == NULL) return 1;
    int shapes = 0;
    int paths = 0;
    for (NSVGshape *shape = image->shapes; shape != NULL; shape = shape->next) {
        ++shapes;
        for (NSVGpath *path = shape->paths; path != NULL; path = path->next) {
            ++paths;
        }
    }
    printf("{\"width\":%.0f,\"height\":%.0f,\"shapes\":%d,\"paths\":%d}\n",
           image->width, image->height, shapes, paths);
    nsvgDelete(image);
    return 0;
}
