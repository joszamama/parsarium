#include "harness.h"

#include <ghostscript/iapi.h>

#include <unistd.h>

#include <cerrno>
#include <climits>
#include <cstdlib>
#include <string>

namespace {

constexpr std::size_t max_input = 8u << 20;

// Same callback as adapters/cpp/pdf/ghostscript.cpp: stdout and stderr share one buffer.
int append_output(void *handle, const char *bytes, int length) {
    if (length > 0) static_cast<std::string *>(handle)->append(bytes, static_cast<std::size_t>(length));
    return length;
}

std::string escape_postscript_string(const std::string &path) {
    std::string escaped;
    for (char c : path) {
        if (c == '(' || c == ')' || c == '\\') escaped += '\\';
        escaped += c;
    }
    return escaped;
}

// The adapter prints `NumPages ==`; accept only that exact text so stray
// interpreter output is never mistaken for a page count.
bool read_pages(const std::string &output, int &pages) {
    if (output.size() < 2 || output.back() != '\n') return false;
    const std::string digits = output.substr(0, output.size() - 1);
    if (digits.find_first_not_of("0123456789") != std::string::npos) return false;
    errno = 0;
    char *end = nullptr;
    const long value = std::strtol(digits.c_str(), &end, 10);
    if (errno || *end || value > INT_MAX) return false;
    pages = static_cast<int>(value);
    return true;
}

class TempFile {
public:
    TempFile(const std::uint8_t *data, std::size_t size) {
        int fd = mkstemps(path_, 4);
        if (fd < 0) return;
        std::size_t offset = 0;
        while (offset < size) {
            const ssize_t n = write(fd, data + offset, size - offset);
            if (n <= 0) break;
            offset += static_cast<std::size_t>(n);
        }
        written_ = close(fd) == 0 && offset == size;
        created_ = true;
    }
    ~TempFile() { if (created_) unlink(path_); }
    TempFile(const TempFile &) = delete;
    TempFile &operator=(const TempFile &) = delete;
    bool ok() const { return created_ && written_; }
    const char *path() const { return path_; }

private:
    char path_[32] = "/tmp/parsarium-XXXXXX.pdf";
    bool created_ = false;
    bool written_ = false;
};

class Instance {
public:
    explicit Instance(std::string &output) {
        if (gsapi_new_instance(&handle_, &output) != 0) handle_ = nullptr;
    }
    ~Instance() {
        if (!handle_) return;
        if (initialised_) gsapi_exit(handle_);
        gsapi_delete_instance(handle_);
    }
    Instance(const Instance &) = delete;
    Instance &operator=(const Instance &) = delete;
    void *get() const { return handle_; }
    void mark_initialised() { initialised_ = true; }
    int exit() {
        initialised_ = false;
        return gsapi_exit(handle_);
    }

private:
    void *handle_ = nullptr;
    bool initialised_ = false;
};

}  // namespace

bool parse_data(const std::uint8_t *data, std::size_t size, Result &result) {
    result = Result{};
    if (!data || !size || size > max_input) return false;
    TempFile file(data, size);
    if (!file.ok()) return false;

    // Call sequence and PostScript program match adapters/cpp/pdf/ghostscript.cpp.
    std::string output;
    Instance instance(output);
    if (!instance.get()) return false;
    if (gsapi_set_stdio(instance.get(), nullptr, append_output, append_output) != 0) return false;
    if (gsapi_add_control_path(instance.get(), GS_PERMIT_FILE_READING, file.path()) != 0) return false;
    char program_name[] = "gs";
    char quiet[] = "-q";
    char no_display[] = "-dNODISPLAY";
    char *arguments[] = {program_name, quiet, no_display};
    const int init = gsapi_init_with_args(instance.get(), 3, arguments);
    instance.mark_initialised();
    if (init != 0) return false;
    const std::string program = "<<>> .PDFInit dup (" + escape_postscript_string(file.path()) +
        ") exch .PDFFile dup .PDFInfo /NumPages get == .PDFClose";
    int exit_code = 0;
    const int status = gsapi_run_string(instance.get(), program.c_str(), 0, &exit_code);
    const int shutdown = instance.exit();
    if (status != 0 || exit_code != 0 || shutdown != 0) return false;
    int pages = 0;
    if (!read_pages(output, pages)) return false;
    result.pages = pages;
    return true;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result;
    (void)parse_data(data, size, result);
    return 0;
}
