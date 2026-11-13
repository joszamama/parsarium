#include <LAGraph.h>

#include <cstdio>

int main(int argc, char **argv) {
    char message[LAGRAPH_MSG_LEN] = {0};
    GrB_Matrix matrix = nullptr;
    GrB_Index rows = 0, cols = 0, nonzeros = 0;
    double value = 0;
    if (argc != 2 || LAGraph_Init(message) != GrB_SUCCESS) return 1;
    FILE *input = std::fopen(argv[1], "rb");
    if (!input) return 2;
    int status = LAGraph_MMRead(&matrix, input, message);
    std::fclose(input);
    if (status != GrB_SUCCESS || !matrix ||
        GrB_Matrix_nrows(&rows, matrix) != GrB_SUCCESS ||
        GrB_Matrix_ncols(&cols, matrix) != GrB_SUCCESS ||
        GrB_Matrix_nvals(&nonzeros, matrix) != GrB_SUCCESS ||
        GrB_Matrix_extractElement_FP64(&value, matrix, 0, 2) != GrB_SUCCESS) {
        std::fprintf(stderr, "%s\n", message);
        return 3;
    }
    std::printf("{\"rows\":%llu,\"cols\":%llu,\"nnz\":%llu,\"entry_1_3\":%.10g}\n",
                (unsigned long long)rows, (unsigned long long)cols,
                (unsigned long long)nonzeros, value);
    GrB_Matrix_free(&matrix);
    return LAGraph_Finalize(message) == GrB_SUCCESS ? 0 : 4;
}
