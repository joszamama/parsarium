import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import javax.imageio.ImageIO;
import javax.imageio.ImageReader;
import javax.imageio.stream.MemoryCacheImageInputStream;

public final class JaiPnmHarness {
    record Parsed(int width, int height, String pixels) {}

    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) {
            throw new IOException("input outside harness limit");
        }
        ImageReader reader = null;
        var candidates = ImageIO.getImageReadersByFormatName("PNM");
        while (candidates.hasNext()) {
            ImageReader candidate = candidates.next();
            if (candidate.getClass().getName().startsWith("com.github.jaiimageio.impl.plugins.pnm.")) {
                reader = candidate;
                break;
            }
            candidate.dispose();
        }
        if (reader == null) throw new IOException("JAI PNM reader unavailable");
        try (var input = new MemoryCacheImageInputStream(new ByteArrayInputStream(data))) {
            reader.setInput(input);
            BufferedImage image = reader.read(0);
            int width = image.getWidth();
            int height = image.getHeight();
            // The first pixel and the next one in raster order, if the image has one.
            String pixels = String.format("%08x", image.getRGB(0, 0));
            if (width > 1) pixels += String.format(",%08x", image.getRGB(1, 0));
            else if (height > 1) pixels += String.format(",%08x", image.getRGB(0, 1));
            return new Parsed(width, height, pixels);
        } finally {
            reader.dispose();
        }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try {
            parse(data);
        } catch (IOException | IllegalArgumentException ignored) {
            // Invalid images can be rejected by the parser.
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed result = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%s\"}%n",
                result.width(), result.height(), result.pixels());
    }
}
