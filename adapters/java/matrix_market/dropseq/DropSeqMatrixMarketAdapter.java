package org.parsarium;

import java.io.File;
import org.broadinstitute.dropseqrna.matrixmarket.MatrixMarketReader;

public final class DropSeqMatrixMarketAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected local Matrix Market path");
        try (MatrixMarketReader reader = new MatrixMarketReader(new File(args[0]))) {
            int entries = 0;
            double value = 0;
            for (MatrixMarketReader.Element element : reader) {
                entries++;
                if (element.row == 0 && element.col == 2) value = element.realValue();
            }
            System.out.printf(
                "{\"rows\":%d,\"cols\":%d,\"entries\":%d,\"value_0_2\":%.1f}%n",
                reader.getNumRows(), reader.getNumCols(), entries, value
            );
        }
    }
}
