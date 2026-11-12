#include <jasper/jasper.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2 || jas_init() != 0) return 2;
    jas_stream_t *stream = jas_stream_fopen(argv[1], "rb");
    if (!stream) return 3;
    jas_image_t *image = jas_image_decode(stream, -1, NULL);
    if (!image || jas_image_numcmpts(image) != 3) return 4;
    int first[3], second[3];
    for (unsigned channel = 0; channel < 3; ++channel) {
        first[channel] = jas_image_readcmptsample(image, channel, 0, 0);
        second[channel] = jas_image_readcmptsample(image, channel, 1, 0);
    }
    printf("{\"width\":%u,\"height\":%u,\"first\":[%d,%d,%d],\"second\":[%d,%d,%d]}\n",
           jas_image_width(image), jas_image_height(image),
           first[0], first[1], first[2], second[0], second[1], second[2]);
    jas_image_destroy(image);
    jas_stream_close(stream);
    jas_cleanup();
    return 0;
}
