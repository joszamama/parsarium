package org.parsarium;

import io.pdal.Pipeline;
import io.pdal.PointView;
import io.pdal.PointViewIterator;
import java.io.IOException;

public final class PdalPlyAdapter {
    private static String quote(String value) {
        StringBuilder out = new StringBuilder("\"");
        for (char c : value.toCharArray()) {
            if (c == '"' || c == '\\') out.append('\\').append(c);
            else if (c < 0x20) out.append(String.format("\\u%04x", (int) c));
            else out.append(c);
        }
        return out.append('"').toString();
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        // Documented io.pdal.Pipeline(json): an explicit readers.ply stage on the local file,
        // executed through the pdal-native JNI library over PDAL's PlyReader.
        String json = "{\"pipeline\":[{\"type\":\"readers.ply\",\"filename\":" + quote(args[0]) + "}]}";
        Pipeline pipeline;
        try {
            pipeline = new Pipeline(json, io.pdal.LogLevel.Error());
        } catch (RuntimeException error) {
            throw new IOException("pipeline rejected: " + error.getMessage(), error);
        }
        try {
            try {
                pipeline.execute();
            } catch (RuntimeException error) {
                throw new IOException("readers.ply rejected input: " + error.getMessage(), error);
            }
            PointViewIterator views = pipeline.getPointViews();
            try {
                if (!views.hasNext()) throw new IOException("no point view");
                PointView view = views.next();
                try {
                    int points = view.length();
                    // second_x and last_y are reported only when the view has those points.
                    StringBuilder out = new StringBuilder(String.format("{\"points\":%d", points));
                    if (points > 1) out.append(String.format(",\"second_x\":%.1f", view.getDouble(1, "X")));
                    if (points > 0) out.append(String.format(",\"last_y\":%.1f", view.getDouble(points - 1, "Y")));
                    System.out.println(out.append('}'));
                } finally {
                    view.close();
                }
            } finally {
                views.close();
            }
        } finally {
            pipeline.close();
        }
    }
}
