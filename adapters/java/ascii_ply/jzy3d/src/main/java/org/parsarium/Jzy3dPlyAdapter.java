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
            System.out.printf("{\"vertices\":%d,\"second_x\":%.1f,\"third_y\":%.1f}%n",
                    vertices.size(), vertices.get(1).x, vertices.get(2).y);
        }
    }
}
