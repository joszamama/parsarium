import java.awt.Component;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import com.github.weisj.jsvg.parser.LoaderContext;
import com.github.weisj.jsvg.parser.SVGLoader;
import com.github.weisj.jsvg.view.FloatSize;

public final class JsvgHarness {
    record Parsed(int width, int height, String pixels) {}

    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) {
            throw new IOException("input outside harness limit");
        }
        var svg = new SVGLoader().load(new ByteArrayInputStream(data),
                                       URI.create("file:/input/control.svg"), LoaderContext.createDefault());
        if (svg == null) throw new IOException("SVG loader rejected input");
        // The document's own size, rendered at that size with JSVG's default
        // bounds (null: the root's size), as in the JSVG README.
        FloatSize size = svg.size();
        int width = (int) size.width, height = (int) size.height;
        if (width <= 0 || height <= 0) return new Parsed(width, height, "");
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        try { svg.render((Component) null, graphics, null); }
        finally { graphics.dispose(); }
        long count = Math.min(2L, (long) width * height);
        StringBuilder pixels = new StringBuilder();
        for (int i = 0; i < count; i++) {
            if (i > 0) pixels.append(',');
            pixels.append(String.format("%08x", image.getRGB(i % width, i / width)));
        }
        return new Parsed(width, height, pixels.toString());
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (IOException | IllegalArgumentException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed result = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%s\"}%n",
                          result.width(), result.height(), result.pixels());
    }
}
