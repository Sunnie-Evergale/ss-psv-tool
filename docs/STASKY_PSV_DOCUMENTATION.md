# Sta☆Sky Script Extraction - Complete Documentation


##  ☕ Support

If you found this project helpful, consider supporting my work:

[![ko-fi](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXpoa2NnaHdhNDl2ajNneXFkemxzbzhxdm1nYXZiYTNsazlxeHJkZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/DzBUMIyTeHDuigQOoh/giphy.gif)](https://ko-fi.com/sunnieevergale)


---

## 🗜️Executive Summary

**Successfully extracted 12,732 dialogue lines** from (PCSG00917) using community tools for the Yeti/Regista game engine.

---


## Overview

### Game Information

| Field | Value |
|-------|-------|
| **Title** | Starry☆Sky ～Autumn Stories～ |
| **Platform** | PlayStation Vita |
| **Product ID** | PCSG00917 |
| **Publisher** | Honeybee Parade / Honeybee Royal |
| **Engine** | Yeti/Regista game engine |
| **Release Date** | 2012 |

### Project Goal

Extract clean Japanese dialogue text from Vita game scripts **without** using the encrypted `eboot.bin` file.

---

## The Breakthrough

### Discovery: yetireg_tools

After multiple failed attempts with custom LZ77 decompression, we discovered the **yetireg_tools** repository by mchubby - a collection of tools specifically designed for games using the "Yeti" and "Regista" game engine.

**Repository**: https://github.com/mchubby/yetireg_tools

### Why This Worked

1. **Engine Compatibility**: Starry☆Sky uses the honeybee, which is based on Yeti/Regista
2. **Same Compression Format**: The Vita version uses the same LZ77 compression as PSP/Xbox 360 versions
3. **Proven Tools**: Community tools already existed for this exact format

---

## Extraction Process

### Step 1: Clone yetireg_tools

```bash
git clone https://github.com/mchubby/yetireg_tools.git
```

### Step 2: Decompress sn.bin

The `sn.bin` file (2.4 MB) is a compressed LZ77 archive containing all game scripts.

```bash
# Copy sn.bin to working directory
cp PCSG00917_decrypted/data/sn.bin sn.bin

# Decompress using yetireg_tools
python3 yetireg_tools/extract_snbin.py sn.bin
```

**Output:**
- `sn.ccpak` - Decompressed archive (7.5 MB)
- `z__sn-000.opcodescript` through `z__sn-795.opcodescript` - 796 bytecode script files

**What happened:**
- The first 4 bytes of `sn.bin` (`0x00771590` = 7,804,304) specify the decompressed size
- LZ77 decompression (N=4096, F=18) is applied to the remaining data
- The decompressed data is parsed into 796 script entries

### Step 3: Extract Dialogue from Opcodescripts

Created custom script `extract_snbin_scripts.py` to parse the opcodescript files and extract Shift-JIS dialogue strings.

```bash
# Extract all dialogue
python3 extract_snbin_scripts.py . extracted_scripts
```

**Output:**
- `extracted_scripts/z__sn-000.txt` through `extracted_scripts/z__sn-795.txt`
- Total: **12,732 dialogue lines**

### Step 4: Validate Results

```bash
# Search for known Luna text phrases
grep -r "夏が終わった" extracted_scripts/
```

**Result:** ✅ All Luna reference text found in extracted files!

---

## Results

### Extraction Statistics

| Metric | Count |
|--------|-------|
| **Total opcodescript files** | 796 |
| **Total dialogue lines extracted** | 12,732 |
| **Combined file size** | ~2 MB |
| **Decompression ratio** | ~3.2:1 (2.4 MB → 7.8 MB) |

### Top Files by Dialogue Count

| File | Dialogue Lines | Description |
|------|----------------|-------------|
| `z__sn-000.txt` | 1,356 | Main story opening |
| `z__sn-032.txt` | 165 | Character route |
| `z__sn-001.txt` | 163 | Early game |
| `z__sn-038.txt` | 143 | Character route |
| `z__sn-193.txt` | 141 | Character route |

### Sample Extracted Text

```
[0x00F4E6] 夏が終わった――%Nそう実感した瞬間はいつだっただろう？
[0x00F535] 夏休みが終わった日？ %N星空がなんだか寂しいと感じた日？
[0x00F585] それとも……。
[0x00F5AB] 今なら分かる。
[0x00F5D1] 私はあの瞬間に、%N新しい季節の訪れを肌で感じた――
[0x00F752] インターハイも無事に終わり、%N弓道部内もリラックスムードだったあの日。
[0x00F7B0] 部活が終わった後、私は１人残って弓を引いていた。
[0x00F835] 「あっ、もう下校時刻だ。%N弓道場の鍵を先生の所に持って行かないと！」
```

---

## File Structure

### Input Files

```
PCSG00917_decrypted/
├── data/
│   ├── sn.bin (2.4 MB) - Compressed script archive
│   └── sys/
│       ├── 00000 (2.3 MB)
│       ├── 00001 (1.9 MB)
│       └── ... (14 files)
```

### Output Files

```
Projects/cpk-unpack/
├── sn.ccpak (7.5 MB) - Decompressed archive
├── z__sn-000.opcodescript through z__sn-795.opcodescript (796 files)
├── extracted_scripts/
│   ├── z__sn-000.txt (1,356 lines)
│   ├── z__sn-001.txt (163 lines)
│   └── ... (796 files total, 12,732 dialogue lines)
├── extract_snbin_scripts.py - Main extraction script
└── docs/
    └── STASKY_PSV_DOCUMENTATION.md - This documentation
```

---

## Usage Instructions

### Quick Start

```bash
# 1. Decompress sn.bin
python3 /path/to/yetireg_tools/extract_snbin.py PCSG00917_decrypted/data/sn.bin

# 2. Extract all dialogue
python3 extract_snbin_scripts.py . extracted_scripts

# 3. Search for specific text taken from Luna Translator + Vita3K emulator
grep -r "検索テキスト" extracted_scripts/
```

### Extract Single File

```bash
python3 extract_snbin_scripts.py z__sn-000.opcodescript
```

This creates `z__sn-000.txt` in the current directory.

### Extract All Scripts

```bash
python3 extract_snbin_scripts.py /path/to/opcodescripts /path/to/output
```

### Find Specific Character Dialogue

```bash
# Find all lines containing a character name
grep -r "水嶋" extracted_scripts/
grep -r "星月" extracted_scripts/
grep -r "陽日" extracted_scripts/
```

---

## Technical Details

### Compression Format

**Algorithm**: LZ77 variant (LZSS)
- **N**: 4096 (dictionary size)
- **F**: 18 (match length + threshold)
- **Reference**: Haruhiko Okumura's LZSS implementation (1989)

### File Format

#### sn.bin Structure

```
Offset 0x00-0x03: Decompressed size (little-endian uint32)
Offset 0x04+:    LZ77 compressed data
```

Example:
```
90 15 77 00 = 0x00771590 = 7,804,304 bytes (decompressed size)
```

#### sn.ccpak Structure

```
Offset 0x00-0x03: Max offset (little-endian uint32)
Offset 0x04+:    Entry table (16 bytes per entry)
  - Offset (4 bytes)
  - Size (4 bytes)
  - Unknown (8 bytes)
Offset variable: Script data entries
```

#### .opcodescript Structure

```
Offset 0x00-0x03: First code offset (little-endian uint32)
Offset 0x04+:    Opcodes and embedded Shift-JIS strings
```

### Text Encoding

| Character Type | Encoding |
|----------------|----------|
| **Japanese** | Shift-JIS (CP932) |
| **ASCII** | 0x20-0x7E |
| **Lead bytes** | 0x81-0x9F, 0xE0-0xEF |
| **Trail bytes** | 0x40-0xFC |

### Control Codes

| Code | Purpose |
|------|---------|
| `%N` | Line break / pause |
| `「」` | Dialogue quotes |
| `『』` | Inner quotes |

---

## Tools Created

### extract_snbin_scripts.py

**Purpose**: Main extraction script for opcodescript files

**Features**:
- Extracts Shift-JIS strings from bytecode
- Filters for dialogue-like content (Japanese text > 8 chars)
- Processes single files or entire directories
- Creates formatted output with hex offsets

**Usage**:
```bash
python3 extract_snbin_scripts.py <input> [output_dir]

# Single file
python3 extract_snbin_scripts.py z__sn-000.opcodescript

# Directory
python3 extract_snbin_scripts.py . extracted_scripts
```

**Key Methods**:
- `extract_strings()`: Raw string extraction
- `extract_dialogue()`: Filtered dialogue extraction

---

## Validation

### Luna Translator Comparison

| Luna Reference | Extracted Text | Status |
|-----------------|---------------|--------|
| 夏が終わった――そう実感した瞬間は... | 夏が終わった――%Nそう実感した瞬間は... | ✅ MATCH |
| インターハイも無事に終わり... | インターハイも無事に終わり... | ✅ MATCH |
| 弓道部内もリラックスムードだったあの日 | 弓道部内もリラックスムードだったあの日 | ✅ MATCH |
| 保健室 | 保健室 | ✅ MATCH |
| 保健室のベッドは寝心地が悪いね | 保健室のベッドは寝心地が悪いね | ✅ MATCH |

**Validation Result**: ✅ **All test phrases found in extracted text**

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'struct'"

**Solution**: The `struct` module is built-in to Python. This error usually indicates a different problem. Check your Python version:

```bash
python3 --version  # Should be 3.x
```

#### Issue: "Opcodescript file not found"

**Solution**: Ensure you decompressed `sn.bin` first:

```bash
python3 yetireg_tools/extract_snbin.py sn.bin
ls z__sn-*.opcodescript  # Should show 796 files
```

#### Issue: Extracted text is garbled

**Solution**: This usually means:
1. The file wasn't properly decompressed
2. The file isn't actually an opcodescript file

Check the file header:
```bash
xxd -l 16 z__sn-000.opcodescript
```

Should show a valid offset at bytes 0x00-0x03.

#### Issue: "No dialogue extracted"

**Solution**: Not all opcodescript files contain dialogue. Some only have labels or function names. This is expected behavior.

---

## Comparison with Previous Attempts

| Method | Result | Why It Failed |
|--------|--------|---------------|
| Direct Shift-JIS scan on bytecode | ❌ Garbled output | Text is compressed with LZ77 |
| [char][marker] pair decoding | ❌ Only labels/function names | Wrong interpretation of bytecode |
| Luna Translator hooking | ✅ Works | Runtime decompression by game engine |
| **yetireg_tools + custom extractor** | ✅ **12,732 lines** | **Proper LZ77 decompression + SJIS extraction** |

---

## Key Learnings

### What Worked

1. **Community tools are invaluable** - The yetireg_tools repository had the exact solution needed
2. **Cross-platform compatibility exists** - Vita version uses same format as PSP/Xbox 360
3. **Shift-JIS extraction over opcode parsing** - Direct string extraction more reliable than parsing unknown opcodes

### What Didn't Work

1. **Custom LZ77 implementation** - Without knowing exact format parameters
2. **Opcode-based parsing** - Vita has different opcodes than PSP
3. **Direct file scanning** - Text is compressed, not stored as plain text

---

## Future Enhancements

### Potential Improvements

1. **Control Code Processing**
   - Remove `%N` and other control codes
   - Format text for readability

2. **Character Organization**
   - Group dialogue by character
   - Separate routes/scenes

3. **Translation Support**
   - Create translation patch files
   - Generate side-by-side translation format

4. **PC Version Comparison**
   - Compare with PC version scripts
   - Map differences between platforms

---


## Credits

| Contribution | Source |
|--------------|--------|
| **Project lead & development** | Sunnie Evergale |
| **yetireg_tools** | mchubby (https://github.com/mchubby/yetireg_tools) |
| **LZSS algorithm** | Haruhiko Okumura (1989) |
| **Vita game decryption** | Vitamin/VitaminDec |
| **Luna Translator** | HIllya51 (https://github.com/HIllya51/LunaTranslator) |
| **Extraction assistance** | Claude (Anthropic) |


---



## Conclusion

The extraction was **successful**! By leveraging existing community tools for the Yeti/Regista game engine, we overcame the initial challenges with the custom bytecode format.

### Key Achievements

✅ **12,732 dialogue lines** extracted from 796 script files
✅ **Clean Japanese text** with proper encoding
✅ **Validated** against Luna Translator reference text
✅ **Documented** complete process for future use

### Demonstrated Principles

1. **Static extraction IS possible** without eboot.bin analysis
2. **Community tools** are often the best starting point
3. **Cross-version compatibility** exists between PSP/Xbox 360 and Vita for this engine

---


##  ☕ Support the developers efforts
[https://ko-fi.com/sunnieevergale](https://ko-fi.com/sunnieevergale)
