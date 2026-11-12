/* Preincluded only while building libonion 0.8 on macOS. */
#include <alloca.h>
#include <strings.h>
#include <stdarg.h>
#include <stdio.h>
#include <syslog.h>

static inline void parsarium_vsyslog(int priority, const char *format, va_list args) {
    char buffer[2048];
    vsnprintf(buffer, sizeof buffer, format, args);
    syslog(priority, "%s", buffer);
}
#define vsyslog parsarium_vsyslog
