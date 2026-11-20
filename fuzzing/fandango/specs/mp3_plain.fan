# Plain MP3: one untagged MPEG-1 or MPEG-2 Layer III stream, with no ID3v2
# tag, no ID3v1 trailer and no Layer I or II frames.
#
# Every frame of a file has the same MPEG version, sample rate, channel
# mode, mode extension, flags and protection (CRC) bit. A file is constant
# bitrate (every frame repeats the first frame's bitrate; only the padding
# bit may differ) or variable bitrate (each frame picks its own bitrate
# index). A file has 5 to 60 audio frames, optionally preceded by a Xing
# ("Xing" for VBR, "Info" for CBR) frame that carries the audio frame count
# and the stream byte count. Files with a Xing frame have no CRC, so the tag
# sits where readers look for it. The side information and main data are
# zeros: every granule has part2_3_length 0 and decodes to silence. Each
# frame's length follows from its header: 144000 * kbps / rate (MPEG-1) or
# 72000 * kbps / rate (MPEG-2), plus the padding bit. A protected frame's
# CRC-16 (poly 0x8005, init 0xFFFF) covers header bytes 3 and 4 and the side
# information. The derived bytes are where constraints that Fandango repairs.
# The audio grammar is the same as in mp3_tagged.fan.

BITRATES = {3: (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
            2: (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)}
RATES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000)}
FRAMES = ('<frame0>', '<cbr>', '<vbr>')

def crc16(data):
    crc = 0xffff
    for value in data:
        crc ^= value << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x8005) if crc & 0x8000 else crc << 1
            crc &= 0xffff
    return crc

def header(hdr):
    data = bytes(hdr)
    return data[1], data[2], data[3]

def frame_length(b1, b2):
    version = (b1 >> 3) & 3
    rate = RATES[version][(b2 >> 2) & 3]
    kbps = BITRATES[version][b2 >> 4]
    return (144000 if version == 3 else 72000) * kbps // rate + ((b2 >> 1) & 1)

def side_length(b1, b3):
    mono = (b3 >> 6) == 3
    if (b1 >> 3) & 3 == 3:
        return 17 if mono else 32
    return 9 if mono else 17

# CRC-16 field: empty when the protection bit is 1 (no CRC).
def crc_field(hdr):
    b1, b2, b3 = header(hdr)
    if b1 & 1:
        return b''
    return crc16(bytes([b2, b3]) + bytes(side_length(b1, b3))).to_bytes(2, 'big')

# Zero side information and main data up to the frame length.
def body(hdr):
    b1, b2, _ = header(hdr)
    return bytes(frame_length(b1, b2) - 4 - (0 if b1 & 1 else 2))

# Bitrate byte of a later frame: the first frame's sample rate, the frame's
# own bitrate (VBR) or the first frame's bitrate (CBR), the frame's own padding.
def vbr_b2(first, mine):
    return bytes([(bytes(mine)[0] & 0xf2) | (bytes(first)[0] & 0x0c)])

def cbr_b2(first, mine):
    return bytes([(bytes(mine)[0] & 0x02) | (bytes(first)[0] & 0xfc)])

# Xing frame header byte: the first frame's sample rate and the first frame's
# bitrate, raised to the lowest bitrate whose frame holds the Xing fields.
def xing_b2(first, xb1, xb3):
    b1, b3 = bytes(xb1)[0], bytes(xb3)[0]
    value = bytes(first)[0] & 0xfc
    need = 4 + side_length(b1, b3) + 16
    while frame_length(b1, value) < need:
        value += 0x10
    return bytes([value])

def find_all(node, names, found):
    if str(node.symbol) in names:
        found.append(node)
        return found
    for child in node.children:
        find_all(child, names, found)
    return found

# Side information (zeros), "Xing" or "Info", flags (frames and bytes), the
# audio frame count, the byte count of all MPEG frames including this one,
# then zeros to the frame length.
def xing_body(start, xhdr):
    b1, b2, b3 = header(xhdr)
    frames = find_all(start, FRAMES, [])
    total = frame_length(b1, b2) + sum(len(bytes(frame)) for frame in frames)
    kinds = {bytes(frame)[2] >> 4 for frame in frames}
    side = side_length(b1, b3)
    fields = (b'Info' if len(kinds) == 1 else b'Xing') + (3).to_bytes(4, 'big') \
        + len(frames).to_bytes(4, 'big') + total.to_bytes(4, 'big')
    return bytes(side) + fields + bytes(max(0, frame_length(b1, b2) - 4 - side - len(fields)))

