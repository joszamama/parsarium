import java.nio.file.Path;
import javax.imageio.ImageIO;

public class PnmNativeAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: local.ppm");
        try (var input = ImageIO.createImageInputStream(Path.of(args[0]).toFile())) {
            var readers = ImageIO.getImageReaders(input);
            if (!readers.hasNext()) throw new IllegalStateException("Native ImageIO did not recognize PNM");
            var reader = readers.next();
            if (!reader.getClass().getName().startsWith("io.github.ghosthack."))
                throw new IllegalStateException("Unexpected PNM reader: " + reader.getClass().getName());
            try {
                reader.setInput(input);
                var image = reader.read(0);
                System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
                    image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
            } finally {
                reader.dispose();
            }
        }
    }
}
