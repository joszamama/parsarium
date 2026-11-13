package org.parsarium;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import cern.colt.matrix.io.MatrixInfo;
import cern.colt.matrix.io.MatrixSize;
import cern.colt.matrix.io.MatrixVectorReader;

public final class ParallelColtMatrixMarketAdapter {
    private ParallelColtMatrixMarketAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected one local Matrix Market path");
        }
        try (MatrixVectorReader reader = new MatrixVectorReader(
                Files.newBufferedReader(Path.of(args[0]), StandardCharsets.US_ASCII))) {
            MatrixInfo info = reader.readMatrixInfo();
            reader.readComments();
            MatrixSize size = reader.readMatrixSize(info);
            int entries = size.numEntries();
            int[] rows = new int[entries];
            int[] columns = new int[entries];
            double[] values = new double[entries];
            reader.readCoordinate(rows, columns, values);
            double entry = 0.0;
            for (int i = 0; i < entries; i++) {
                if (rows[i] == 0 && columns[i] == 2) {
                    entry = values[i];
                }
            }
            System.out.printf(
                "{\"rows\":%d,\"cols\":%d,\"nnz\":%d,\"entry_1_3\":%s}%n",
                size.numRows(), size.numColumns(), entries, Double.toString(entry));
        }
    }
}
