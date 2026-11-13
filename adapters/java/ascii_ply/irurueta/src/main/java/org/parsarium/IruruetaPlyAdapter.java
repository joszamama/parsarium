package org.parsarium;

import com.irurueta.geometry.io.LoaderPLY;
import java.io.File;

public final class IruruetaPlyAdapter {
    private IruruetaPlyAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("expected local PLY path");
        }
        var loader = new LoaderPLY(new File(args[0]));
        var chunks = loader.load();
        int vertices = 0;
        int faces = 0;
        int[] indices = null;
        while (chunks.hasNext()) {
            var chunk = chunks.next();
            var positions = chunk.getVerticesCoordinatesData();
            if (positions != null) {
                vertices += positions.length / 3;
            }
            var faceIndices = chunk.getIndicesData();
            if (faceIndices != null) {
                indices = faceIndices;
                faces += faceIndices.length / 3;
            }
        }
        if (indices == null || indices.length != 3) {
            throw new IllegalStateException("expected one parsed triangle");
        }
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                vertices, faces, indices[0], indices[1], indices[2]);
    }
}
