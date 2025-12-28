# SS PSVITA Tool 🎮📖

**A specialized tool for extracting game scripts from SS Series PSVita Games for translation purposes**

*Developed by Sunnie Evergale*

---

## 🎯 Targeted Games

This tool is specifically designed for the **SS Series** on PlayStation Vita:

- **VLJM-35379** - [Game Title 1]
- **VLJM-35390** - [Game Title 2]  
- **VLJM-35391** - [Game Title 3]

*Note: May work with other similar SS engine Vita games*


## Quick Start

```bash
# Decompress sn.bin (using yetireg_tools)
python3 yetireg_tools/extract_snbin.py PCSG00917_decrypted/data/sn.bin

# Extract all dialogue
python3 extract_snbin_scripts.py . extracted_scripts

# Search for specific text
grep -r "検索テキスト" extracted_scripts/
```



## Game Information

| Field | Value |
|-------|-------|
| Title | Starry☆Sky ～Autumn Stories～ |
| Platform | PlayStation Vita |
| Product ID | PCSG00917 |
| Publisher | honeybee |
| Engine | Yeti/Regista game engine |
| Release Date | 2012 |

## Technical Details

- **Compression**: LZ77 variant (LZSS, N=4096, F=18)
- **Text Encoding**: Shift-JIS (CP932)
- **Format**: Yeti/Regista opcodescript bytecode

## Documentation

See [`docs/STASKY_PSV_DOCUMENTATION.md`](docs/STASKY_PSV_DOCUMENTATION.md) for complete documentation including:
- Full extraction process
- Technical specifications
- Validation results
- Troubleshooting guide

## Support

If you found this project helpful, consider supporting my work:

[![ko-fi](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXpoa2NnaHdhNDl2ajNneXFkemxzbzhxdm1nYXZiYTNsazlxeHJkZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/DzBUMIyTeHDuigQOoh/giphy.gif)](https://ko-fi.com/sunnieevergale)

## Credits

| Contribution | Source |
|--------------|--------|
| Project lead & development | Sunnie Evergale |
| yetireg_tools | mchubby (https://github.com/mchubby/yetireg_tools) |
| LZSS algorithm | Haruhiko Okumura (1989) |
| Vita game decryption | Vitamin/VitaminDec |
| Luna Translator | HIllya51 (https://docs.lunatranslator.org/en/) |
| Extraction assistance | Claude (Anthropic) |

## ⚠️ Disclaimer
This tool is for educational and preservation purposes only. You must own legitimate copies of the games. Not for piracy or commercial use.

## License

This project is for educational and research purposes.

---

**Date**: 2025-12-29
**Status**: ✅ COMPLETE
