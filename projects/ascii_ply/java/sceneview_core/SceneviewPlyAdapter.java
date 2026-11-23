package org.parsarium;

import io.github.sceneview.core.ply.PlyLoader;
import io.github.sceneview.core.ply.PlyModel;
import io.github.sceneview.core.ply.PlyParseException;
import io.github.sceneview.core.threemf.ThreeMfUnit;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.stream.Collectors;

public final class SceneviewPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        byte[] bytes = Files.readAllBytes(Path.of(args[0]));
        PlyModel model;
        try {
            model = PlyLoader.INSTANCE.parse(bytes, ThreeMfUnit.MILLIMETER,
                    1_000_000, 1_000_000, 32 * 1024 * 1024);
        } catch (PlyParseException rejected) {
            // Documented parser rejection, not a harness failure: report the parser's message.
            throw new IOException(rejected.toString(), rejected);
        }
        String indices = Arrays.stream(model.getIndices()).mapToObj(Integer::toString)
                .collect(Collectors.joining(","));
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%s]}%n",
                model.getVertexCount(), model.getTriangleCount(), indices);
    }
}
