package org.parsarium;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javax.imageio.ImageIO;
import org.w3c.dom.Document;
import io.sf.carte.echosvg.anim.dom.SAXSVGDocumentFactory;
import io.sf.carte.echosvg.apps.rasterizer.SVGConverter;
import io.sf.carte.echosvg.swing.JSVGCanvas;
import io.sf.carte.echosvg.swing.svg.SVGDocumentLoaderAdapter;
import io.sf.carte.echosvg.swing.svg.SVGDocumentLoaderEvent;
import io.sf.carte.echosvg.transcoder.TranscoderInput;
import io.sf.carte.echosvg.transcoder.TranscoderOutput;
import io.sf.carte.echosvg.transcoder.image.PNGTranscoder;

public final class EchoSvgAdapter {
    private EchoSvgAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: label local.svg");
        Path path = Path.of(args[1]);
        switch (args[0]) {
            case "echosvg-anim" -> {
                try (InputStream input = Files.newInputStream(path)) {
                    Document svg = new SAXSVGDocumentFactory().createDocument(path.toUri().toString(), input);
                    printDom(svg);
                }
            }
            case "echosvg-transcoder-svg" -> {
                var parser = new PNGTranscoder();
                var bytes = new ByteArrayOutputStream();
                try (InputStream input = Files.newInputStream(path)) {
                    parser.transcode(new TranscoderInput(input), new TranscoderOutput(bytes));
                }
                printPixels(ImageIO.read(new ByteArrayInputStream(bytes.toByteArray())));
            }
            case "echosvg-svgrasterizer" -> {
                Path output = Files.createTempFile("parsarium-echosvg-", ".png");
                try {
                    var converter = new SVGConverter();
                    converter.setSources(new String[] {path.toAbsolutePath().toString()});
                    converter.setDst(output.toFile());
                    converter.execute();
                    printPixels(ImageIO.read(output.toFile()));
                } finally {
                    Files.deleteIfExists(output);
                }
            }
            case "echosvg-swing" -> {
                var canvas = new JSVGCanvas();
                var loaded = new CountDownLatch(1);
                canvas.addSVGDocumentLoaderListener(new SVGDocumentLoaderAdapter() {
                    @Override public void documentLoadingCompleted(SVGDocumentLoaderEvent event) {
                        loaded.countDown();
                    }
                });
                canvas.setURI(path.toUri().toString());
                if (!loaded.await(15, TimeUnit.SECONDS)) throw new IllegalStateException("EchoSVG canvas timed out");
                Document svg = canvas.getSVGDocument();
                if (svg == null) throw new IllegalStateException("EchoSVG canvas did not parse SVG");
                printDom(svg);
                canvas.stopProcessing();
            }
            default -> throw new IllegalArgumentException("unknown adapter: " + args[0]);
        }
    }

    private static void printDom(Document svg) {
        var root = svg.getDocumentElement();
        System.out.printf("{\"width\":%s,\"height\":%s,\"rects\":%d}%n",
            root.getAttribute("width"), root.getAttribute("height"),
            root.getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect").getLength());
    }

    private static void printPixels(java.awt.image.BufferedImage image) {
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
            image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
    }
}
