#include <tcl.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    Tcl_FindExecutable(argv[0]);
    Tcl_Interp *interp = Tcl_CreateInterp();
    if (!interp || Tcl_Init(interp) != TCL_OK) return 3;
    if (TclZipfs_Mount(interp, argv[1], "/parsarium", NULL) != TCL_OK) return 4;
    if (Tcl_Eval(interp, "glob -nocomplain //zipfs:/parsarium/*") != TCL_OK) return 5;
    Tcl_Size count = 0;
    Tcl_Obj **paths = NULL;
    if (Tcl_ListObjGetElements(interp, Tcl_GetObjResult(interp), &count, &paths) != TCL_OK || count < 1) return 6;
    const char *path_value = Tcl_GetString(paths[0]);
    char path[512];
    if (strlen(path_value) >= sizeof path) return 7;
    strcpy(path, path_value);
    const char *slash = strrchr(path, '/');
    if (!slash) return 8;
    Tcl_Channel channel = Tcl_OpenFileChannel(interp, path, "r", 0);
    if (!channel) return 9;
    unsigned char content[256];
    Tcl_Size length = Tcl_Read(channel, (char *)content, sizeof content);
    if (length < 0 || length == sizeof content) return 10;
    if (Tcl_Read(channel, (char *)content + length, 1) != 0) return 11;
    zip_report((size_t)count, slash + 1, content, (size_t)length);
    Tcl_Close(interp, channel);
    TclZipfs_Unmount(interp, argv[1]);
    Tcl_DeleteInterp(interp);
    Tcl_Finalize();
    return 0;
}
