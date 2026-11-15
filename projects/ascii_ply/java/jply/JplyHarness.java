import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.smurn.jply.PlyReaderFile;
import org.smurn.jply.ElementReader;
import org.smurn.jply.Element;

public final class JplyHarness {
    record Parsed(int vertices, int faces, int[] indices) {}
    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IOException("input outside harness limit");
        Path path = Files.createTempFile("parsarium-ply-", ".ply");
        try {
            Files.write(path, data);
            PlyReaderFile reader = new PlyReaderFile(path.toFile());
            try {
                int vertices = reader.getElementCount("vertex");
                int faces = reader.getElementCount("face");
                int[] indices = null;
                ElementReader elements;
                while ((elements = reader.nextElementReader()) != null) {
                    try {
                        if (elements.getElementType().getName().equals("face")) {
                            Element face = elements.readElement();
                            indices = face.getIntList("vertex_indices");
                        } else {
                            for (int i = 0; i < elements.getCount(); i++) elements.readElement();
                        }
                    } finally { elements.close(); }
                }
                if (indices == null || indices.length != 3) throw new IOException("no triangle face");
                return new Parsed(vertices, faces, indices);
            } finally { reader.close(); }
        } finally { Files.deleteIfExists(path); }
    }
    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); } catch (IOException | IllegalArgumentException ignored) { }
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed p = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                          p.vertices(), p.faces(), p.indices()[0], p.indices()[1], p.indices()[2]);
    }
}
