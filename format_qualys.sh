#!/bin/bash
# Qualys Formatter Quick Launcher
# Usage: ./format_qualys.sh <input_file> [output_prefix] [format]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORMATTER="$SCRIPT_DIR/qualys_formatter/qualys_formatter.py"

INPUT_FILE="$1"
OUTPUT_PREFIX="${2:-qualys_report}"
FORMAT="${3:-html}"

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <input_file> [output_prefix] [format]"
    echo ""
    echo "Examples:"
    echo "  $0 my_scan.xml"
    echo "  $0 my_scan.csv my_report all"
    echo "  $0 my_scan.json security_assessment html"
    echo ""
    echo "Formats: html, csv, json, all"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

if [ ! -f "$FORMATTER" ]; then
    echo "Error: Formatter script not found at '$FORMATTER'"
    exit 1
fi

echo "Processing Qualys report: $INPUT_FILE"
echo "Output prefix: $OUTPUT_PREFIX"
echo "Format: $FORMAT"
echo ""

python3 "$FORMATTER" "$INPUT_FILE" -o "$OUTPUT_PREFIX" -f "$FORMAT"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Report generation completed successfully!"
    
    case "$FORMAT" in
        "html"|"all")
            echo "📊 HTML Dashboard: ${OUTPUT_PREFIX}.html"
            ;;
    esac
    
    case "$FORMAT" in
        "csv"|"all")
            echo "📋 CSV Summary: ${OUTPUT_PREFIX}_summary.csv"
            ;;
    esac
    
    case "$FORMAT" in
        "json"|"all")
            echo "🔧 JSON Export: ${OUTPUT_PREFIX}.json"
            ;;
    esac
else
    echo "❌ Report generation failed!"
    exit 1
fi