package org.parsarium;

import java.io.FileInputStream;
import org.la4j.io.MatrixMarketStream;
import org.la4j.matrix.Matrix;

public final class La4jMatrixMarketAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("local Matrix Market path required");
        Matrix matrix;
        try (FileInputStream input = new FileInputStream(args[0])) {
            matrix = new MatrixMarketStream(input).readMatrix();
        }
        int nonzero = 0;
        for (int row = 0; row < matrix.rows(); row++) {
            for (int col = 0; col < matrix.columns(); col++) {
                if (matrix.get(row, col) != 0.0) nonzero++;
            }
        }
        System.out.printf("{\"rows\":%d,\"cols\":%d,\"nnz\":%d,\"entry_1_3\":%.1f}%n",
                matrix.rows(), matrix.columns(), nonzero, matrix.get(0, 2));
    }
}
