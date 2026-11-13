package org.parsarium;

import java.nio.file.Path;
import org.meteoinfo.math.matrix.DMatrix;

public final class MeteoInfoMatrixMarketAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected local Matrix Market path");
        DMatrix matrix = DMatrix.market(Path.of(args[0]));
        System.out.printf("{\"rows\":%d,\"cols\":%d,\"value_0_2\":%.1f}%n",
                          matrix.nrows(), matrix.ncols(), matrix.get(0, 2));
    }
}
