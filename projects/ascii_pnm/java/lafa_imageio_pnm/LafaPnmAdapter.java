package org.parsarium;

import java.io.File;
import javax.imageio.ImageIO;

/** Probe the isolated Lafa TwelveMonkeys PNM plugin on a local P3 PPM. */
public final class LafaPnmAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: LafaPnmAdapter control.ppm");
        try (var input = ImageIO.createImageInputStream(new File(args[0]))) {
            var readers = ImageIO.getImageReaders(input);
            if (!readers.hasNext()) throw new IllegalStateException("no PNM reader");
            var reader = readers.next();
            try {
                reader.setInput(input);
                var image = reader.read(0);
                System.out.printf("{\"reader\":\"%s\",\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
                    reader.getClass().getName(), image.getWidth(), image.getHeight(),
                    image.getRGB(0, 0), image.getRGB(1, 0));
            } finally {
                reader.dispose();
            }
        }
    }
}
