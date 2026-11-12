use std::error::Error;
use std::fs;
use std::io::{BufReader, Cursor};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        return Err("usage: cargo run -- PACKAGE CONTROL".into());
    }
    let name = &args[1];
    let bytes = fs::read(&args[2])?;
    match name.as_str() {
        "png" => {
            let decoder = png::Decoder::new(BufReader::new(Cursor::new(&bytes)));
            let mut reader = decoder.read_info()?;
            let mut buffer = vec![0; reader.output_buffer_size().expect("PNG output size")];
            let frame = reader.next_frame(&mut buffer)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", frame.width, frame.height, buffer[0]);
        }
        "image" => {
            let image = image::load_from_memory(&bytes)?.to_rgba8();
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width(), image.height(), image.get_pixel(0, 0)[0]);
        }
        "img-parts" => {
            let image = img_parts::png::Png::from_bytes(bytes.into())?;
            let (width, height) = image.dimensions().ok_or("missing PNG dimensions")?;
            println!("{{\"width\":{},\"height\":{},\"chunks\":{}}}", width, height, image.chunks().len());
        }
        "png_pong" => {
            use png_pong::PngRaster::*;
            let decoder = png_pong::Decoder::new(BufReader::new(Cursor::new(&bytes)))?;
            let step = decoder.into_steps().next().ok_or("missing PNG frame")??;
            let (width, height) = match step.raster {
                Gray8(r) => (r.width(), r.height()), Gray16(r) => (r.width(), r.height()),
                Rgb8(r) => (r.width(), r.height()), Rgb16(r) => (r.width(), r.height()),
                Palette(r, _, _) => (r.width(), r.height()),
                Graya8(r) => (r.width(), r.height()), Graya16(r) => (r.width(), r.height()),
                Rgba8(r) => (r.width(), r.height()), Rgba16(r) => (r.width(), r.height()),
            };
            println!("{{\"width\":{},\"height\":{}}}", width, height);
        }
        "lodepng" => {
            let image = lodepng::decode32_file(&args[2])?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width, image.height, image.buffer[0].r);
        }
        "zune-png" => {
            let mut decoder = zune_png::PngDecoder::new(Cursor::new(&bytes));
            let pixels = decoder.decode_raw()?;
            let (width, height) = decoder.dimensions().ok_or("missing PNG dimensions")?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", width, height, pixels[0]);
        }
        "load_image" => {
            let image = load_image::load_data(&bytes)?;
            println!("{{\"width\":{},\"height\":{}}}", image.width, image.height);
        }
        "gufo-png" => {
            let image = gufo_png::Png::new(bytes).map_err(|error| format!("{error:?}"))?;
            let title = image.chunks().into_iter()
                .find(|chunk| chunk.chunk_type() == gufo_png::ChunkType::tEXt)
                .ok_or("missing PNG tEXt chunk")?;
            let (key, value) = title.text()?;
            println!("{{\"key\":\"{}\",\"value\":\"{}\"}}", String::from_utf8_lossy(key), String::from_utf8_lossy(value));
        }
        "minipng" => {
            let header = minipng::decode_png_header(&bytes)?;
            let mut buffer = vec![0; header.required_bytes_rgba8bpc()];
            let mut image = minipng::decode_png(&bytes, &mut buffer)?;
            image.convert_to_rgba8bpc()?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width(), image.height(), image.pixels()[0]);
        }
        "png-decoder" => {
            let (header, pixels) = png_decoder::decode(&bytes).map_err(|error| format!("{error:?}"))?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", header.width, header.height, pixels[0][0]);
        }
        "oxideav-png" => {
            let image = oxideav_png::decode(&bytes)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width(), image.height(), image.to_rgba8()[0]);
        }
        "rusty_png" => {
            let decoder = rusty_png::Decoder::new(Cursor::new(&bytes));
            let mut reader = decoder.read_info()?;
            let mut buffer = vec![0; reader.output_buffer_size()];
            let frame = reader.next_frame(&mut buffer)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", frame.width, frame.height, buffer[0]);
        }
        "imagefmt" => {
            let image = imagefmt::read_from(&mut Cursor::new(&bytes), imagefmt::ColFmt::RGBA)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.w, image.h, image.buf[0]);
        }
        "zenpng" => {
            let image = zenpng::decode(&bytes, &zenpng::PngDecodeConfig::default(), &enough::Unstoppable)?;
            println!("{{\"width\":{},\"height\":{}}}", image.info.width, image.info.height);
        }
        "spng" => {
            let (info, pixels) = spng::decode(Cursor::new(&bytes), spng::Format::Rgba8)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", info.width, info.height, pixels[0]);
        }
        "wml2" => {
            let image = wml2::draw::image_from_file(args[2].clone())?;
            let red = image.buffer.as_ref().ok_or("missing PNG pixel buffer")?[0];
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width, image.height, red);
        }
        "nopng" => {
            let image = nopng::decode_image(&bytes)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width.get(), image.height.get(), image.pixels[0]);
        }
        "pb-imgsize" => {
            let image = pb_imgsize::read_bytes(&bytes).map_err(|error| format!("{error:?}"))?;
            println!("{{\"width\":{},\"height\":{}}}", image.width, image.height);
        }
        "png-spark" => {
            let image = png_spark::decode(&bytes)?;
            let red = image.to_rgba8()?[0];
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width(), image.height(), red);
        }
        "makepad-zune-png" => {
            let mut decoder = makepad_zune_png::PngDecoder::new(bytes.as_slice());
            let pixels = decoder.decode_raw()?;
            println!("{{\"red_0_0\":{},\"pixel_bytes\":{}}}", pixels[0], pixels.len());
        }
        "format-png" => {
            let image = format_png::decode_rgba8(&bytes)?;
            println!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width(), image.height(), image.data()[0]);
        }
        _ => return Err(format!("unknown PNG package: {name}").into()),
    }
    Ok(())
}
