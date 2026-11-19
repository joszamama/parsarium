# Minimal ISO BMFF / MP4: ftyp, moov and one mdat, plus optional free boxes.
# A file holds an H.264 video track (one 2x2 IDR frame), an AAC audio track
# (nine samples of one second of 8 kHz mono silence), or both. moov may end
# with iTunes-style metadata (udta/meta/hdlr mdir/ilst). The mdat goes either
# after moov or between ftyp and moov; with both tracks, the video sample comes
# before or after the audio chunk. Every box size is a 32-bit big-endian field
# that a constraint ties to the box's own byte length, and each stco chunk
# offset is tied to its sample's position in the file; Fandango repairs these
# fields directly.
#
# The SPS/PPS (avcC), the IDR slice, the AAC sample entry (mp4a, esds, btrt),
# the audio sample tables and the audio sample bytes are copied byte for byte
# from controls/mp4/red-av.mp4 (FFmpeg/libx264/AAC). The ilst layout follows
# the control's udta.

import struct

def u32(n):
    return struct.pack('>I', n)

# Byte offset of the first node named `name` inside `node`, or None.
def locate(node, name, base=0):
    if str(node.symbol) == name:
        return base
    for child in node.children:
        found = locate(child, name, base)
        if found is not None:
            return found
        base += len(bytes(child))
    return None

def find(node, name):
    if str(node.symbol) == name:
        return node
    for child in node.children:
        found = find(child, name)
        if found is not None:
            return found
    return None

# File offset of a track's sample data.
def chunk_offset(start, name):
    offset = locate(start, name)
    return u32(offset if offset is not None else 0)

# The audio media lasts 9024 samples at 8000 Hz; express that in the movie
# timescale, rounded up.
AUDIO_MEDIA_DURATION = 9024
AUDIO_RATE = 8000

