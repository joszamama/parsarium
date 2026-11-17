#include <CoreFoundation/CoreFoundation.h>
#include <CoreGraphics/CoreGraphics.h>

#include <stdio.h>
#include <string.h>

/* Replay one local PDF through CGPDFDocumentCreateWithURL and print its page count. */
int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE.pdf\n", argv[0]);
        return 1;
    }
    CFURLRef url = CFURLCreateFromFileSystemRepresentation(
        kCFAllocatorDefault, (const UInt8 *)argv[1], (CFIndex)strlen(argv[1]), false);
    if (url == NULL) return 2;
    CGPDFDocumentRef document = CGPDFDocumentCreateWithURL(url);
    CFRelease(url);
    if (document == NULL) return 3;
    size_t pages = CGPDFDocumentGetNumberOfPages(document);
    CGPDFDocumentRelease(document);
    if (pages == 0) return 4;
    printf("{\"pages\":%zu}\n", pages);
    return 0;
}
