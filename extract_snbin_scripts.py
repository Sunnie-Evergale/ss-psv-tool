#!/usr/bin/env python3
"""
Starry☆Sky Vita Script Extractor
Extracts dialogue text from decompressed sn.bin opcodescript files.
"""

import os
import sys
from pathlib import Path
from struct import unpack


class ScriptExtractor:
    """Extract text from Yeti/Regista opcodescript files."""

    def __init__(self, opcodescript_path: str):
        self.opcodescript_path = Path(opcodescript_path)
        self._data = None

    @property
    def data(self) -> bytes:
        """Raw file data."""
        if self._data is None:
            with open(self.opcodescript_path, 'rb') as f:
                self._data = f.read()
        return self._data

    def extract_strings(self, min_length: int = 5) -> list:
        """
        Extract Shift-JIS strings from opcodescript file.

        Args:
            min_length: Minimum string length to include

        Returns:
            List of (offset, text) tuples
        """
        data = self.data
        results = []
        used = set()
        i = 0

        while i < len(data) - min_length:
            if i in used:
                i += 1
                continue

            b = data[i]

            # Shift-JIS lead byte or ASCII
            is_sjis_lead = (0x81 <= b <= 0x9F) or (0xE0 <= b <= 0xEF)
            is_ascii = 0x20 <= b <= 0x7E

            if is_sjis_lead or is_ascii:
                start = i
                chars = []
                j = i

                while j < len(data):
                    b1 = data[j]

                    if b1 == 0x00:
                        break

                    if (0x81 <= b1 <= 0x9F) or (0xE0 <= b1 <= 0xEF):
                        if j + 1 < len(data):
                            chars.extend([b1, data[j+1]])
                            j += 2
                        else:
                            break
                    elif 0x20 <= b1 <= 0x7E:
                        chars.append(b1)
                        j += 1
                    else:
                        break

                if j > start and len(chars) >= min_length:
                    try:
                        text = bytes(chars).decode('shift-jis')
                        # Clean up text
                        clean = ''.join(
                            c if c.isprintable() or c in '「」『』\n\t' else ' '
                            for c in text
                        )
                        clean = ' '.join(clean.split())

                        # Check for meaningful content
                        has_japanese = any(ord(c) > 127 for c in clean)
                        is_meaningful = (
                            len(clean) >= min_length and
                            not clean.isdigit() and
                            (has_japanese or any(c.isalpha() for c in clean))
                        )

                        if is_meaningful:
                            results.append((start, clean))
                            # Mark bytes as used
                            for k in range(start, j):
                                used.add(k)
                    except:
                        pass

            i += 1

        return results

    def extract_dialogue(self) -> list:
        """
        Extract dialogue strings (Japanese text longer than 8 chars).

        Returns:
            List of (offset, text) tuples
        """
        all_strings = self.extract_strings(min_length=3)

        # Filter for dialogue-like content
        dialogue = []
        for offset, text in all_strings:
            # Has Japanese characters and reasonable length
            has_japanese = any(ord(c) > 127 for c in text)
            is_long_enough = len(text) >= 8

            # Skip obvious non-dialogue (labels, codes, etc.)
            if text.startswith(('I', 'AA_', 'after', 'Lunar')):
                continue

            if has_japanese and is_long_enough:
                dialogue.append((offset, text))

        return dialogue


def extract_all_scripts(input_dir: str = ".", output_dir: str = "extracted_scripts"):
    """
    Extract text from all opcodescript files.

    Args:
        input_dir: Directory containing opcodescript files
        output_dir: Directory for output text files
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all opcodescript files
    script_files = sorted(input_path.glob("z__sn-*.opcodescript"))

    if not script_files:
        print(f"No opcodescript files found in {input_dir}")
        return

    print(f"Found {len(script_files)} opcodescript files")
    print(f"Output directory: {output_path.absolute()}")
    print()

    total_dialogue = 0

    for script_file in script_files:
        print(f"Processing {script_file.name}...", end=' ')

        extractor = ScriptExtractor(script_file)
        dialogue = extractor.extract_dialogue()

        if dialogue:
            # Write to output file
            output_file = output_path / f"{script_file.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for offset, text in dialogue:
                    f.write(f"[0x{offset:06X}] {text}\n")

            total_dialogue += len(dialogue)
            print(f"{len(dialogue)} dialogue lines -> {output_file.name}")
        else:
            print("no dialogue found")

    print()
    print(f"Total dialogue lines extracted: {total_dialogue}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_snbin_scripts.py <opcodescript_file|directory> [output_dir]")
        print()
        print("Examples:")
        print("  python extract_snbin_scripts.py z__sn-000.opcodescript")
        print("  python extract_snbin_scripts.py . extracted_scripts")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "extracted_scripts"

    input_p = Path(input_path)

    if input_p.is_file() and input_p.suffix == '.opcodescript':
        # Single file mode
        extractor = ScriptExtractor(input_p)
        dialogue = extractor.extract_dialogue()

        print(f"Extracted {len(dialogue)} dialogue lines from {input_p.name}")

        output_file = Path(output_dir) / f"{input_p.stem}.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            for offset, text in dialogue:
                f.write(f"[0x{offset:06X}] {text}\n")

        print(f"Output: {output_file}")

    elif input_p.is_dir():
        # Directory mode - extract all scripts
        extract_all_scripts(input_path, output_dir)
    else:
        print(f"Error: {input_path} is not a valid opcodescript file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