def audio_track_duration(timescale):
    scale = int.from_bytes(bytes(timescale), 'big')
    return u32(-(-AUDIO_MEDIA_DURATION * scale // AUDIO_RATE))

# The movie lasts as long as its longest track.
def movie_duration(start, timescale):
    durations = []
    video = find(start, '<vmdhd>')
    if video is not None:
        durations.append(int.from_bytes(bytes(find(video, '<duration>')), 'big'))
    if find(start, '<atrak>') is not None:
        durations.append(int.from_bytes(audio_track_duration(timescale), 'big'))
    return u32(max(durations) if durations else 0)

# Track IDs are fixed: video 1, audio 2. Files with one track still use
# next_track_ID 3.
<start> ::= <ftyp> <free>? <v_moov> <free>? <v_mdat> | <ftyp> <free>? <v_mdat> <v_moov> <free>? | <ftyp> <free>? <a_moov> <free>? <a_mdat> | <ftyp> <free>? <a_mdat> <a_moov> <free>? | <ftyp> <free>? <av_moov> <free>? <av_mdat> | <ftyp> <free>? <av_mdat> <av_moov> <free>?

<size> ::= <byte>{4}

# File type box
<ftyp> ::= <size> b'ftyp' <brand> b'\x00\x00\x00\x00' <brand>{1,4}
<brand> ::= b'isom' | b'iso2' | b'mp41' | b'mp42' | b'avc1'

# Movie boxes: video only, audio only, or video and audio.
<v_moov> ::= <size> b'moov' <mvhd> <vtrak> <udta>?
<a_moov> ::= <size> b'moov' <mvhd> <atrak> <udta>?
<av_moov> ::= <size> b'moov' <mvhd> <vtrak> <atrak> <udta>?
<mvhd> ::= <size> b'mvhd' b'\x00\x00\x00\x00' <time> <time> <timescale> <movie_duration> b'\x00\x01\x00\x00' b'\x01\x00' b'\x00'{10} <matrix> b'\x00'{24} b'\x00\x00\x00\x03'

# Video track
<vtrak> ::= <size> b'trak' <vtkhd> <vmdia>
<vtkhd> ::= <size> b'tkhd' b'\x00\x00\x00\x03' <time> <time> b'\x00\x00\x00\x01' b'\x00\x00\x00\x00' <track_duration> b'\x00'{8} b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' <matrix> <dimension> <dimension>
<vmdia> ::= <size> b'mdia' <vmdhd> <vhdlr> <vminf>
<vmdhd> ::= <size> b'mdhd' b'\x00\x00\x00\x00' <time> <time> <timescale> <duration> <language> b'\x00\x00'
<vhdlr> ::= <size> b'hdlr' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'vide' b'\x00'{12} <vhandler_name>
<vminf> ::= <size> b'minf' <vmhd> <dinf> <vstbl>
<vmhd> ::= <size> b'vmhd' b'\x00\x00\x00\x01' b'\x00'{8}
<dinf> ::= <size> b'dinf' <dref>
<dref> ::= <size> b'dref' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' <url>
<url> ::= <size> b'url ' b'\x00\x00\x00\x01'

# Video sample tables: one sample in one chunk, lasting the whole track.
<vstbl> ::= <size> b'stbl' <vstsd> <vstts> <vstsc> <vstsz> <vstco>
<vstsd> ::= <size> b'stsd' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' <avc1>
<vstts> ::= <size> b'stts' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' b'\x00\x00\x00\x01' <duration>
<vstsc> ::= <size> b'stsc' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' b'\x00\x00\x00\x01' b'\x00\x00\x00\x01' b'\x00\x00\x00\x01'
<vstsz> ::= <size> b'stsz' b'\x00\x00\x00\x00' <sample_size> b'\x00\x00\x00\x01'
<vstco> ::= <size> b'stco' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' <chunk_offset>
<sample_size> ::= <byte>{4}
<chunk_offset> ::= <byte>{4}

# Visual sample entry: data reference 1, 2x2 coded size (fixed by the SPS),
# 72 dpi, one frame per sample, depth 24.
<avc1> ::= <size> b'avc1' b'\x00'{6} b'\x00\x01' b'\x00'{16} b'\x00\x02\x00\x02' b'\x00\x48\x00\x00\x00\x48\x00\x00' b'\x00\x00\x00\x00' b'\x00\x01' <compressor_name> b'\x00\x18\xff\xff' <avcC> <pasp>?
<compressor_name> ::= b'\x00'{32} | b'\x09Parsarium' b'\x00'{22} | b'\x0aAVC Coding' b'\x00'{21}
<avcC> ::= <size> b'avcC' (b'\x01\xf4\x00\x0a\xff\xe1\x00\x18\x67\xf4\x00\x0a\xae\xb4\xfc\x44\x46\x02\x20\x00\x00\x03\x00\x20'
                         b'\x00\x00\x03\x00\x41\xe2\x44\xd4\x01\x00\x05\x68\xce\x01\xaf\x20\xfd\xf8\xf8\x00')
# Pixel aspect ratio, square pixels
<pasp> ::= <size> b'pasp' b'\x00\x00\x00\x01' b'\x00\x00\x00\x01'

# Audio track: enabled and in movie, alternate group 1, full volume.
<atrak> ::= <size> b'trak' <atkhd> <amdia>
<atkhd> ::= <size> b'tkhd' b'\x00\x00\x00\x03' <time> <time> b'\x00\x00\x00\x02' b'\x00\x00\x00\x00' <track_duration> b'\x00'{8} b'\x00\x00\x00\x01' b'\x01\x00\x00\x00' <matrix> b'\x00'{8}
<amdia> ::= <size> b'mdia' <amdhd> <ahdlr> <aminf>
# Media timescale 8000 (the sample rate), duration 9024 samples.
<amdhd> ::= <size> b'mdhd' b'\x00\x00\x00\x00' <time> <time> b'\x00\x00\x1f\x40' b'\x00\x00\x23\x40' <language> b'\x00\x00'
<ahdlr> ::= <size> b'hdlr' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'soun' b'\x00'{12} <ahandler_name>
<aminf> ::= <size> b'minf' <smhd> <dinf> <astbl>
<smhd> ::= <size> b'smhd' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00'

# Audio sample tables: nine samples in one chunk, eight of 1024 PCM frames and
# a last one of 832.
<astbl> ::= <size> b'stbl' <astsd> <astts> <astsc> <astsz> <astco>
<astsd> ::= <size> b'stsd' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' <mp4a>
<astts> ::= <size> b'stts' b'\x00\x00\x00\x00' b'\x00\x00\x00\x02' b'\x00\x00\x00\x08' b'\x00\x00\x04\x00' b'\x00\x00\x00\x01' b'\x00\x00\x03\x40'
<astsc> ::= <size> b'stsc' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' b'\x00\x00\x00\x01' b'\x00\x00\x00\x09' b'\x00\x00\x00\x01'
<astsz> ::= <size> b'stsz' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'\x00\x00\x00\x09' b'\x00\x00\x00\x13' b'\x00\x00\x00\x04'{8}
<astco> ::= <size> b'stco' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' <chunk_offset>

# Audio sample entry: data reference 1, mono, 16-bit, 8000 Hz; AAC-LC
# decoder configuration and bitrate box from the control.
<mp4a> ::= <size> b'mp4a' b'\x00'{6} b'\x00\x01' b'\x00'{8} b'\x00\x01\x00\x10' b'\x00\x00\x00\x00' b'\x1f\x40\x00\x00' <esds> <btrt>?
<esds> ::= <size> b'esds' (b'\x00\x00\x00\x00\x03\x80\x80\x80\x25\x00\x02\x00\x04\x80\x80\x80\x17\x40\x15\x00\x00\x00\x00\x00'
                         b'\x3e\x80\x00\x00\x01\x69\x05\x80\x80\x80\x05\x15\x88\x56\xe5\x00\x06\x80\x80\x80\x01\x02')
<btrt> ::= <size> b'btrt' b'\x00\x00\x00\x00\x00\x00\x3e\x80\x00\x00\x01\x69'

# iTunes-style metadata: one to five of title, artist, album, date and track
# number, in that order. Text items are UTF-8 (data type 1); trkn is binary
# (data type 0).
<udta> ::= <size> b'udta' <meta>
<meta> ::= <size> b'meta' b'\x00\x00\x00\x00' <mhdlr> <ilst>
<mhdlr> ::= <size> b'hdlr' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'mdir' b'appl' b'\x00'{8} b'\x00'
<ilst> ::= <size> b'ilst' <items>
<items> ::= <inam> <iart>? <ialb>? <iday>? <itrkn>? | <iart> <ialb>? <iday>? <itrkn>? | <ialb> <iday>? <itrkn>? | <iday> <itrkn>? | <itrkn>
<inam> ::= <size> b'\xa9nam' <tdata>
<iart> ::= <size> b'\xa9ART' <tdata>
<ialb> ::= <size> b'\xa9alb' <tdata>
<iday> ::= <size> b'\xa9day' <ddata>
<itrkn> ::= <size> b'trkn' <ndata>
<tdata> ::= <size> b'data' b'\x00\x00\x00\x01' b'\x00\x00\x00\x00' <text>
<ddata> ::= <size> b'data' b'\x00\x00\x00\x01' b'\x00\x00\x00\x00' <date>
<ndata> ::= <size> b'data' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'\x00\x00' <track_number> <track_total> b'\x00\x00'

# One to three words separated by single spaces; a word may hold one
# two- or three-byte UTF-8 character.
<text> ::= <word> (b' ' <word>){0,2}
<word> ::= <alnum>{1,8} | <alnum>{0,3} <utf8_char> <alnum>{0,3}
<alnum> ::= rb'[A-Za-z0-9]'
<utf8_char> ::= b'\xc3\xa9' | b'\xc3\xb1' | b'\xc3\xbc' | b'\xc3\x9f' | b'\xd0\x96' | b'\xe6\x97\xa5'
<date> ::= <year> | <year> b'-' <month> b'-' <day_of_month>
<year> ::= (b'19' | b'20') rb'[0-9]' rb'[0-9]'
<month> ::= b'0' rb'[1-9]' | b'1' rb'[0-2]'
<day_of_month> ::= b'0' rb'[1-9]' | b'1' rb'[0-9]' | b'2' rb'[0-8]'
# Track 1..9 of 0 (unknown) or 10..20 tracks.
<track_number> ::= b'\x00' rb'[\x01-\x09]'
<track_total> ::= b'\x00\x00' | b'\x00' rb'[\x0a-\x14]'

# Media data: the video access unit, the audio chunk, or both.
<v_mdat> ::= <size> b'mdat' <sample>
<a_mdat> ::= <size> b'mdat' <aac_chunk>
<av_mdat> ::= <size> b'mdat' (<sample> <aac_chunk> | <aac_chunk> <sample>)

# One access unit of 4-byte length-prefixed NAL units, an optional access
# unit delimiter (I slices) followed by the IDR slice.
<sample> ::= <aud>? <idr>
<aud> ::= b'\x00\x00\x00\x02\x09\x10'
<idr> ::= (b'\x00\x00\x02\x5b\x65\x88\x84\xa0\xc6\x00\x08\x00\x02\x07\xa0\x00\x20\x42\x00\x34\x1d\x3d\x3d\x3d'
           b'\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x00\x07\x00\x01\x03\xd0\x00\x10\x21\x00\x1a\x0e\x9e\x9e\x9e'
           b'\x9e\x9e\x9e\x9e\x9e\x9e\x9e\x9e\xf0\x00\x02\x07\xa0\x00\x20\x42\x00\x34\x1d\x3d\x3d\x3d\x3d\x3d'
           b'\x3d\x3d\x3d\x3d\x3d\x3d\xe0\x00\x04\x0f\x40\x00\x40\x84\x00\x68\x3a\x7a\x7a\x7a\x7a\x7a\x7a\x7a'
           b'\x7a\x7a\x7a\x7b\xc0\x00\x08\x1e\x80\x00\x81\x08\x00\xd0\x74\xf4\xf4\xf4\xf4\xf4\xf4\xf4\xf4\xf4'
           b'\xf4\xf7\x80\x00\x10\x3d\x00\x01\x02\x10\x01\xa0\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xef'
           b'\x00\x00\x20\x7a\x00\x02\x04\x20\x03\x41\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xde\x00\x00'
           b'\x40\xf4\x00\x04\x08\x40\x06\x83\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xbc\x00\x00\x81\xe8'
           b'\x00\x08\x10\x80\x0d\x07\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x78\x00\x01\x03\xd0\x00\x10'
           b'\x21\x00\x1a\x0e\x9e\x9e\x9e\x9e\x9e\x9e\x9e\x9e\x9e\x9e\x9e\xf0\x00\x02\x07\xa0\x00\x20\x42\x00'
           b'\x34\x1d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\x3d\xe0\x00\x04\x0f\x40\x00\x40\x84\x00\x68\x3a'
           b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7b\xc0\x00\x08\x1e\x80\x00\x81\x08\x00\xd0\x74\xf4\xf4'
           b'\xf4\xf4\xf4\xf4\xf4\xf4\xf4\xf4\xf7\x80\x00\x10\x3d\x00\x01\x02\x10\x01\xa0\xe9\xe9\xe9\xe9\xe9'
           b'\xe9\xe9\xe9\xe9\xe9\xe9\xef\x00\x00\x20\x7a\x00\x02\x04\x20\x03\x41\xd3\xd3\xd3\xd3\xd3\xd3\xd3'
           b'\xd3\xd3\xd3\xd3\xde\x00\x00\x40\xf4\x00\x04\x08\x40\x06\x83\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7'
           b'\xa7\xa7\xbc\x00\x00\x81\xe8\x00\x08\x10\x80\x0d\x07\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x4f'
           b'\x42\x00\x01\x02\xb0\x00\x10\x0f\x00\x58\x6c\x20\x00\x10\xbe\x00\x01\x0a\x20\x00\x10\x66\x00\x07'
           b'\x80\x01\xc0\x00\x40\xac\x00\x04\x03\xc0\x16\x1b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\xe0'
           b'\x00\x04\x0a\xc0\x00\x40\x3c\x01\x61\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xbe\x00\x00\x40'
           b'\xac\x00\x04\x03\xc0\x16\x1b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\x2b\xe0\x00\x04\x0a\xc0\x00'
           b'\x40\x3c\x01\x61\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb2\xb0\x00\x70\x00\x10\xbe\x00\x01\x0a'
           b'\x20\x00\x10\x66\x00\x07\x80\xf8\x5e\x17\x85\xe1\x78\x5e\x17\x85\xe1\x78\x5e\x17\xb8\x00\x01\x0b'
           b'\xe0\x00\x10\xa2\x00\x01\x06\x60\x00\x78\x0f\x85\xe1\x78\x5e\x17\x85\xe1\x78\x5e\x17\x85\xe1\x7b'
           b'\x80\x00\x10\xbe\x00\x01\x0a\x20\x00\x10\x66\x00\x07\x80\xf8\x5e\x17\x85\xe1\x78\x5e\x17\x85\xe1'
           b'\x78\x5e\x17\xb8\x00\x01\x0b\xe0\x00\x10\xa2\x00\x01\x06\x60\x00\x78\x0f\x85\xe1\x78\x5e\x17\x85'
           b'\xe1\x78\x5e\x17\x85\xe1\x7a')

# The audio chunk: nine raw AAC frames (19 bytes, then eight of 4 bytes).
<aac_chunk> ::= (b'\xdc\x00\x4c\x61\x76\x63\x36\x33\x2e\x31\x2e\x31\x30\x32\x00\x02\x30\x40\x0e'
                 b'\x01\x18\x20\x07\x01\x18\x20\x07\x01\x18\x20\x07\x01\x18\x20\x07'
                 b'\x01\x18\x20\x07\x01\x18\x20\x07\x01\x18\x20\x07\x01\x18\x20\x07')

<free> ::= <size> b'free' <byte>{0,16}

# Field values
<time> ::= b'\x00\x00\x00\x00' | b'\xe0' <byte>{3}
<timescale> ::= b'\x00\x00\x02\x58' | b'\x00\x00\x03\xe8' | b'\x00\x00\x75\x30' | b'\x00\x01\x5f\x90'
<duration> ::= b'\x00\x00' rb'[\x01-\xff]' <byte>
# Movie and track durations are computed by constraints.
<movie_duration> ::= <byte>{4}
<track_duration> ::= <byte>{4}
<matrix> ::= b'\x00\x01\x00\x00' b'\x00'{12} b'\x00\x01\x00\x00' b'\x00'{12} b'\x40\x00\x00\x00'
# 16.16 fixed point, integer part 1..255 (Exiv2 rejects zero dimensions)
<dimension> ::= b'\x00' rb'[\x01-\xff]' b'\x00\x00'
<language> ::= b'\x55\xc4' | b'\x15\xc7' | b'\x19\x4c'
<vhandler_name> ::= b'\x00' | b'VideoHandler\x00' | b'Parsarium\x00'
<ahandler_name> ::= b'\x00' | b'SoundHandler\x00' | b'Parsarium\x00'

where <ftyp>.<size> == u32(len(bytes(<ftyp>)))
where <v_moov>.<size> == u32(len(bytes(<v_moov>)))
where <a_moov>.<size> == u32(len(bytes(<a_moov>)))
where <av_moov>.<size> == u32(len(bytes(<av_moov>)))
where <mvhd>.<size> == u32(len(bytes(<mvhd>)))
where <vtrak>.<size> == u32(len(bytes(<vtrak>)))
where <vtkhd>.<size> == u32(len(bytes(<vtkhd>)))
where <vmdia>.<size> == u32(len(bytes(<vmdia>)))
where <vmdhd>.<size> == u32(len(bytes(<vmdhd>)))
where <vhdlr>.<size> == u32(len(bytes(<vhdlr>)))
where <vminf>.<size> == u32(len(bytes(<vminf>)))
where <vmhd>.<size> == u32(len(bytes(<vmhd>)))
where <dinf>.<size> == u32(len(bytes(<dinf>)))
where <dref>.<size> == u32(len(bytes(<dref>)))
where <url>.<size> == u32(len(bytes(<url>)))
where <vstbl>.<size> == u32(len(bytes(<vstbl>)))
where <vstsd>.<size> == u32(len(bytes(<vstsd>)))
where <avc1>.<size> == u32(len(bytes(<avc1>)))
where <avcC>.<size> == u32(len(bytes(<avcC>)))
where <pasp>.<size> == u32(len(bytes(<pasp>)))
where <vstts>.<size> == u32(len(bytes(<vstts>)))
where <vstsc>.<size> == u32(len(bytes(<vstsc>)))
where <vstsz>.<size> == u32(len(bytes(<vstsz>)))
where <vstco>.<size> == u32(len(bytes(<vstco>)))
where <atrak>.<size> == u32(len(bytes(<atrak>)))
where <atkhd>.<size> == u32(len(bytes(<atkhd>)))
where <amdia>.<size> == u32(len(bytes(<amdia>)))
where <amdhd>.<size> == u32(len(bytes(<amdhd>)))
where <ahdlr>.<size> == u32(len(bytes(<ahdlr>)))
where <aminf>.<size> == u32(len(bytes(<aminf>)))
where <smhd>.<size> == u32(len(bytes(<smhd>)))
where <astbl>.<size> == u32(len(bytes(<astbl>)))
where <astsd>.<size> == u32(len(bytes(<astsd>)))
where <mp4a>.<size> == u32(len(bytes(<mp4a>)))
where <esds>.<size> == u32(len(bytes(<esds>)))
where <btrt>.<size> == u32(len(bytes(<btrt>)))
where <astts>.<size> == u32(len(bytes(<astts>)))
where <astsc>.<size> == u32(len(bytes(<astsc>)))
where <astsz>.<size> == u32(len(bytes(<astsz>)))
where <astco>.<size> == u32(len(bytes(<astco>)))
where <udta>.<size> == u32(len(bytes(<udta>)))
where <meta>.<size> == u32(len(bytes(<meta>)))
where <mhdlr>.<size> == u32(len(bytes(<mhdlr>)))
where <ilst>.<size> == u32(len(bytes(<ilst>)))
where <inam>.<size> == u32(len(bytes(<inam>)))
where <iart>.<size> == u32(len(bytes(<iart>)))
where <ialb>.<size> == u32(len(bytes(<ialb>)))
where <iday>.<size> == u32(len(bytes(<iday>)))
where <itrkn>.<size> == u32(len(bytes(<itrkn>)))
where <tdata>.<size> == u32(len(bytes(<tdata>)))
where <ddata>.<size> == u32(len(bytes(<ddata>)))
where <ndata>.<size> == u32(len(bytes(<ndata>)))
where <v_mdat>.<size> == u32(len(bytes(<v_mdat>)))
where <a_mdat>.<size> == u32(len(bytes(<a_mdat>)))
where <av_mdat>.<size> == u32(len(bytes(<av_mdat>)))
where <free>.<size> == u32(len(bytes(<free>)))
# The video media uses the movie timescale; its track, media and sample
# durations agree. The audio track duration is the audio media duration in
# the movie timescale, and the movie lasts as long as its longest track.
where <vmdhd>.<timescale> == bytes(<mvhd>.<timescale>)
where <vtkhd>.<track_duration> == bytes(<vmdhd>.<duration>)
where <vstts>.<duration> == bytes(<vmdhd>.<duration>)
where <atkhd>.<track_duration> == audio_track_duration(<mvhd>.<timescale>)
where <mvhd>.<movie_duration> == movie_duration(<start>, <mvhd>.<timescale>)
# The video sample is the whole access unit; each stco points at its track's
# data in mdat.
where <vstsz>.<sample_size> == u32(len(bytes(<sample>)))
where <vstco>.<chunk_offset> == chunk_offset(<start>, '<sample>')
where <astco>.<chunk_offset> == chunk_offset(<start>, '<aac_chunk>')
