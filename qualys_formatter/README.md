# Qualys Vulnerability Report Formatter

A comprehensive tool for formatting and visualizing Qualys vulnerability reports with beautiful HTML dashboards, CSV summaries, and JSON exports.

## Features

- **Multi-format support**: Parse XML, CSV, and JSON Qualys reports
- **Beautiful HTML Dashboard**: Interactive charts and responsive design
- **Summary Statistics**: Vulnerability counts, severity distribution, and host analysis
- **Multiple Export Formats**: HTML, CSV, and JSON outputs
- **CVSS Score Analysis**: Categorized vulnerability scoring
- **Top Vulnerabilities**: Most common issues across your environment
- **Host-based Analysis**: Identify most vulnerable systems

## Installation

No additional dependencies required - uses Python standard library and CDN resources for charts.

```bash
# Make the script executable
chmod +x qualys_formatter.py
```

## Usage

### Basic Usage

```bash
# Generate HTML report from XML
python3 qualys_formatter.py sample_data/sample_qualys_report.xml

# Generate HTML report from CSV
python3 qualys_formatter.py sample_data/sample_qualys_report.csv -o my_report

# Generate all formats
python3 qualys_formatter.py sample_data/sample_qualys_report.json -f all
```

### Command Line Options

```bash
python3 qualys_formatter.py [-h] [-o OUTPUT] [-f {html,csv,json,all}] input_file

positional arguments:
  input_file            Path to the Qualys report file (XML, CSV, or JSON)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file prefix (default: qualys_report)
  -f FORMAT, --format FORMAT
                        Output format (default: html)
                        Choices: html, csv, json, all
```

### Examples

```bash
# Generate HTML dashboard
python3 qualys_formatter.py my_qualys_scan.xml

# Generate CSV summary only
python3 qualys_formatter.py my_qualys_scan.csv -f csv -o vulnerability_summary

# Generate all formats with custom prefix
python3 qualys_formatter.py my_qualys_scan.json -f all -o security_assessment_2024
```

## Supported Input Formats

### XML Format
- Standard Qualys XML vulnerability reports
- ASSET_DATA_REPORT format
- Custom XML structures with HOST/VULN elements

### CSV Format
- Comma or semicolon delimited
- Flexible column mapping for common field names
- Headers: IP, QID, Title, Severity, CVSS Score, Category, Port, Protocol, CVE, Solution, Results

### JSON Format
- Structured JSON with vulnerability arrays
- Supports nested objects and various JSON schemas
- Flexible field mapping

## Output Formats

### HTML Dashboard
- **Interactive charts** using Chart.js
- **Responsive design** for mobile and desktop
- **Color-coded severity levels**
- **Summary cards** with key metrics
- **Detailed vulnerability table** with filtering capabilities
- **Professional styling** suitable for executive reports

### CSV Summary
- High-level statistics and metrics
- Severity distribution breakdown
- Top 10 most common vulnerabilities
- Host vulnerability counts
- Easy to import into spreadsheet applications

### JSON Export
- Complete structured data export
- Metadata and summary statistics
- Full vulnerability details
- Machine-readable format for further processing

## Visualization Features

### Dashboard Sections

1. **Summary Cards**
   - Total vulnerability count
   - Unique host count  
   - Critical and high severity counts

2. **Interactive Charts**
   - Severity distribution (doughnut chart)
   - CVSS score ranges (bar chart)
   - Responsive and mobile-friendly

3. **Vulnerability Table**
   - Sortable columns
   - Color-coded severity badges
   - Truncated descriptions with full details on hover
   - First 100 vulnerabilities for performance

4. **Professional Styling**
   - Modern CSS with gradients and shadows
   - Color-coded severity levels
   - Hover effects and animations
   - Print-friendly design

## Sample Data

The `sample_data/` directory contains example reports in all supported formats:

- `sample_qualys_report.xml` - XML format with multiple hosts and vulnerabilities
- `sample_qualys_report.csv` - CSV format with common vulnerability types
- `sample_qualys_report.json` - JSON format with structured data

Test the formatter with sample data:

```bash
# Test XML parsing
python3 qualys_formatter.py sample_data/sample_qualys_report.xml -o test_xml

# Test CSV parsing  
python3 qualys_formatter.py sample_data/sample_qualys_report.csv -o test_csv

# Test JSON parsing
python3 qualys_formatter.py sample_data/sample_qualys_report.json -o test_json
```

## Integration with Shuffle SOAR

This formatter is designed to integrate with Shuffle SOAR workflows:

1. **Automated Processing**: Use as a workflow action to process Qualys scan results
2. **Report Generation**: Generate formatted reports for security teams
3. **Data Transformation**: Convert between different report formats
4. **Dashboard Creation**: Create executive-ready security dashboards

### Workflow Integration Example

```python
# In a Shuffle workflow action
import subprocess
import json

def process_qualys_report(input_file):
    # Run the formatter
    result = subprocess.run([
        'python3', 'qualys_formatter.py', 
        input_file, '-f', 'all', '-o', 'workflow_report'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"status": "success", "files": ["workflow_report.html", "workflow_report.json"]}
    else:
        return {"status": "error", "message": result.stderr}
```

## Security Considerations

- **No sensitive data logging**: Vulnerability details are not logged to console
- **Local processing**: All data processing happens locally
- **HTML security**: Generated HTML includes XSS protection
- **File permissions**: Output files use secure default permissions

## Troubleshooting

### Common Issues

1. **"No vulnerabilities found"**
   - Check input file format and structure
   - Verify XML/CSV/JSON syntax is valid
   - Ensure column headers match expected format

2. **"Unsupported file format"**
   - Use .xml, .csv, or .json file extensions
   - Verify file is not corrupted

3. **Charts not displaying**
   - Check internet connection (Chart.js loads from CDN)
   - Open browser developer tools for JavaScript errors

### Debug Mode

Add print statements to debug parsing issues:

```python
# Add after parsing
print(f"Parsed {len(formatter.vulnerabilities)} vulnerabilities")
print(f"Sample vulnerability: {formatter.vulnerabilities[0] if formatter.vulnerabilities else 'None'}")
```

## Future Enhancements

- **Offline chart rendering** using local Chart.js
- **PDF export capability** 
- **Advanced filtering options**
- **Custom vulnerability scoring**
- **Integration APIs** for security tools
- **Email report delivery**
- **Historical trend analysis**

## Contributing

This tool is part of the Shuffle SOAR ecosystem. Contributions welcome for:

- Additional input format support
- Enhanced visualizations  
- Performance improvements
- Integration capabilities

---

**Note**: This formatter is designed for internal security use. Ensure proper handling of sensitive vulnerability data according to your organization's security policies.