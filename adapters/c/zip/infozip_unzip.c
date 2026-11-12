#include "unzip.h"
#include "report.h"
#include <stdio.h>
#include <string.h>

static unsigned char listing[4096];
static size_t listing_length;

static int capture(zvoid *context, uch *bytes, ulg length, int flags) {
    (void) context;
    (void) flags;
    if (length > sizeof(listing) - listing_length) return 1;
    memcpy(listing + listing_length, bytes, length);
    listing_length += length;
    return 0;
}

static int discard(zvoid *context, uch *bytes, ulg length, int flags) {
    (void) context;
    (void) bytes;
    (void) length;
    (void) flags;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    UzpInit init = {0};
    init.structlen = sizeof(init);
    init.msgfn = capture;
    char program[] = "unzip";
    char zipinfo[] = "-Z";
    char names_only[] = "-1";
    char *arguments[] = {program, zipinfo, names_only, argv[1]};
    if (UzpAltMain(4, arguments, &init) != 0) return 3;
    if (!listing_length || listing[listing_length - 1] != '\n') return 4;
    size_t entries = 0;
    for (size_t i = 0; i < listing_length; ++i) {
        if (listing[i] == '\n') {
            ++entries;
            if (entries == 1) listing[i] = 0;
        }
    }
    if (entries != 1 || !listing[0]) return 5;
    UzpOpts options = {0};
    UzpCB callbacks = {0};
    callbacks.structlen = sizeof(callbacks);
    callbacks.msgfn = discard;
    UzpBuffer result = {0};
    if (!UzpUnzipToMemory(argv[1], (char *) listing, &options, &callbacks, &result)) return 6;
    zip_report(entries, (const char *) listing,
               (const unsigned char *) result.strptr, result.strlength);
    UzpFreeMemBuffer(&result);
    return 0;
}
