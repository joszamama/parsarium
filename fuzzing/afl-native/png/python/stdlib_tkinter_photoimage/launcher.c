/* Supply AFL++'s runtime from the executable while running pinned CPython.
 * Tk is a shared library; its decoder probes resolve through this executable.
 * Compile this launcher with plain clang so only tkImgPNG.c adds feedback. */
extern int Py_BytesMain(int argc, char **argv);

int main(int argc, char **argv) {
    return Py_BytesMain(argc, argv);
}
