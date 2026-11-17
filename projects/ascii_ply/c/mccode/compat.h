#ifndef PARSARIUM_MCCODE_COMPAT_H
#define PARSARIUM_MCCODE_COMPAT_H

/* McStas normally supplies these generic helpers in generated instrument C. */
#define _GNU_SOURCE
#include <float.h>
#include <math.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHAR_BUF_LENGTH 1024
#define MPI_MASTER(...) /* diagnostic output only */

typedef double MCNUM;
typedef struct { double x, y, z; } Coords;

static inline Coords coords_set(double x, double y, double z) {
    return (Coords){x, y, z};
}
static inline double scalar_prod(double ax, double ay, double az,
                                 double bx, double by, double bz) {
    return ax * bx + ay * by + az * bz;
}
static inline FILE *Open_File(char *name, char *mode, char *path) {
    (void)path;
    return fopen(name, mode);
}

/* The tagged file also contains drawing and trajectory code, unused here. */
static const int mcgravitation = 0;
static const int mcdotrace = 0;
static inline double rand01(void) { return 0.0; }
static inline void mcdis_polyhedron(const char *json) { (void)json; }
static inline void mcdis_line(double x1, double y1, double z1,
                              double x2, double y2, double z2) {
    (void)x1; (void)y1; (void)z1; (void)x2; (void)y2; (void)z2;
}

#endif
