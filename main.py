#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 make.fun bounty entry.

Verifies entry.png rigorously with the standard library only, delivers it
to /output/entry.png, re-inspects the delivered copy, and repeats the whole
delivery once more, requiring byte-identical results both times.

Checks on the PNG:
  * file size <= 1 MiB
  * 8-byte PNG signature
  * first chunk is IHDR declaring 1024x1024
  * every chunk's stored CRC-32 matches zlib.crc32(type + data)
  * the joined IDAT payload zlib-decompresses cleanly
  * an IEND chunk is present and is the last chunk, with no trailing bytes

Exit code 0 and an OK line on success; non-zero with a stderr message on
any failure. No network access.
"""
import hashlib
import os
import shutil
import struct
import sys
import zlib

MAX_BYTES = 1024 * 1024  # 1 MiB
EXPECTED_W = 1024
EXPECTED_H = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
OUTPUT_PATH = "/output/entry.png"


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def inspect_png(path):
    """Return (size, sha256_hex) after fully validating the PNG at path."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")

    if len(data) > MAX_BYTES:
        fail(f"{path}: {len(data)} bytes exceeds the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        fail(f"{path}: missing PNG signature")

    pos = len(PNG_SIGNATURE)
    idat = bytearray()
    seen_iend = False
    first_chunk = True
    while pos < len(data):
        if pos + 8 > len(data):
            fail(f"{path}: truncated chunk header at offset {pos}")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        cstart = pos + 8
        cend = cstart + length
        if cend + 4 > len(data):
            fail(f"{path}: truncated chunk {ctype!r} at offset {pos}")
        cdata = data[cstart:cend]
        (stored_crc,) = struct.unpack(">I", data[cend:cend + 4])
        actual_crc = zlib.crc32(ctype + cdata) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail(f"{path}: CRC mismatch in chunk {ctype!r} at offset {pos}")

        if first_chunk:
            if ctype != b"IHDR":
                fail(f"{path}: first chunk is {ctype!r}, expected IHDR")
            if length != 13:
                fail(f"{path}: IHDR length {length}, expected 13")
            width, height = struct.unpack(">II", cdata[0:8])
            if (width, height) != (EXPECTED_W, EXPECTED_H):
                fail(f"{path}: IHDR declares {width}x{height}, "
                     f"expected {EXPECTED_W}x{EXPECTED_H}")
            first_chunk = False
        if ctype == b"IDAT":
            idat.extend(cdata)
        pos = cend + 4
        if ctype == b"IEND":
            seen_iend = True
            if pos != len(data):
                fail(f"{path}: {len(data) - pos} trailing bytes after IEND")
            break

    if first_chunk:
        fail(f"{path}: no chunks found")
    if not seen_iend:
        fail(f"{path}: no IEND chunk")
    if not idat:
        fail(f"{path}: no IDAT data")
    try:
        zlib.decompress(bytes(idat))
    except zlib.error as exc:
        fail(f"{path}: IDAT does not zlib-decompress: {exc}")

    return len(data), hashlib.sha256(data).hexdigest()


def deliver(source):
    """Copy source to the output path, re-inspect, return (size, sha256)."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    shutil.copyfile(source, OUTPUT_PATH)
    return inspect_png(OUTPUT_PATH)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.exists(source):
        source = os.path.join(os.getcwd(), "entry.png")
    if not os.path.exists(source):
        fail("entry.png not found next to main.py or in the working directory")

    src_size, src_sha = inspect_png(source)

    first = deliver(source)
    if first != (src_size, src_sha):
        fail("first delivery does not match the source bytes")
    second = deliver(source)
    if second != first:
        fail("second delivery differs from the first")

    print(f"OK: entry.png verified and delivered to {OUTPUT_PATH} "
          f"({src_size} bytes, sha256 {src_sha})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
