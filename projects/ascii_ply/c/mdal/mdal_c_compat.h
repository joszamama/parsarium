/* MDAL 1.3.3 exports these C ABI functions. Its published mdal.h uses C++
 * enum type names and bool without C typedefs, so it does not compile as C11. */
#ifndef PARSARIUM_MDAL_C_COMPAT_H
#define PARSARIUM_MDAL_C_COMPAT_H

typedef void *MDAL_MeshH;
typedef void *MDAL_MeshFaceIteratorH;
/* MDAL_LogLevel and MDAL_Status are plain C++ enums (int-sized). */
typedef void (*MDAL_LoggerCallback)(int logLevel, int status, const char *message);

void MDAL_SetLoggerCallback(MDAL_LoggerCallback callback);

MDAL_MeshH MDAL_LoadMesh(const char *uri);
void MDAL_CloseMesh(MDAL_MeshH mesh);
const char *MDAL_M_driverName(MDAL_MeshH mesh);
int MDAL_M_vertexCount(MDAL_MeshH mesh);
int MDAL_M_faceCount(MDAL_MeshH mesh);
int MDAL_M_faceVerticesMaximumCount(MDAL_MeshH mesh);
MDAL_MeshFaceIteratorH MDAL_M_faceIterator(MDAL_MeshH mesh);
int MDAL_FI_next(MDAL_MeshFaceIteratorH iterator,
                 int faceOffsetsBufferLen, int *faceOffsetsBuffer,
                 int vertexIndicesBufferLen, int *vertexIndicesBuffer);
void MDAL_FI_close(MDAL_MeshFaceIteratorH iterator);

#endif
