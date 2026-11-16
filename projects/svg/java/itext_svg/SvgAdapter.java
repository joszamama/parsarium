package org.parsarium;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javax.imageio.ImageIO;

import org.apache.batik.anim.dom.SAXSVGDocumentFactory;
import org.apache.batik.apps.rasterizer.SVGConverter;
import org.apache.batik.swing.JSVGCanvas;
import org.apache.batik.swing.svg.SVGDocumentLoaderAdapter;
import org.apache.batik.swing.svg.SVGDocumentLoaderEvent;
import org.apache.batik.transcoder.TranscoderInput;
import org.apache.batik.transcoder.TranscoderOutput;
import org.apache.batik.transcoder.image.PNGTranscoder;
import org.apache.batik.util.XMLResourceDescriptor;
import org.w3c.dom.Document;

import com.github.weisj.jsvg.parser.LoaderContext;
import com.github.weisj.jsvg.parser.SVGLoader;
import com.github.weisj.jsvg.view.ViewBox;
import com.kitfox.svg.SVGDiagram;
import com.kitfox.svg.SVGUniverse;

public final class SvgAdapter {
    private SvgAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: label local.svg");
        Path path = Path.of(args[1]);
        switch (args[0]) {
            case "batik-anim" -> {
                SAXSVGDocumentFactory factory = new SAXSVGDocumentFactory(
                    XMLResourceDescriptor.getXMLParserClassName());
                try (InputStream input = Files.newInputStream(path)) {
                    Document svg = factory.createDocument(path.toUri().toString(), input);
                    int rects = svg.getDocumentElement()
                        .getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect").getLength();
                    String width = svg.getDocumentElement().getAttribute("width");
                    String height = svg.getDocumentElement().getAttribute("height");
                    System.out.printf("{\"width\":%s,\"height\":%s,\"rects\":%d}%n",
                        width, height, rects);
                }
            }
            case "batik-transcoder" -> {
                PNGTranscoder parser = new PNGTranscoder();
                ByteArrayOutputStream bytes = new ByteArrayOutputStream();
                try (InputStream input = Files.newInputStream(path)) {
                    parser.transcode(new TranscoderInput(input), new TranscoderOutput(bytes));
                }
                printPixels(ImageIO.read(new java.io.ByteArrayInputStream(bytes.toByteArray())));
            }
            case "batik-svgrasterizer" -> {
                Path output = Files.createTempFile("parsarium-svg-", ".png");
                try {
                    SVGConverter parser = new SVGConverter();
                    parser.setSources(new String[] {path.toAbsolutePath().toString()});
                    parser.setDst(output.toFile());
                    parser.execute();
                    printPixels(ImageIO.read(output.toFile()));
                } finally {
                    Files.deleteIfExists(output);
                }
            }
            case "batik-swing" -> {
                JSVGCanvas canvas = new JSVGCanvas();
                CountDownLatch loaded = new CountDownLatch(1);
                canvas.addSVGDocumentLoaderListener(new SVGDocumentLoaderAdapter() {
                    @Override public void documentLoadingCompleted(SVGDocumentLoaderEvent event) {
                        loaded.countDown();
                    }
                });
                canvas.setURI(path.toUri().toString());
                if (!loaded.await(15, TimeUnit.SECONDS)) throw new IllegalStateException("SVG canvas load timed out");
                var svg = canvas.getSVGDocument();
                if (svg == null) throw new IllegalStateException("SVG canvas did not parse document");
                System.out.printf("{\"width\":%s,\"height\":%s,\"rects\":%d}%n",
                    svg.getDocumentElement().getAttribute("width"),
                    svg.getDocumentElement().getAttribute("height"),
                    svg.getDocumentElement().getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect").getLength());
                canvas.stopProcessing();
            }
            case "itext-svg" -> {
                ByteArrayOutputStream bytes = new ByteArrayOutputStream();
                try (InputStream input = Files.newInputStream(path);
                     var pdf = new com.itextpdf.kernel.pdf.PdfDocument(new com.itextpdf.kernel.pdf.PdfWriter(bytes))) {
                    var object = com.itextpdf.svg.converter.SvgConverter.convertToXObject(input, pdf);
                    System.out.printf("{\"width\":%d,\"height\":%d}%n",
                        Math.round(object.getWidth()), Math.round(object.getHeight()));
                }
            }
            case "fop-core" -> {
                ByteArrayOutputStream bytes = new ByteArrayOutputStream();
                try (InputStream input = Files.newInputStream(path)) {
                    var parser = new org.apache.fop.svg.PDFTranscoder();
                    parser.transcode(new TranscoderInput(input), new TranscoderOutput(bytes));
                }
                try (var pdf = new com.itextpdf.kernel.pdf.PdfDocument(
                         new com.itextpdf.kernel.pdf.PdfReader(new java.io.ByteArrayInputStream(bytes.toByteArray())))) {
                    var page = pdf.getFirstPage();
                    var size = page.getPageSize();
                    String content = new String(page.getContentBytes(), java.nio.charset.StandardCharsets.ISO_8859_1);
                    System.out.printf("{\"width\":%d,\"height\":%d,\"red\":%s,\"green\":%s}%n",
                        Math.round(size.getWidth()), Math.round(size.getHeight()),
                        content.contains("1 0 0 rg"), content.contains("0 1 0 rg"));
                }
            }
            case "radiance-svg-transcoder" -> {
                var generated = new java.io.StringWriter();
                String template = "TOKEN_ORIG_WIDTH,TOKEN_ORIG_HEIGHT\nTOKEN_PAINTING_CODE\n";
                try (InputStream input = Files.newInputStream(path);
                     InputStream pattern = new java.io.ByteArrayInputStream(template.getBytes(java.nio.charset.StandardCharsets.UTF_8))) {
                    var parser = new org.pushingpixels.radiance.tools.svgtranscoder.api.SvgStreamTranscoder(
                        input, "ParsariumSvg", new org.pushingpixels.radiance.tools.svgtranscoder.api.java.JavaLanguageRenderer());
                    parser.setPrintWriter(new java.io.PrintWriter(generated));
                    parser.transcode(pattern);
                }
                String result = generated.toString();
                System.out.printf("{\"dimensions\":%s,\"red\":%s,\"green\":%s}%n",
                    result.contains("2.0,1.0"), result.contains("255, 0, 0"), result.contains("0, 255, 0"));
            }
            case "aurora-svg-transcoder" -> {
                var writer = new java.io.StringWriter();
                var parser = new org.pushingpixels.aurora.tools.svgtranscoder.SvgTranscoder(
                    path.toUri().toString(), "ParsariumSvg");
                parser.setListener(new org.pushingpixels.aurora.tools.svgtranscoder.TranscoderListener() {
                    @Override public java.io.Writer getWriter() { return writer; }
                    @Override public void finished() {}
                });
                try (InputStream template = new java.io.ByteArrayInputStream("TOKEN_ORIG_WIDTH,TOKEN_ORIG_HEIGHT\n"
                         .getBytes(java.nio.charset.StandardCharsets.UTF_8))) {
                    Document svg = parser.transcode(template);
                    if (svg == null) throw new IllegalStateException("Aurora did not parse SVG");
                    System.out.printf("{\"width\":%s,\"height\":%s,\"rects\":%d}%n",
                        svg.getDocumentElement().getAttribute("width"),
                        svg.getDocumentElement().getAttribute("height"),
                        svg.getDocumentElement().getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect").getLength());
                }
            }
            case "gsvg" -> {
                var svg = se.alipsa.groovy.svg.io.SvgReader.parse(path.toFile());
                var rects = svg.findAll(se.alipsa.groovy.svg.Rect.class);
                System.out.printf("{\"width\":%s,\"height\":%s,\"rects\":%d,\"fills\":\"%s,%s\"}%n",
                    svg.getWidth(), svg.getHeight(), rects.size(),
                    rects.get(0).getFill(), rects.get(1).getFill());
            }
            case "furutuki-transcoder" -> {
                var generated = new java.io.StringWriter();
                var parser = new com.github.furutuki.androidsvgtranscoder.SvgTranscoder(
                    path.toUri().toURL(), "ParsariumSvg");
                parser.setExternalPrintWriter(new java.io.PrintWriter(generated));
                parser.transcode();
                String result = generated.toString();
                System.out.printf("{\"dimensions\":%s,\"red\":%s,\"green\":%s}%n",
                    result.contains("2.0") && result.contains("1.0"),
                    result.contains("255, 0, 0"), result.contains("0, 255, 0"));
            }
            case "twelvemonkeys-batik" -> {
                javax.imageio.ImageReader reader = null;
                var providers = ImageIO.getImageReadersByFormatName("SVG");
                while (providers.hasNext()) {
                    var candidate = providers.next();
                    if (candidate.getClass().getName().startsWith("com.twelvemonkeys.imageio.plugins.svg.")) {
                        reader = candidate;
                        break;
                    }
                }
                if (reader == null) throw new IllegalStateException("TwelveMonkeys SVG reader unavailable");
                try (var input = ImageIO.createImageInputStream(path.toFile())) {
                    reader.setInput(input);
                    printPixels(reader.read(0));
                } finally {
                    reader.dispose();
                }
            }
            case "jsvgicon" -> {
                try (InputStream input = Files.newInputStream(path)) {
                    var shape = com.bw.jtools.svg.SVGConverter.convert(input);
                    var painter = new com.bw.jtools.shape.ShapePainter(shape);
                    BufferedImage image = new BufferedImage(2, 1, BufferedImage.TYPE_INT_ARGB);
                    printPixels(painter.paintShapeToBufferTransparent(image, false));
                }
            }
            case "jsvg" -> {
                com.github.weisj.jsvg.SVGDocument svg;
                try (InputStream input = Files.newInputStream(path)) {
                    svg = new SVGLoader().load(input, path.toUri(), LoaderContext.createDefault());
                }
                if (svg == null) throw new IllegalStateException("JSVG did not parse SVG");
                BufferedImage image = new BufferedImage(2, 1, BufferedImage.TYPE_INT_ARGB);
                Graphics2D graphics = image.createGraphics();
                svg.render(null, graphics, new ViewBox(0, 0, 2, 1));
                graphics.dispose();
                printPixels(image);
            }
            case "svg-salamander" -> {
                SVGUniverse universe = new SVGUniverse();
                URI uri;
                try (InputStream input = Files.newInputStream(path)) {
                    uri = universe.loadSVG(input, "parsarium-control.svg");
                }
                SVGDiagram svg = universe.getDiagram(uri);
                if (svg == null) throw new IllegalStateException("Salamander did not parse SVG");
                BufferedImage image = new BufferedImage(2, 1, BufferedImage.TYPE_INT_ARGB);
                Graphics2D graphics = image.createGraphics();
                svg.render(graphics);
                graphics.dispose();
                printPixels(image);
            }
            default -> throw new IllegalArgumentException("unknown adapter: " + args[0]);
        }
    }

    private static void printPixels(BufferedImage image) {
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
            image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
    }
}
