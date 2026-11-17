/* AFL_PRELOAD shim: constant getrandom(2) bytes so std HashMap RandomState keys repeat
 * across target processes. Parser code is not modified; only its hash seed is fixed. */
#include <stddef.h>
#include <sys/types.h>

ssize_t getrandom(void *buf, size_t len, unsigned int flags) {
    unsigned char *out = buf;
    (void)flags;
    for (size_t i = 0; i < len; i++) out[i] = (unsigned char)(0x5a ^ i);
    return (ssize_t)len;
}
