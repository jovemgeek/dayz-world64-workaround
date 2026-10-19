"""Exact-build, copy-only DayZ dedicated server World arena workaround."""
import argparse
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = "67dea3d44a5956cc4f57e9ecce91a64c9e7ee9cdfff0de52a65e4cae46f7ff20"
OUTPUT_SHA256 = "e5575fdeeeb4649432841f768d47f637a2ad34286eed11482d42601a85273ab6"
SIZE = 24849464
OFFSET = 0xA4E734
SITES = {0xA4E662: 2, 0xA4E6C8: 32, 0xA4E72D: 32, 0xA4E78E: 32}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def transform(raw):
    if len(raw) != SIZE or digest(raw) != SOURCE_SHA256:
        raise ValueError("Unsupported executable: exact original build SHA-256 required")
    for offset, mib in SITES.items():
        expected = bytes.fromhex("c7442420") + (mib * 1024 * 1024).to_bytes(4, "little")
        if raw[offset:offset + 8] != expected:
            raise ValueError("Instruction verification failed")
    data = bytearray(raw)
    data[OFFSET] = 4
    if digest(data) != OUTPUT_SHA256:
        raise ValueError("Unexpected output SHA-256")
    return bytes(data)


def patch(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    manifest = output.with_suffix(".manifest.json")
    if source in (output, manifest) or output == manifest:
        raise ValueError("Source, output and manifest must be different paths")
    if output.exists() or manifest.exists():
        raise ValueError("Output or manifest already exists; refusing overwrite")
    raw = source.read_bytes()
    data = transform(raw)
    record = {
        "status": "EXPERIMENTAL_WORKAROUND",
        "source_sha256": SOURCE_SHA256, "output_sha256": OUTPUT_SHA256,
        "file_size": SIZE, "changed_byte_offset": hex(OFFSET),
        "old_byte": "02", "new_byte": "04",
        "module": "World", "old_capacity_bytes": 33554432,
        "new_capacity_bytes": 67108864,
        "authenticode": "Original publisher signature no longer matches modified file",
    }
    # Exclusive creation prevents overwriting a file created after our checks.
    # Partial new artifacts may remain after an I/O failure; never install those.
    with manifest.open("x", encoding="utf-8") as meta:
        with output.open("xb") as executable:
            executable.write(data)
        if digest(output.read_bytes()) != OUTPUT_SHA256:
            raise ValueError("Written output failed verification; do not install")
        if source.read_bytes() != raw:
            raise ValueError("Source changed concurrently; do not install output")
        json.dump(record, meta, indent=2)
        meta.write("\n")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Original DayZServer_x64.exe")
    parser.add_argument("--output", required=True, help="New copy in an existing directory")
    args = parser.parse_args()
    try:
        print(json.dumps(patch(args.source, args.output), indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
