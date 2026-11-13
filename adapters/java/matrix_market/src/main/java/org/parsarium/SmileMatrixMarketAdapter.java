package org.parsarium;

import java.nio.file.Path;
import smile.tensor.Matrix;
import smile.tensor.SparseMatrix;

public final class SmileMatrixMarketAdapter {
    private SmileMatrixMarketAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected local Matrix Market path");
        Matrix matrix = Matrix.market(Path.of(args[0]));
        if (!(matrix instanceof SparseMatrix sparse)) {
            throw new IllegalStateException("expected sparse coordinate matrix");
        }
        System.out.printf("{\"rows\":%d,\"cols\":%d,\"nnz\":%d,\"entry_1_3\":%.1f}%n",
                          sparse.nrow(), sparse.ncol(), sparse.length(), sparse.get(0, 2));
    }
}
