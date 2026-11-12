use serde_json::{Value, json};
use std::{env, fs, path::Path};

// The component parsers accept an SVG path-data value, rather than a document.
// This extraction is deliberately limited to the checked-in valid control.
fn path_data(text: &str) -> Result<&str, Box<dyn std::error::Error>> {
    let after = text.split_once("<path d=\"").ok_or("control has no path")?.1;
    Ok(after.split_once('"').ok_or("path attribute is not closed")?.0)
}

fn size_usvg(tree: &usvg::Tree) -> Value {
    json!({"width": tree.size().width(), "height": tree.size().height(),
           "nodes": tree.root().children().len()})
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        return Err("usage: parsarium-rust-svg PACKAGE CONTROL.svg".into());
    }
    let package = args[1].as_str();
    let path = Path::new(&args[2]);
    let bytes = fs::read(path)?;
    let text = std::str::from_utf8(&bytes)?;
    let output = match package {
        "svgtypes" => {
            let segments: Vec<_> = svgtypes::PathParser::from(path_data(text)?)
                .collect::<Result<_, _>>()?;
            json!({"path_segments": segments.len(),
                   "first_command": (segments[0].command() as char).to_string()})
        }
        "svg_path_ops" => {
            let parsed = svg_path_ops::pt::PathTransformer::parse(path_data(text)?)?;
            json!({"serialized": parsed.to_string()})
        }
        "oxideav-svg" => {
            let doc = oxideav_svg::parse_from(bytes.as_slice())?;
            json!({"width": doc.width, "height": doc.height,
                   "nodes": doc.root.children.len()})
        }
        "oxvg_ast" => {
            oxvg_ast::parse::roxmltree::parse(text, |document, _allocator| {
                let root = document.child_nodes_iter().find_map(|node| node.element())
                    .expect("SVG control has no document element");
                json!({"root": root.local_name().to_string(),
                       "elements": root.child_element_count()})
            }).map_err(|e| format!("{e:?}"))?
        }
        "usvg" => size_usvg(&usvg::Tree::from_data(&bytes, &usvg::Options::default())?),
        "resvg" => {
            let tree = resvg::usvg::Tree::from_data(&bytes, &resvg::usvg::Options::default())?;
            let mut pixmap = resvg::tiny_skia::Pixmap::new(2, 1).ok_or("pixmap allocation")?;
            resvg::render(&tree, resvg::tiny_skia::Transform::identity(), &mut pixmap.as_mut());
            json!({"width": tree.size().width(), "height": tree.size().height(),
                   "rgba": pixmap.data()})
        }
        "svg" => {
            let mut content = String::new();
            let events = svg::open(path, &mut content)?;
            let mut rects = 0;
            let mut paths = 0;
            for event in events {
                match event {
                    svg::parser::Event::Tag("rect", _, _) => rects += 1,
                    svg::parser::Event::Tag("path", _, _) => paths += 1,
                    svg::parser::Event::Error(error) => return Err(error.into()),
                    _ => {}
                }
            }
            json!({"rects": rects, "paths": paths})
        }
        "usvg-parser" => {
            use usvg_parser::TreeParsing;
            let tree = usvg_tree::Tree::from_data(&bytes, &usvg_parser::Options::default())?;
            json!({"width": tree.size.width(), "height": tree.size.height()})
        }
        "svg-hush" => {
            let mut out = Vec::new();
            svg_hush::Filter::new().filter(bytes.as_slice(), &mut out)?;
            let filtered = std::str::from_utf8(&out)?;
            json!({"rects_retained": filtered.matches("<rect").count(),
                   "svg_retained": filtered.contains("<svg")})
        }
        "svgdom" => {
            let doc = svgdom::Document::from_str(text)?;
            let rects = doc.root().descendants()
                .filter(|node| node.has_tag_name(svgdom::ElementId::Rect)).count();
            json!({"rects": rects, "has_svg": doc.svg_element().is_some()})
        }
        "svgrtypes" => {
            let segments: Vec<_> = svgrtypes::PathParser::from(path_data(text)?)
                .collect::<Result<_, _>>()?;
            json!({"path_segments": segments.len(),
                   "first_command": (segments[0].command() as char).to_string()})
        }
        "usvgr" => {
            let tree = usvgr::Tree::from_data(&bytes, &usvgr::Options::default())?;
            json!({"width": tree.size().width(), "height": tree.size().height(),
                   "nodes": tree.root().children().len()})
        }
        "svgr" => {
            let tree = svgr::usvgr::Tree::from_data(&bytes, &svgr::usvgr::Options::default())?;
            let mut pixmap = svgr::tiny_skia::Pixmap::new(2, 1).ok_or("pixmap allocation")?;
            let mut cache = svgr::SvgrCache::none();
            let pool = svgr::PixmapPool::new();
            let context = svgr::Context::new_from_pixmap(&pixmap);
            svgr::render(&tree, svgr::tiny_skia::Transform::identity(),
                         &mut pixmap.as_mut(), &mut cache, &pool, &context);
            json!({"width": tree.size().width(), "height": tree.size().height(),
                   "rgba": pixmap.data()})
        }
        "oxvg_path" => {
            use oxvg_path::parser::Parse;
            let parsed = oxvg_path::Path::parse_string(path_data(text)?)
                .map_err(|e| format!("{e:?}"))?;
            json!({"path_commands": parsed.0.len(), "serialized": parsed.to_string()})
        }
        "svgparser" => {
            use svgparser::xmlparser::FromSpan;
            let mut rects = 0;
            for token in svgparser::svg::Tokenizer::from_str(text) {
                if let svgparser::svg::Token::ElementStart(name) = token.map_err(|e| format!("{e:?}"))? {
                    if name.local == svgparser::svg::Name::Svg(svgparser::ElementId::Rect) {
                        rects += 1;
                    }
                }
            }
            json!({"rects": rects})
        }
        "nsvg" => {
            let image = nsvg::SvgImage::parse_file(path, nsvg::Units::Pixel, 96.0)?;
            json!({"width": image.width(), "height": image.height()})
        }
        "svg_metadata" => {
            let metadata = svg_metadata::Metadata::parse_file(path.to_path_buf())?;
            let view_box = metadata.view_box.ok_or("missing viewBox")?;
            json!({"viewbox_width": view_box.width, "viewbox_height": view_box.height})
        }
        "spreet" => {
            let tree = spreet::load_svg(path)?;
            json!({"width": tree.size().width(), "height": tree.size().height(),
                   "nodes": tree.root().children().len()})
        }
        "ps-usvg" => {
            let tree = ps_usvg::Tree::from_data(&bytes, &ps_usvg::Options::default())?;
            json!({"width": tree.size().width(), "height": tree.size().height(),
                   "nodes": tree.root().children().len()})
        }
        "svgcleaner" => {
            let doc = svgcleaner::cleaner::parse_data(text, &svgcleaner::ParseOptions::default())?;
            let rects = doc.descendants()
                .filter(|node| node.tag_id() == Some(svgdom_old::ElementId::Rect)).count();
            json!({"rects": rects, "has_svg": doc.svg_element().is_some()})
        }
        "ferrigura-path" => {
            let bounds = ferrigura_path::bounding_box(path_data(text)?);
            json!({"x": bounds.x, "y": bounds.y,
                   "width": bounds.width, "height": bounds.height})
        }
        "librsvg" => {
            let handle = rsvg::Loader::new().read_path(path)?;
            let size = rsvg::CairoRenderer::new(&handle)
                .intrinsic_size_in_pixels().ok_or("SVG has no intrinsic pixel size")?;
            json!({"width": size.0, "height": size.1})
        }
        "vello_svg" => {
            let scene = vello_svg::render(text)?;
            json!({"paths": scene.encoding().n_paths,
                   "path_segments": scene.encoding().n_path_segments})
        }
        "anyrender_svg" => {
            let mut scene = anyrender::recording::Scene::new();
            anyrender_svg::render_svg_str(&mut scene, text, kurbo::Affine::IDENTITY)?;
            json!({"render_commands": scene.commands.len()})
        }
        "ps-anyrender-svg" => {
            let mut scene = ps_anyrender::recording::Scene::new();
            ps_anyrender_svg::render_svg_str(&mut scene, text, kurbo::Affine::IDENTITY)?;
            json!({"render_commands": scene.commands.len()})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    println!("{output}");
    Ok(())
}
