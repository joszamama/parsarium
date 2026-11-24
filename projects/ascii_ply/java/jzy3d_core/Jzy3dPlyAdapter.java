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
            // second_x and third_y are reported only when the file has that many vertices.
            StringBuilder json = new StringBuilder(String.format("{\"vertices\":%d", vertices.size()));
            // Coord3d stores float coordinates; print them at full float precision.
            if (vertices.size() > 1) json.append(",\"second_x\":").append(Float.toString(vertices.get(1).x));
            if (vertices.size() > 2) json.append(",\"third_y\":").append(Float.toString(vertices.get(2).y));
            System.out.println(json.append('}'));
        }
    }
}
