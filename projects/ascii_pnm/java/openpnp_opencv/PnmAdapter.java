package org.parsarium;

import java.awt.image.BufferedImage;
import java.nio.file.Path;
import javax.imageio.ImageIO;
import javax.imageio.ImageReader;

public final class PnmAdapter {
    private PnmAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: label local.ppm");
        Path path = Path.of(args[1]);
        BufferedImage image;
        if (args[0].equals("commons-imaging")) {
            image = org.apache.commons.imaging.Imaging.getBufferedImage(path.toFile());
        } else if (args[0].equals("imagej")) {
            var opened = new ij.io.Opener().openImage(path.toString());
            if (opened == null) throw new IllegalStateException("ImageJ did not open PNM");
            image = opened.getBufferedImage();
        } else if (args[0].equals("thumbnailator")) {
            requirePnmReader(path);
            image = net.coobird.thumbnailator.Thumbnails.of(path.toFile()).scale(1.0).asBufferedImage();
        } else if (args[0].equals("boofcv-io")) {
            requirePnmReader(path);
            image = boofcv.io.image.UtilImageIO.loadImage(path.toString());
        } else if (args[0].equals("tika-image")) {
            requirePnmReader(path);
            var metadata = new org.apache.tika.metadata.Metadata();
            metadata.set(org.apache.tika.metadata.HttpHeaders.CONTENT_TYPE, "image/x-portable-pixmap");
            try (var input = org.apache.tika.io.TikaInputStream.get(path)) {
                new org.apache.tika.parser.image.ImageParser().parse(input,
                    new org.xml.sax.helpers.DefaultHandler(), metadata,
                    new org.apache.tika.parser.ParseContext());
            }
            System.out.printf("{\"width\":%s,\"height\":%s}%n",
                metadata.get(org.apache.tika.metadata.TIFF.IMAGE_WIDTH),
                metadata.get(org.apache.tika.metadata.TIFF.IMAGE_LENGTH));
            return;
        } else if (args[0].equals("openpnp-opencv")) {
            nu.pattern.OpenCV.loadLocally();
            var decoded = org.opencv.imgcodecs.Imgcodecs.imread(path.toString());
            try {
                if (decoded.empty()) throw new IllegalStateException("OpenCV did not decode PNM");
                image = new BufferedImage(decoded.cols(), decoded.rows(), BufferedImage.TYPE_INT_ARGB);
                for (int y = 0; y < decoded.rows(); y++) {
                    for (int x = 0; x < decoded.cols(); x++) {
                        double[] bgr = decoded.get(y, x);
                        image.setRGB(x, y, 0xff000000 | ((int) bgr[2] << 16) | ((int) bgr[1] << 8) | (int) bgr[0]);
                    }
                }
            } finally {
                decoded.release();
            }
        } else {
            String prefix = switch (args[0]) {
                case "twelvemonkeys-pnm" -> "com.twelvemonkeys.imageio.plugins.pnm.";
                case "jai-imageio-core" -> "com.github.jaiimageio.impl.plugins.pnm.";
                default -> throw new IllegalArgumentException("unknown adapter " + args[0]);
            };
            ImageReader reader = null;
            var candidates = ImageIO.getImageReadersByFormatName("PNM");
            while (candidates.hasNext()) {
                var candidate = candidates.next();
                if (candidate.getClass().getName().startsWith(prefix)) {
                    reader = candidate;
                    break;
                }
            }
            if (reader == null) throw new IllegalStateException("PNM reader unavailable: " + prefix);
            try (var input = ImageIO.createImageInputStream(path.toFile())) {
                reader.setInput(input);
                image = reader.read(0);
            } finally {
                reader.dispose();
            }
        }
        if (image == null) throw new IllegalStateException("No image decoded");
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
            image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
    }

    private static void requirePnmReader(Path path) throws Exception {
        try (var input = ImageIO.createImageInputStream(path.toFile())) {
            var readers = ImageIO.getImageReaders(input);
            if (!readers.hasNext()) throw new IllegalStateException("No ImageIO reader for PNM");
            readers.next().dispose();
        }
    }
}
