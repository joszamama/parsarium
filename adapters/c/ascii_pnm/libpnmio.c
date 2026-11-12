#include <pnmio.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    int width = 0, height = 0, maxval = 0, ascii = 0;
    int bytes = read_ppm_header(file, &width, &height, &maxval, &ascii);
    if (width != 2 || height != 1 || maxval != 255 || ascii != 1 || bytes != 6 * (int)sizeof(int)) {
        fclose(file);
        return 4;
    }
    int pixels[6] = {0};
    read_ppm_data(file, pixels, ascii);
    fclose(file);
    printf("{\"width\":%d,\"height\":%d,\"maxval\":%d,\"first\":[%d,%d,%d],\"second\":[%d,%d,%d]}\n",
           width, height, maxval, pixels[0], pixels[1], pixels[2],
           pixels[3], pixels[4], pixels[5]);
    return 0;
}
