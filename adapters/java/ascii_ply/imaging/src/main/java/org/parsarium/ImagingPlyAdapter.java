package org.parsarium;

import java.nio.file.Files;
import java.nio.file.Path;
import science.aist.imaging.mesh.storage.ply.PlyReader;

public final class ImagingPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        try (var input = Files.newBufferedReader(Path.of(args[0]))) {
            var mesh = new PlyReader().read(input).orElseThrow();
            System.out.printf("{\"points\":%d,\"faces\":%d}%n",
                    mesh.getPoints().size(), mesh.getMesh().size());
        }
    }
}
