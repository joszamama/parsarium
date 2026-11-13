package org.parsarium;

import graphtea.extensions.io.MM;
import Jama.Matrix;
import java.io.File;

public final class GraphTeaMatrixMarketAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local Matrix Market file path");
        }
        Matrix matrix = MM.loadMatrixFromSPARSE(new File(args[0]));
        System.out.printf("{\"rows\":%d,\"cols\":%d,\"value_0_2\":%.1f}%n",
                matrix.getRowDimension(), matrix.getColumnDimension(), matrix.get(0, 2));
    }
}
