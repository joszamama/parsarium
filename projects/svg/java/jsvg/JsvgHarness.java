import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import com.github.weisj.jsvg.parser.LoaderContext;
import com.github.weisj.jsvg.parser.SVGLoader;
import com.github.weisj.jsvg.view.ViewBox;

public final class JsvgHarness {
    record Parsed(int width, int height, String pixels) {}

    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) {
            throw new IOException("input outside harness limit");
        }
        var svg = new SVGLoader().load(new ByteArrayInputStream(data),
                                       URI.create("file:/input/control.svg"), LoaderContext.createDefault());
        if (svg == null) throw new IOException("SVG loader rejected input");
        BufferedImage image = new BufferedImage(2, 1, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        try { svg.render(null, graphics, new ViewBox(0, 0, 2, 1)); }
        finally { graphics.dispose(); }
        return new Parsed(image.getWidth(), image.getHeight(),
                          String.format("%08x,%08x", image.getRGB(0, 0), image.getRGB(1, 0)));
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
