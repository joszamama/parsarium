package org.parsarium;

import org.jzy3d.io.ply.Ply;
import java.io.FileInputStream;

public final class Jzy3dPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        try (FileInputStream input = new FileInputStream(args[0])) {
            var vertices = Ply.read(input);
            // Coord3d stores float coordinates; print them at full float precision.
            System.out.println("{\"vertices\":" + vertices.size()
                    + ",\"second_x\":" + Float.toString(vertices.get(1).x)
                    + ",\"third_y\":" + Float.toString(vertices.get(2).y) + "}");
        }
    }
}
