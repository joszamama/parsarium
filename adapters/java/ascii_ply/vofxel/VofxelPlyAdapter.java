package org.parsarium;

import eu.iamgio.vofxel.PlyParser;
import eu.iamgio.vofxel.Vertex;
import eu.iamgio.vofxel.VertexList;
import java.nio.file.Files;
import java.nio.file.Path;

public final class VofxelPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected local PLY path");
        try (var input = Files.newInputStream(Path.of(args[0]))) {
            VertexList vertices = new PlyParser(input).parse();
            Vertex first = vertices.get(0);
            Vertex last = vertices.get(vertices.size() - 1);
            System.out.printf(
                "{\"vertices\":%d,\"first_x\":%.1f,\"first_red\":%d,\"last_z\":%.1f}%n",
                vertices.size(), first.getX(), first.getRed(), last.getZ()
            );
        }
    }
}
