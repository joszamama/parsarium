package org.parsarium;

import com.ripplargames.meshio.Mesh;
import com.ripplargames.meshio.Face;
import com.ripplargames.meshio.meshformats.ply.PlyFormatAscii_1_0;
import java.io.File;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import org.smurn.jply.Element;
import org.smurn.jply.ElementReader;
import org.smurn.jply.PlyReaderFile;

public final class PlyAdapter {
    private PlyAdapter() {}

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
        } else throw new IllegalArgumentException("Unknown parser: " + args[0]);
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                vertices, faces, indices[0], indices[1], indices[2]);
    }
}