<start> ::= <audio>

# ---------------------------------------------------------------- audio
<audio> ::= <xing> <frame0> <cbr>{4,59} | <xing> <frame0> <vbr>{4,59} | <frame0> <cbr>{4,59} | <frame0> <vbr>{4,59}
<frame0> ::= <hdr> <crc> <body>
<cbr> ::= <hdr> <crc> <body>
<vbr> ::= <hdr> <crc> <body>
<xing> ::= <xhdr> <xbody>

# Header: sync, then MPEG-1 (0xFB/0xFA) or MPEG-2 (0xF3/0xF2) Layer III with
# (0xFA, 0xF2) or without a CRC. Bitrate byte: index 1-14, sample rate index
# 0-2, padding 0 or 1, private bit 0. Mode byte: stereo, joint stereo with
# mode extension 0-3, dual channel or mono, original bit 0 or 1, no
# emphasis.
<hdr> ::= b'\xff' <b1> <b2> <b3>
<xhdr> ::= b'\xff' <xb1> <b2> <b3>
<b1> ::= b'\xfb' | b'\xfa' | b'\xf3' | b'\xf2'
<xb1> ::= b'\xfb' | b'\xf3'
<b2> ::= rb'[\x10\x12\x14\x16\x18\x1a\x20\x22\x24\x26\x28\x2a\x30\x32\x34\x36\x38\x3a\x40\x42\x44\x46\x48\x4a\x50\x52\x54\x56\x58\x5a\x60\x62\x64\x66\x68\x6a\x70\x72\x74\x76\x78\x7a\x80\x82\x84\x86\x88\x8a\x90\x92\x94\x96\x98\x9a\xa0\xa2\xa4\xa6\xa8\xaa\xb0\xb2\xb4\xb6\xb8\xba\xc0\xc2\xc4\xc6\xc8\xca\xd0\xd2\xd4\xd6\xd8\xda\xe0\xe2\xe4\xe6\xe8\xea]'
<b3> ::= rb'[\x00\x04]' | rb'[\x40\x44\x50\x54\x60\x64\x70\x74]' | rb'[\x80\x84]' | rb'[\xc0\xc4]'
<crc> ::= rb'([\x00-\xff]{2})?'
<body> ::= rb'\x00*'
<xbody> ::= rb'[\x00-\xff]*'

where <frame0>.<hdr>.<b1> == bytes(<xing>.<xhdr>.<xb1>)
where <xing>.<xhdr>.<b3> == bytes(<frame0>.<hdr>.<b3>)
where <xing>.<xhdr>.<b2> == xing_b2(<frame0>.<hdr>.<b2>, <xing>.<xhdr>.<xb1>, <xing>.<xhdr>.<b3>)
where <cbr>.<hdr>.<b1> == bytes(<frame0>.<hdr>.<b1>)
where <vbr>.<hdr>.<b1> == bytes(<frame0>.<hdr>.<b1>)
where <cbr>.<hdr>.<b3> == bytes(<frame0>.<hdr>.<b3>)
where <vbr>.<hdr>.<b3> == bytes(<frame0>.<hdr>.<b3>)
where <cbr>.<hdr>.<b2> == cbr_b2(<frame0>.<hdr>.<b2>, <cbr>.<hdr>.<b2>)
where <vbr>.<hdr>.<b2> == vbr_b2(<frame0>.<hdr>.<b2>, <vbr>.<hdr>.<b2>)
where <frame0>.<crc> == crc_field(<frame0>.<hdr>)
where <cbr>.<crc> == crc_field(<cbr>.<hdr>)
where <vbr>.<crc> == crc_field(<vbr>.<hdr>)
where <frame0>.<body> == body(<frame0>.<hdr>)
where <cbr>.<body> == body(<cbr>.<hdr>)
where <vbr>.<body> == body(<vbr>.<hdr>)
where <xing>.<xbody> == xing_body(<start>, <xing>.<xhdr>)
