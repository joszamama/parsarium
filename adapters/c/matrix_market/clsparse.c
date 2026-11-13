#include "clSPARSE.h"
#include <stdio.h>
#include <stdlib.h>

#define CHECK(x) do { int e_ = (int)(x); if (e_ != 0) { fprintf(stderr, "%s: %d\n", #x, e_); return 1; } } while (0)
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    cl_platform_id platform;
    cl_device_id device;
    cl_int err;
    CHECK(clGetPlatformIDs(1, &platform, NULL));
    CHECK(clGetDeviceIDs(platform, CL_DEVICE_TYPE_ALL, 1, &device, NULL));
    cl_context context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    CHECK(err);
    cl_command_queue queue = clCreateCommandQueue(context, device, 0, &err);
    CHECK(err);
    CHECK(clsparseSetup());
    clsparseCreateResult cr = clsparseCreateControl(queue);
    CHECK(cr.status);
    clsparseIdx_t nnz=0, rows=0, cols=0;
    CHECK(clsparseHeaderfromFile(&nnz, &rows, &cols, argv[1]));
    clsparseCooMatrix matrix;
    CHECK(clsparseInitCooMatrix(&matrix));
    matrix.values = clCreateBuffer(context, CL_MEM_READ_WRITE, nnz * sizeof(cl_float), NULL, &err); CHECK(err);
    matrix.row_indices = clCreateBuffer(context, CL_MEM_READ_WRITE, nnz * sizeof(clsparseIdx_t), NULL, &err); CHECK(err);
    matrix.col_indices = clCreateBuffer(context, CL_MEM_READ_WRITE, nnz * sizeof(clsparseIdx_t), NULL, &err); CHECK(err);
    CHECK(clsparseSCooMatrixfromFile(&matrix, argv[1], cr.control, CL_TRUE));
    float values[3]; clsparseIdx_t row[3], col[3];
    if (matrix.num_nonzeros != 3) return 3;
    CHECK(clEnqueueReadBuffer(queue, matrix.values, CL_TRUE, 0, 3*sizeof(float), values, 0, NULL, NULL));
    CHECK(clEnqueueReadBuffer(queue, matrix.row_indices, CL_TRUE, 0, 3*sizeof(clsparseIdx_t), row, 0, NULL, NULL));
    CHECK(clEnqueueReadBuffer(queue, matrix.col_indices, CL_TRUE, 0, 3*sizeof(clsparseIdx_t), col, 0, NULL, NULL));
    printf("{\"rows\":%u,\"cols\":%u,\"nnz\":%u,\"row\":[%u,%u,%u],\"col\":[%u,%u,%u],\"value\":[%g,%g,%g]}\n", (unsigned)matrix.num_rows, (unsigned)matrix.num_cols, (unsigned)matrix.num_nonzeros, (unsigned)row[0], (unsigned)row[1], (unsigned)row[2], (unsigned)col[0], (unsigned)col[1], (unsigned)col[2], values[0], values[1], values[2]);
    clReleaseMemObject(matrix.values); clReleaseMemObject(matrix.row_indices); clReleaseMemObject(matrix.col_indices);
    CHECK(clsparseReleaseControl(cr.control)); CHECK(clsparseTeardown());
    clReleaseCommandQueue(queue); clReleaseContext(context);
    return 0;
}
