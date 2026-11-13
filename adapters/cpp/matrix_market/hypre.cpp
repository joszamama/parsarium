#include <mpi.h>
#include <HYPRE.h>
#include <HYPRE_IJ_mv.h>

#include <stdio.h>

int main(int argc, char **argv) {
    HYPRE_IJMatrix matrix = NULL;
    HYPRE_BigInt rows = 0, cols = 0, nonzeros = 0;
    HYPRE_BigInt row = 0, col = 2;
    HYPRE_Int one = 1;
    HYPRE_Complex value = 0;
    if (argc != 2 || MPI_Init(&argc, &argv) != MPI_SUCCESS) return 1;
    if (HYPRE_Init() != 0 ||
        HYPRE_IJMatrixReadMM(argv[1], MPI_COMM_SELF, HYPRE_PARCSR, &matrix) != 0 ||
        !matrix ||
        HYPRE_IJMatrixGetGlobalInfo(matrix, &rows, &cols, &nonzeros) != 0 ||
        HYPRE_IJMatrixGetValues(matrix, 1, &one, &row, &col, &value) != 0) {
        MPI_Finalize();
        return 2;
    }
    printf("{\"rows\":%lld,\"cols\":%lld,\"nnz\":%lld,\"entry_1_3\":%.10g}\n",
           (long long)rows, (long long)cols, (long long)nonzeros, (double)value);
    HYPRE_IJMatrixDestroy(matrix);
    HYPRE_Finalize();
    MPI_Finalize();
    return 0;
}
