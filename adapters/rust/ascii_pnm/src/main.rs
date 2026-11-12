use serde_json::json;
use std::{
    env, fs,
    io::{BufReader, Cursor},
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        return Err("usage: parsarium-rust-ascii-pnm PACKAGE CONTROL.pnm".into());
    }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "image" => {
            let img = image::load_from_memory_with_format(&bytes, image::ImageFormat::Pnm)?;
            json!({"width": img.width(), "height": img.height(), "rgb": img.to_rgb8().into_raw()})
        }
        "imageun" => {
            let img = imageun::load_from_memory_with_format(&bytes, imageun::ImageFormat::Pnm)?;
            json!({"width": img.width(), "height": img.height(), "rgb": img.to_rgb8().into_raw()})
        }
        "imagesize" => {
            let size = imagesize::blob_size(&bytes)?;
            json!({"width": size.width, "height": size.height})
        }
        "bevy_image" => {
            let img = bevy_image::Image::from_buffer(
                &bytes,
                bevy_image::ImageType::Format(bevy_image::ImageFormat::Pnm),
                bevy_image::CompressedImageFormats::NONE,
                true,
                bevy_image::ImageSampler::default(),
                bevy_asset::RenderAssetUsages::default(),
            )?;
            json!({"width": img.width(), "height": img.height(), "rgba": img.data})
        }
        "bevy" => {
            let img = bevy::image::Image::from_buffer(
                &bytes,
                bevy::image::ImageType::Format(bevy::image::ImageFormat::Pnm),
                bevy::image::CompressedImageFormats::NONE,
                true,
                bevy::image::ImageSampler::default(),
                bevy_asset::RenderAssetUsages::default(),
            )?;
            json!({"width": img.width(), "height": img.height(), "rgba": img.data})
        }
        "ai-image" => {
            let img = ai_image::load_from_memory_with_format(&bytes, ai_image::ImageFormat::Pnm)?;
            json!({"width": img.width(), "height": img.height(), "rgb": img.to_rgb8().into_raw()})
        }
        "devela" => {
            let len = devela::Pnm::decoded_len_u8(&bytes).map_err(|e| format!("{e:?}"))?;
            let mut pixels = vec![0; len];
            let (size, channels) =
                devela::Pnm::decode_u8(&bytes, &mut pixels).map_err(|e| format!("{e:?}"))?;
            json!({"size": format!("{size:?}"), "channels": channels, "pixels": pixels})
        }
        "oxideav-pbm" => {
            #[allow(deprecated)]
            let (img, format) = oxideav_pbm::decode_pbm(&bytes)?;
            json!({"width": img.width(), "height": img.height(), "format": format!("{format:?}"), "rgb": img.to_rgb8()})
        }
        "oxideav-image" => {
            let mut ctx = oxideav_image::RuntimeContext::new();
            oxideav_pbm::registry::register(&mut ctx);
            let file = oxideav_image::decode_bytes(&ctx, &bytes)?;
            let img = file.primary();
            json!({"width": img.width(), "height": img.height(), "rgb": img.to_rgb8()?})
        }
        "oxideav-io" => {
            let mut ctx = oxideav_image::RuntimeContext::new();
            oxideav_pbm::registry::register(&mut ctx);
            let img = oxideav_io::open_image_with(
                &ctx,
                oxideav_io::Source::bytes(&bytes),
                &oxideav_io::OpenOptions::eager(),
            )?;
            json!({"width": img.width(), "height": img.height(), "rgb": img.to_rgb8()?})
        }
        "zenbitmaps" => {
            let img = zenbitmaps::decode(&bytes, enough::Unstoppable)?;
            json!({"width": img.width, "height": img.height, "layout": format!("{:?}", img.layout), "pixels": img.pixels()})
        }
        "coldiron" => {
            let img = coldiron::Image::read_from(&mut Cursor::new(&bytes))?;
            json!({"width": img.width(), "height": img.height(),
                   "format": format!("{:?}", img.format),
                   "pixels": [img.get_pixel(0, 0), img.get_pixel(1, 0)]})
        }
        "photocraft" => {
            let img = photocraft::Image::read_ppm(&mut BufReader::new(Cursor::new(&bytes)))?;
            json!({"width": img.width, "height": img.height,
                   "rgb": img.pixels.iter().flat_map(|p| [p.r, p.g, p.b]).collect::<Vec<_>>()})
        }
        "unicraft" => {
            let img = unicraft::photo::Image::read_ppm(&mut BufReader::new(Cursor::new(&bytes)))?;
            json!({"width": img.width, "height": img.height,
                   "rgb": img.pixels.iter().flat_map(|p| [p.r, p.g, p.b]).collect::<Vec<_>>()})
        }
        "libviprs" => {
            let img = libviprs::Raster::ppm_load(&bytes)?;
            json!({"width": img.width(), "height": img.height(), "rgb": img.data()})
        }
        "opencv-no-c-imgcodecs" => {
            use cv_core::MatLike;
            let img = cv_imgcodecs::pnm::decode(&bytes)?;
            json!({"width": img.cols(), "height": img.rows(), "bgr": img.as_bytes()})
        }
        "rusty-ppm" => {
            let path = std::path::Path::new(&args[2]);
            let canvas = rusty_ppm::ppm_reader::read_ppm(
                path,
                path.file_name()
                    .ok_or("control path has no name")?
                    .to_str()
                    .ok_or("non-UTF8 control path")?,
            )?;
            json!({"pixels": canvas.iter().map(|p| [p.x, p.y, p.z]).collect::<Vec<_>>()})
        }
        "roka-qr" => {
            let code = roka_qr::Reader::from_pbm(&bytes)?;
            json!({"size": code.size(), "payload": String::from_utf8(code.payload().to_vec())?})
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    println!("{output}");
    Ok(())
}
