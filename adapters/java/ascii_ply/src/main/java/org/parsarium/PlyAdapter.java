package org.parsarium;

import com.ripplargames.meshio.Mesh;
import com.ripplargames.meshio.Face;
import com.ripplargames.meshio.meshformats.ply.PlyFormatAscii_1_0;
import java.io.File;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.nio.file.Files;
import java.nio.file.Path;
import org.smurn.jply.Element;
import org.smurn.jply.ElementReader;
import org.smurn.jply.PlyReaderFile;

public final class PlyAdapter {
    private PlyAdapter() {}

    public static final class PointCloud {
        private final List<float[]> points = new ArrayList<>();
        private final List<int[]> triangles = new ArrayList<>();

        @cn.jimmiez.pcu.io.ply.ReadFromPly(element = "vertex", properties = {"x", "y", "z"})
        public List<float[]> getPoints() { return points; }

        @cn.jimmiez.pcu.io.ply.ReadFromPly(element = "face", properties = {"vertex_indices"})
        public List<int[]> getTriangles() { return triangles; }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("Expected parser and local PLY path");
        int vertices, faces;
        int[] indices;
        if (args[0].equals("jply")) {
            PlyReaderFile reader = new PlyReaderFile(new File(args[1]));
            try {
                vertices = reader.getElementCount("vertex");
                faces = reader.getElementCount("face");
                indices = null;
                ElementReader elements;
                while ((elements = reader.nextElementReader()) != null) {
                    if (elements.getElementType().getName().equals("face")) {
                        Element face = elements.readElement();
                        indices = face.getIntList("vertex_indices");
                    } else {
                        for (int i = 0; i < elements.getCount(); i++) elements.readElement();
                    }
                    elements.close();
                }
                if (indices == null) throw new IllegalStateException("No parsed face");
            } finally {
                reader.close();
            }
        } else if (args[0].equals("meshio")) {
            try (InputStream in = Files.newInputStream(Path.of(args[1]))) {
                Mesh mesh = new PlyFormatAscii_1_0().read(in);
                vertices = mesh.vertexCount();
                faces = mesh.faceCount();
                Face face = mesh.faces().get(0);
                indices = new int[]{face.getV0(), face.getV1(), face.getV2()};
            }
        } else if (args[0].equals("mesh-ply")) {
            hu.kazocsaba.v3d.mesh.IndexedTriangleMesh mesh =
                    hu.kazocsaba.v3d.mesh.format.ply.PlyReader.readMesh(new File(args[1]));
            vertices = mesh.getPointCount();
            faces = mesh.getTriangleCount();
            indices = new int[]{mesh.getTrianglePointIndex(0, 0),
                                mesh.getTrianglePointIndex(0, 1),
                                mesh.getTrianglePointIndex(0, 2)};
        } else if (args[0].equals("pcutil")) {
            PointCloud cloud = new cn.jimmiez.pcu.io.ply.PlyReader().read(
                    new File(args[1]), PointCloud.class);
            vertices = cloud.getPoints().size();
            faces = cloud.getTriangles().size();
            indices = cloud.getTriangles().get(0);
        } else throw new IllegalArgumentException("Unknown parser: " + args[0]);
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                vertices, faces, indices[0], indices[1], indices[2]);
    }
}
