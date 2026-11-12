import java.nio.file.Path;
import javax.imageio.ImageIO;

public final class JdkSvgProbe {
    public static void main(String[] args) throws Exception {
        var readers = ImageIO.getImageReadersByFormatName("SVG");
        var image = ImageIO.read(Path.of(args[0]).toFile());
        System.out.printf("{\"svg_readers\":%d,\"imageio_result\":%s}%n",
            readers.hasNext() ? 1 : 0, image == null ? "null" : "image");
    }
}
