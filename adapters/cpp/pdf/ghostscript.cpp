#include <ghostscript/iapi.h>

#include <iostream>
#include <string>

static int append_output(void* handle, const char* bytes, int length) {
    static_cast<std::string*>(handle)->append(bytes, length);
    return length;
}

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    std::string output;
    void* instance = nullptr;
    if (gsapi_new_instance(&instance, &output) != 0) return 2;
    if (gsapi_set_stdio(instance, nullptr, append_output, append_output) != 0) return 3;
    if (gsapi_add_control_path(instance, GS_PERMIT_FILE_READING, argv[1]) != 0) return 4;
    char program_name[] = "gs";
    char quiet[] = "-q";
    char no_display[] = "-dNODISPLAY";
    char* arguments[] = {program_name, quiet, no_display};
    if (gsapi_init_with_args(instance, 3, arguments) != 0) return 5;
    std::string escaped_path;
    for (const char* p = argv[1]; *p; ++p) {
        if (*p == '(' || *p == ')' || *p == '\\') escaped_path += '\\';
        escaped_path += *p;
    }
    const std::string program = "<<>> .PDFInit dup (" + escaped_path +
        ") exch .PDFFile dup .PDFInfo /NumPages get == .PDFClose";
    int exit_code = 0;
    const int status = gsapi_run_string(instance, program.c_str(), 0, &exit_code);
    const int shutdown = gsapi_exit(instance);
    gsapi_delete_instance(instance);
    if (status != 0 || exit_code != 0 || shutdown != 0) return 6;
    std::cout << "{\"pages\":" << std::stoi(output) << "}\n";
}
