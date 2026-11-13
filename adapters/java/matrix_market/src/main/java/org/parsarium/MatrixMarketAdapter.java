package org.parsarium;

import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import org.ejml.data.DMatrixSparseTriplet;
import org.ejml.ops.MatrixIO;

public final class MatrixMarketAdapter {
    private MatrixMarketAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected one local Matrix Market path");
        }
        try (Reader reader = Files.newBufferedReader(Path.of(args[0]), StandardCharsets.US_ASCII)) {
            DMatrixSparseTriplet matrix = MatrixIO.loadMatrixMarketDSTR(reader);
            if (matrix == null) {
                throw new IllegalStateException("EJML did not produce a matrix");
            }
            System.out.printf(
                "{\"rows\":%d,\"cols\":%d,\"nnz\":%d,\"entry_1_3\":%.1f}%n",
                matrix.numRows, matrix.numCols, matrix.nz_length, matrix.get(0, 2));
        }
    }
}
