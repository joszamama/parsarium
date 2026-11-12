import java.io.File;
import javax.imageio.ImageIO;

public class JdkPnmProbe {
    public static void main(String[] args) throws Exception {
        int readers = 0;
        var candidates = ImageIO.getImageReadersByFormatName("PNM");
        while (candidates.hasNext()) { candidates.next(); readers++; }
        var decoded = ImageIO.read(new File(args[0]));
        System.out.printf("{\"pnm_readers\":%d,\"imageio_result\":%s}%n",
            readers, decoded == null ? "null" : "\"image\"");
    }
}
