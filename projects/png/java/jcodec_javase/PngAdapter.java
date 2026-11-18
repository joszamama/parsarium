package org.parsarium;

import java.awt.image.BufferedImage;
import java.nio.file.Files;
import java.nio.file.Path;
import javax.imageio.ImageIO;

public final class PngAdapter {
    private PngAdapter() {}

    private record Parsed(int width, int height, String pixels) {}

    /** Pixel (0,0) and, when the image is wider than one pixel, pixel (1,0), as ARGB hex. */
    private static String pixels(int width, int first, java.util.function.IntSupplier second) {
        return width > 1 ? String.format("%08x,%08x", first, second.getAsInt())
                : String.format("%08x", first);
    }

    private static Parsed fromImage(BufferedImage image) {
        if (image == null) throw new IllegalStateException("no image decoded");
        return new Parsed(image.getWidth(), image.getHeight(),
                pixels(image.getWidth(), image.getRGB(0, 0), () -> image.getRGB(1, 0)));
    }

    private static Parsed fromAwtImage(java.awt.Image image) {
        var loaded = new javax.swing.ImageIcon(image);
        if (loaded.getIconWidth() <= 0 || loaded.getIconHeight() <= 0) {
            throw new IllegalStateException("AWT image failed to decode");
        }
        var buffered = new BufferedImage(loaded.getIconWidth(), loaded.getIconHeight(),
                BufferedImage.TYPE_INT_ARGB);
        var graphics = buffered.createGraphics();
        try {
            graphics.drawImage(loaded.getImage(), 0, 0, null);
        } finally {
            graphics.dispose();
        }
        return fromImage(buffered);
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: PngAdapter API CONTROL.png");
        Path path = Path.of(args[1]);
        Parsed parsed = switch (args[0]) {
            case "jdk-imageio" -> fromImage(ImageIO.read(path.toFile()));
            case "jdk-imageicon" -> fromAwtImage(
                    new javax.swing.ImageIcon(Files.readAllBytes(path)).getImage());
            case "jdk-toolkit" -> fromAwtImage(
                    java.awt.Toolkit.getDefaultToolkit().createImage(Files.readAllBytes(path)));
            case "jdk-imagereader" -> {
                var readers = ImageIO.getImageReadersByFormatName("PNG");
                if (!readers.hasNext()) throw new IllegalStateException("JDK PNG reader not found");
                var reader = readers.next();
                try (var input = ImageIO.createImageInputStream(path.toFile())) {
                    reader.setInput(input);
                    yield fromImage(reader.read(0));
                } finally {
                    reader.dispose();
                }
            }
            case "commons-imaging" -> fromImage(
                    org.apache.commons.imaging.Imaging.getBufferedImage(path.toFile()));
            case "pngj" -> {
                try (var input = Files.newInputStream(path)) {
                    var reader = new ar.com.hjg.pngj.PngReader(input);
                    var line = (ar.com.hjg.pngj.ImageLineInt) reader.readRow();
                    var values = line.getScanline();
                    int first = (values[3] << 24) | (values[0] << 16) | (values[1] << 8) | values[2];
                    Parsed result = new Parsed(reader.imgInfo.cols, reader.imgInfo.rows,
                            pixels(reader.imgInfo.cols, first,
                                    () -> (values[7] << 24) | (values[4] << 16) | (values[5] << 8) | values[6]));
                    reader.end();
                    yield result;
                }
            }
            case "thumbnailator" -> fromImage(net.coobird.thumbnailator.Thumbnails
                    .of(path.toFile()).scale(1.0).asBufferedImage());
            case "ij" -> {
                var image = new ij.io.Opener().openImage(path.toString());
                if (image == null) throw new IllegalStateException("ImageJ failed to open PNG");
                yield fromImage(image.getBufferedImage());
            }
            case "boofcv-io" -> fromImage(boofcv.io.image.UtilImageIO.loadImage(path.toString()));
            case "batik-codec" -> {
                try (var input = Files.newInputStream(path)) {
                    var rendered = new org.apache.batik.ext.awt.image.codec.png.PNGImageDecoder(input, null)
                            .decodeAsRenderedImage();
                    var image = new BufferedImage(rendered.getWidth(), rendered.getHeight(),
                            BufferedImage.TYPE_INT_ARGB);
                    var graphics = image.createGraphics();
                    try {
                        graphics.drawRenderedImage(rendered, new java.awt.geom.AffineTransform());
                    } finally {
                        graphics.dispose();
                    }
                    yield fromImage(image);
                }
            }
            case "pngtastic" -> {
                try (var input = Files.newInputStream(path)) {
                    var image = new com.googlecode.pngtastic.core.PngImage(input);
                    yield new Parsed(Math.toIntExact(image.getWidth()), Math.toIntExact(image.getHeight()), null);
                }
            }
            case "itextpdf" -> {
                try (var input = Files.newInputStream(path)) {
                    var image = com.itextpdf.text.pdf.codec.PngImage.getImage(input);
                    yield new Parsed(Math.round(image.getWidth()), Math.round(image.getHeight()), null);
                }
            }
            case "metadata-extractor" -> {
                var metadata = com.drew.imaging.ImageMetadataReader.readMetadata(path.toFile());
                var image = metadata.getFirstDirectoryOfType(com.drew.metadata.png.PngDirectory.class);
                if (image == null) throw new IllegalStateException("PNG IHDR metadata missing");
                yield new Parsed(image.getInt(com.drew.metadata.png.PngDirectory.TAG_IMAGE_WIDTH),
                        image.getInt(com.drew.metadata.png.PngDirectory.TAG_IMAGE_HEIGHT), null);
            }
            case "jOpenDocument" -> {
                var image = new org.jopendocument.util.ImageInfo();
                try (var input = Files.newInputStream(path)) {
                    image.setInput(input);
                    if (!image.check() || !"PNG".equals(image.getFormatName())) {
                        throw new IllegalStateException("PNG not recognized");
                    }
                    yield new Parsed(image.getWidth(), image.getHeight(), null);
                }
            }
            case "pdfbox" -> {
                try (var document = new org.apache.pdfbox.pdmodel.PDDocument()) {
                    var image = org.apache.pdfbox.pdmodel.graphics.image.PDImageXObject
                            .createFromFileByContent(path.toFile(), document);
                    yield new Parsed(image.getWidth(), image.getHeight(), null);
                }
            }
            case "jcodec" -> {
                var decoder = new org.jcodec.codecs.png.PNGDecoder();
                var bytes = java.nio.ByteBuffer.wrap(Files.readAllBytes(path));
                var size = decoder.getCodecMeta(bytes.duplicate()).getSize();
                var buffer = org.jcodec.common.model.Picture.create(size.getWidth(), size.getHeight(),
                        org.jcodec.common.model.ColorSpace.RGB).getData();
                var image = decoder.decodeFrame(bytes, buffer);
                yield new Parsed(image.getWidth(), image.getHeight(), null);
            }
            case "jcodec-javase" -> {
                var image = new org.jcodec.codecs.pngawt.PNGDecoder().decodeFrame(
                        java.nio.ByteBuffer.wrap(Files.readAllBytes(path)), null);
                yield new Parsed(image.getWidth(), image.getHeight(), null);
            }
            case "openpdf" -> {
                var image = org.openpdf.text.ImageLoader.getPngImage(Files.readAllBytes(path));
                yield new Parsed(Math.round(image.getWidth()), Math.round(image.getHeight()), null);
            }
            case "itext-io" -> {
                var image = com.itextpdf.io.image.ImageDataFactory.createPng(Files.readAllBytes(path));
                yield new Parsed(Math.round(image.getWidth()), Math.round(image.getHeight()), null);
            }
            case "lwjgl-stb" -> {
                byte[] bytes = Files.readAllBytes(path);
                var encoded = java.nio.ByteBuffer.allocateDirect(bytes.length);
                encoded.put(bytes).flip();
                int[] width = new int[1], height = new int[1], channels = new int[1];
                var pixels = org.lwjgl.stb.STBImage.stbi_load_from_memory(encoded,
                        width, height, channels, org.lwjgl.stb.STBImage.STBI_rgb_alpha);
                if (pixels == null) throw new IllegalStateException(org.lwjgl.stb.STBImage.stbi_failure_reason());
                try {
                    int first = (pixels.get(3) & 255) << 24 | (pixels.get(0) & 255) << 16
                            | (pixels.get(1) & 255) << 8 | (pixels.get(2) & 255);
                    yield new Parsed(width[0], height[0], pixels(width[0], first,
                            () -> (pixels.get(7) & 255) << 24 | (pixels.get(4) & 255) << 16
                                    | (pixels.get(5) & 255) << 8 | (pixels.get(6) & 255)));
                } finally {
                    org.lwjgl.stb.STBImage.stbi_image_free(pixels);
                }
            }
            case "tika-image" -> {
                var metadata = new org.apache.tika.metadata.Metadata();
                metadata.set(org.apache.tika.metadata.HttpHeaders.CONTENT_TYPE, "image/png");
                try (var input = org.apache.tika.io.TikaInputStream.get(path)) {
                    new org.apache.tika.parser.image.ImageParser().parse(input,
                            new org.xml.sax.helpers.DefaultHandler(), metadata,
                            new org.apache.tika.parser.ParseContext());
                }
                yield new Parsed(Integer.parseInt(metadata.get(org.apache.tika.metadata.TIFF.IMAGE_WIDTH)),
                        Integer.parseInt(metadata.get(org.apache.tika.metadata.TIFF.IMAGE_LENGTH)), null);
            }
            case "xmlgraphics-commons" -> {
                var manager = new org.apache.xmlgraphics.image.loader.ImageManager(
                        new org.apache.xmlgraphics.image.loader.impl.DefaultImageContext());
                var session = new org.apache.xmlgraphics.image.loader.impl.DefaultImageSessionContext(
                        manager.getImageContext(), null);
                var info = manager.getImageInfo(path.toUri().toString(), session);
                if (!"image/png".equals(info.getMimeType())) {
                    throw new IllegalStateException("PNG not recognized");
                }
                yield new Parsed(info.getSize().getWidthPx(), info.getSize().getHeightPx(), null);
            }
            case "javafx-graphics" -> {
                try (var input = Files.newInputStream(path)) {
                    var image = new javafx.scene.image.Image(input);
                    if (image.isError()) throw new IllegalStateException("JavaFX PNG failed", image.getException());
                    var pixels = image.getPixelReader();
                    if (pixels == null) throw new IllegalStateException("JavaFX pixel reader missing");
                    yield new Parsed((int) image.getWidth(), (int) image.getHeight(),
                            pixels((int) image.getWidth(), pixels.getArgb(0, 0), () -> pixels.getArgb(1, 0)));
                }
            }
            case "openpnp-opencv" -> {
                nu.pattern.OpenCV.loadLocally();
                var image = org.opencv.imgcodecs.Imgcodecs.imread(path.toString(),
                        org.opencv.imgcodecs.Imgcodecs.IMREAD_UNCHANGED);
                try {
                    if (image.empty()) throw new IllegalStateException("OpenCV PNG failed");
                    yield new Parsed(image.cols(), image.rows(), null);
                } finally {
                    image.release();
                }
            }
            default -> throw new IllegalArgumentException("unknown API: " + args[0]);
        };
        System.out.println("{\"width\":" + parsed.width + ",\"height\":" + parsed.height
                + (parsed.pixels == null ? "}" : ",\"pixels\":\"" + parsed.pixels + "\"}"));
    }
}
