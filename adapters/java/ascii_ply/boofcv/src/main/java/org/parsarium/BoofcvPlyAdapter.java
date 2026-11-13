package org.parsarium;

import boofcv.io.points.PointCloudIO;
import boofcv.struct.mesh.VertexMesh;
import java.io.FileInputStream;

public final class BoofcvPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        VertexMesh mesh = new VertexMesh();
        try (FileInputStream input = new FileInputStream(args[0])) {
            PointCloudIO.load(PointCloudIO.Format.PLY, input, mesh);
        }
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                mesh.vertexes.size(), mesh.size(), mesh.faceVertexes.get(0),
                mesh.faceVertexes.get(1), mesh.faceVertexes.get(2));
    }
}
