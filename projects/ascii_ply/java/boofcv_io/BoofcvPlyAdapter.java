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
        // Vertex indices of the first face: faceOffsets holds each face's start
        // in faceVertexes (it starts with 0); empty when the mesh has no faces.
        StringBuilder indices = new StringBuilder();
        if (mesh.size() > 0) {
            for (int i = mesh.faceOffsets.get(0); i < mesh.faceOffsets.get(1); i++) {
                if (indices.length() > 0) indices.append(',');
                indices.append(mesh.faceVertexes.get(i));
            }
        }
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%s]}%n",
                mesh.vertexes.size(), mesh.size(), indices);
    }
}
