package org.parsarium;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import org.apache.sysds.common.Types;
import org.apache.sysds.runtime.io.IOUtilFunctions;
import org.apache.sysds.runtime.io.ReaderTextCell;
import org.apache.sysds.runtime.matrix.data.MatrixBlock;

public final class SystemDSMatrixMarketAdapter {
    private SystemDSMatrixMarketAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected one local Matrix Market path");
        }
        String[] header = IOUtilFunctions.readMatrixMarketHeader(args[0]);
        String[] dimensions = header[1].trim().split("\\s+");
        int rows = Integer.parseInt(dimensions[0]);
        int columns = Integer.parseInt(dimensions[1]);
        long nonzeros = Long.parseLong(dimensions[2]);
        try (InputStream input = Files.newInputStream(Path.of(args[0]))) {
            MatrixBlock matrix = new ReaderTextCell(Types.FileFormat.MM)
                .readMatrixFromInputStream(input, rows, columns, 1000, nonzeros);
            System.out.printf(
                "{\"rows\":%d,\"cols\":%d,\"nnz\":%d,\"entry_1_3\":%s}%n",
                matrix.getNumRows(), matrix.getNumColumns(), matrix.getNonZeros(),
                Double.toString(matrix.get(0, 2)));
        }
    }
}
