#define _GNU_SOURCE
#include "harness.h"
#include <netpbm/ppm.h>
#include <setjmp.h>
#include <stdio.h>

static void discard_error(const char *message) { (void)message; }

int parsarium_parse_pnm(const uint8_t *data, size_t size,
                       struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = (struct parsarium_pnm_result){0};
    FILE *file = fmemopen((void *)data, size, "rb");
    if (!file) return 0;
    static int initialized;
    if (!initialized) {
        pm_init("parsarium-netpbm", 0);
        pm_setusererrormsgfn(discard_error);
        initialized = 1;
    }
    pixel *volatile row = NULL;
    jmp_buf jump;
    int okay = 0;
    if (setjmp(jump) == 0) {
        pm_setjmpbuf(&jump);
        int cols, rows, format;
        pixval maxval;
        ppm_readppminit(file, &cols, &rows, &maxval, &format);
        /* A plain PPM pixel takes at least six bytes ("0 0 0 "), so this
           bound never rejects a valid input; it only caps the row buffer. */
        if (cols > 0 && rows > 0 && (size_t)cols * (size_t)rows <= size) {
            row = ppm_allocrow(cols);
            result->width = (size_t)cols;
            result->height = (size_t)rows;
            result->maxval = maxval;
            for (int y = 0; y < rows; ++y) {
                ppm_readppmrow(file, (pixel *)row, cols, maxval, format);
                /* The second pixel is the next one in raster order, if any. */
                if (y == 0) {
                    result->first[0] = PPM_GETR(row[0]);
                    result->first[1] = PPM_GETG(row[0]);
                    result->first[2] = PPM_GETB(row[0]);
                }
                if ((y == 0 && cols > 1) || (y == 1 && cols == 1)) {
                    int x = y == 0 ? 1 : 0;
                    result->has_second = 1;
                    result->second[0] = PPM_GETR(row[x]);
                    result->second[1] = PPM_GETG(row[x]);
                    result->second[2] = PPM_GETB(row[x]);
                }
            }
            okay = 1;
        }
    }
    pm_setjmpbuf(NULL);
    if (row) ppm_freerow((pixel *)row);
    fclose(file);
    return okay;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
