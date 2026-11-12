use serde_json::json;
use std::{env, fs};

#[derive(Default)]
struct UrlCapture {
    url: Vec<u8>,
    message_complete: bool,
}

impl http_muncher::ParserHandler for UrlCapture {
    fn on_url(&mut self, _: &mut http_muncher::Parser, data: &[u8]) -> bool {
        self.url.extend_from_slice(data);
        true
    }
    fn on_message_complete(&mut self, _: &mut http_muncher::Parser) -> bool {
        self.message_complete = true;
        true
    }
}

impl http_parser::HttpParserCallback for UrlCapture {
    fn on_url(&mut self, _: &mut http_parser::HttpParser, data: &[u8]) -> http_parser::CallbackResult {
        self.url.extend_from_slice(data);
        Ok(http_parser::ParseAction::None)
    }
    fn on_message_complete(&mut self, _: &mut http_parser::HttpParser) -> http_parser::CallbackResult {
        self.message_complete = true;
        Ok(http_parser::ParseAction::None)
    }
}

fn utf8(bytes: &[u8]) -> Result<&str, Box<dyn std::error::Error>> {
    Ok(std::str::from_utf8(bytes)?)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        return Err("usage: parsarium-rust-http11 PACKAGE CONTROL.http".into());
    }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "httparse" => {
            let mut headers = [httparse::EMPTY_HEADER; 16];
            let mut request = httparse::Request::new(&mut headers);
            let status = request.parse(&bytes)?;
            if !status.is_complete() { return Err("incomplete HTTP request".into()); }
            json!({"method": request.method, "target": request.path,
                   "minor": request.version, "headers": request.headers.len()})
        }
        "ntex-httparse" => {
            let mut request = ntex_httparse::Request::default();
            let status = request.parse(&bytes)?;
            if !status.is_complete() { return Err("incomplete HTTP request line".into()); }
            json!({"method": utf8(&bytes[request.method.start..request.method.end])?,
                   "target": utf8(&bytes[request.path.start..request.path.end])?,
                   "minor": request.version})
        }
        "shiguredo_http11" => {
            let mut decoder = shiguredo_http11::RequestDecoder::new();
            decoder.feed(&bytes)?;
            let request = decoder.decode()?.ok_or("incomplete HTTP request")?;
            json!({"method": request.method(), "target": request.uri(),
                   "version": request.version()})
        }
        "http-net" => {
            let mut fields = [http_net::FieldSpan::default(); 16];
            let parsed = http_net::parse_request_head(&bytes, &http_net::Limits::new(), &mut fields)?;
            let http_net::Parsed::Complete { head, .. } = parsed else {
                return Err("incomplete HTTP request head".into());
            };
            let view = head.view();
            json!({"method": view.method_str(), "target": view.target(),
                   "version": format!("{:?}", view.version())})
        }
        "blazingly-wire" => {
            let head = blazingly_wire::parse_request_head(&bytes, blazingly_wire::Limits::default())?
                .ok_or("incomplete HTTP request head")?;
            json!({"method": format!("{:?}", head.method),
                   "target": head.target.text(&bytes), "keep_alive": head.keep_alive})
        }
        "weida-http-codec" => {
            let (head, _) = weida_http_codec::h1::decode_request(&bytes, weida_http_codec::Limits::default())?;
            json!({"method": utf8(head.method)?, "target": utf8(head.target)?,
                   "minor": head.minor, "headers": head.fields.len()})
        }
        "http-kit-h1" => {
            let mut buffer = bytes::BytesMut::from(bytes.as_slice());
            let head = http_kit_h1::proto::parse_request_head(&mut buffer, &http_kit_h1::Limits::default())?
                .ok_or("incomplete HTTP request head")?;
            json!({"method": head.parts.method.as_str(),
                   "target": head.parts.uri.to_string(), "keep_alive": head.keep_alive})
        }
        "xibalba-proto" => {
            let mut headers = [const { xibalba_proto::header::Header::empty() }; 16];
            let (head, consumed) = xibalba_proto::response::ResponseHead::parse(&bytes, &mut headers)?;
            json!({"status": head.status.as_u16(), "headers": head.header_count,
                   "body": utf8(&bytes[consumed..])?})
        }
        "xocomil" => {
            let head = xocomil::request::Request::<16>::parse(&bytes)?;
            json!({"method": format!("{:?}", head.method()),
                   "target": utf8(head.path())?, "version": format!("{:?}", head.version())})
        }
        "thhp" => {
            let mut headers = Vec::<thhp::HeaderField>::with_capacity(16);
            let status = thhp::Request::parse(&bytes, &mut headers)?;
            let thhp::Status::Complete((head, _)) = status else {
                return Err("incomplete HTTP request head".into());
            };
            json!({"method": head.method, "target": head.target,
                   "minor": head.minor_version, "headers": head.headers.len()})
        }
        "minihttpse" => {
            let response = minihttpse::Response::new(bytes.clone())
                .map_err(|error| format!("{error:?}"))?;
            json!({"status": response.status_code(), "reason": response.reason(),
                   "body": response.text()})
        }
        "request-http-parser" => {
            let request = request_http_parser::parser::Request::new(utf8(&bytes)?)?;
            json!({"method": format!("{:?}", request.method), "path": request.path,
                   "query_x": request.params.as_ref().and_then(|params| params.get("x")),
                   "host": request.headers.get("host")})
        }
        "saf-httparser" => {
            let request = saf_httparser::request_from_bytes(&bytes)?;
            json!({"method": request.method().as_str(),
                   "target": request.uri().path_and_query().map(|value| value.as_str()),
                   "version": format!("{:?}", request.version())})
        }
        "sutegi-http" => {
            let mut reader = std::io::BufReader::new(std::io::Cursor::new(&bytes));
            let request = sutegi_http::parse_request(&mut reader, &sutegi_http::Limits::default())?
                .ok_or("incomplete HTTP request")?;
            let sutegi_http::Incoming::Request(request) = request else {
                return Err("request rejected by parser".into());
            };
            json!({"method": request.method.as_str(), "path": request.path,
                   "query": request.query, "version": request.version})
        }
        "zenith-http1" => {
            let (response, _) = zenith_http1::parse_response(&bytes)
                .map_err(|error| format!("{error:?}"))?
                .ok_or("incomplete HTTP response")?;
            json!({"status": response.status, "headers": response.headers.len(),
                   "body": utf8(&response.body)?})
        }
        "stream-httparse" => {
            let mut parser = stream_httparse::streaming_parser::ReqParser::new_capacity(256);
            let (complete, _) = parser.block_parse(&bytes);
            if !complete { return Err("incomplete HTTP request".into()); }
            let request = parser.finish().map_err(|error| format!("{error:?}"))?;
            json!({"method": format!("{:?}", request.method()),
                   "target": request.path(), "protocol": request.protocol()})
        }
        "h11r" => {
            let mut connection = h11r::Connection::new(h11r::Role::Server, h11r::Limits::default());
            connection.receive_data(&bytes)?;
            let h11r::NextEvent::Event(h11r::Event::Request(request)) = connection.next_event()? else {
                return Err("no parsed HTTP request event".into());
            };
            json!({"method": format!("{:?}", request.method),
                   "target": utf8(&request.target)?, "version": format!("{:?}", request.http_version)})
        }
        "webparse" => {
            let mut request = webparse::Request::<()>::new();
            let consumed = request.parse(&bytes).map_err(|error| format!("{error:?}"))?;
            json!({"method": request.method().to_string(),
                   "target": request.url().to_string(), "consumed": consumed})
        }
        "async-h1" => {
            let mut response = futures_lite::future::block_on(
                async_h1::client::decode(futures_lite::io::Cursor::new(bytes.clone())))?;
            let status = response.status() as u16;
            let body = futures_lite::future::block_on(response.body_string())?;
            json!({"status": status, "body": body})
        }
        "async-http-codec" => {
            let (_, head) = futures::executor::block_on(
                async_http_codec::RequestHead::decode(futures::io::Cursor::new(bytes.clone())))?;
            json!({"method": head.method().as_str(), "target": head.uri().to_string(),
                   "version": format!("{:?}", head.version()), "headers": head.headers().len()})
        }
        "http-muncher" => {
            let mut parser = http_muncher::Parser::request();
            let mut capture = UrlCapture::default();
            let consumed = parser.parse(&mut capture, &bytes);
            if parser.has_error() || !capture.message_complete || consumed != bytes.len() {
                return Err(format!("HTTP request parsing incomplete: {}", parser.error()).into());
            }
            let (major, minor) = parser.http_version();
            json!({"method": parser.http_method(), "target": utf8(&capture.url)?,
                   "version": format!("{major}.{minor}"), "consumed": consumed})
        }
        "http_parser" => {
            let mut parser = http_parser::HttpParser::new(http_parser::HttpParserType::Request);
            let mut capture = UrlCapture::default();
            let consumed = parser.execute(&mut capture, &bytes);
            if parser.errno.is_some() || !capture.message_complete || consumed != bytes.len() {
                return Err("HTTP request parsing incomplete".into());
            }
            json!({"method": parser.method.map(|method| method.to_string()),
                   "target": utf8(&capture.url)?,
                   "version": parser.http_version.to_string(), "consumed": consumed})
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    println!("{output}");
    Ok(())
}
