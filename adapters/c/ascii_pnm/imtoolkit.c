#include <im.h>
#include <im_image.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int error = 0;
    imImage *image = imFileImageLoad(argv[1], 0, &error);
    if (!image || error != IM_ERR_NONE) return 3;
    if (image->width != 2 || image->height != 1 || image->depth != 3 ||
        image->data_type != IM_BYTE || image->color_space != IM_RGB) {
        imImageDestroy(image);
        return 4;
    }
    unsigned char *r = image->data[0];
    unsigned char *g = image->data[1];
    unsigned char *b = image->data[2];
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           image->width, image->height, r[0], g[0], b[0], r[1], g[1], b[1]);
    imImageDestroy(image);
    return 0;
}
