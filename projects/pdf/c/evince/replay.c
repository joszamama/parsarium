#include "harness.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int pages = 0;
    if (!parsarium_parse_pdf_file(argv[1], &pages)) return 1;
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
