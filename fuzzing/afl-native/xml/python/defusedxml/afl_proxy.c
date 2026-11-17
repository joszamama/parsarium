#define _POSIX_C_SOURCE 200809L

#include <dlfcn.h>
#include <stdint.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

/* The classic AFL++ compiler mode reserves the full 64 KiB map. The child
 * tracer writes one parser-source feature per line; wrapper coverage is
 * incidental, while these entries are input-dependent parser feedback. */
static uint32_t feature_hash(const char *value) {
    uint32_t hash = 2166136261u;
    for (; *value; ++value) {
        hash ^= (unsigned char)*value;
        hash *= 16777619u;
    }
    return hash;
}

extern void parsarium_afl_start(void);

int main(int argc, char **argv) {
    parsarium_afl_start();
    if (argc != 2) return 2;
    char result[] = "/tmp/parsarium-afl-features-XXXXXX";
    int descriptor = mkstemp(result);
    if (descriptor < 0) return 2;
    close(descriptor);

    pid_t child = fork();
    if (child < 0) {
        unlink(result);
        return 2;
    }
    if (child == 0) {
        execl("/bin/sh", "/bin/sh", "/work/afl_trace", argv[1], result, (char *)NULL);
        _exit(127);
    }
    int status;
    if (waitpid(child, &status, 0) < 0) {
        unlink(result);
        return 2;
    }
    FILE *features = fopen(result, "r");
    if (!features) {
        unlink(result);
        return 2;
    }
    unsigned char **area = (unsigned char **)dlsym(RTLD_DEFAULT, "__afl_area_ptr");
    if (!area || !*area) {
        fclose(features);
        unlink(result);
        return 3;
    }
    char feature[4096];
    while (fgets(feature, sizeof(feature), features)) {
        feature[strcspn(feature, "\r\n")] = '\0';
        if (*feature) ++(*area)[feature_hash(feature) & 65535u];
    }
    fclose(features);
    unlink(result);
    if (!WIFEXITED(status)) {
        raise(SIGABRT);
    } else if (WEXITSTATUS(status) != 0) {
        raise(SIGABRT);
    }
    return 0;
}
