# Qualys Vulnerability Report Formatter

Transform raw Qualys vulnerability reports into beautiful, actionable security dashboards.

## 🚀 Quick Demo

Try it with sample data:
```bash
./format_qualys.sh qualys_formatter/sample_data/sample_qualys_report.xml demo
```

## 📋 What it does

- ✅ Parses Qualys XML, CSV, and JSON reports
- ✅ Creates interactive HTML dashboards
- ✅ Generates CSV summaries for spreadsheets
- ✅ Exports structured JSON data
- ✅ Analyzes CVSS scores and severity levels
- ✅ Identifies top vulnerabilities and affected hosts
- ✅ Mobile-responsive design

## 🎯 Best visualization approaches for Qualys reports:

### 1. Executive Dashboard (HTML)
- **Use case**: C-level presentations, board reports
- **Features**: High-level metrics, risk visualization, trends
- **Output**: Interactive HTML with charts

### 2. Technical Analysis (CSV + JSON)
- **Use case**: Security team analysis, ticketing systems
- **Features**: Detailed vulnerability data, filtering capabilities
- **Output**: Structured data for further processing

### 3. Remediation Planning (Combined)
- **Use case**: IT teams, prioritization
- **Features**: Risk-based prioritization, host grouping
- **Output**: Multiple formats for different audiences

## 📊 Visualization Features

- **Summary Cards**: Quick overview of vulnerability counts
- **Severity Distribution**: Pie chart showing risk breakdown
- **CVSS Score Analysis**: Bar chart of vulnerability scores
- **Host Analysis**: Identify most vulnerable systems
- **Top Vulnerabilities**: Most common security issues
- **Risk Prioritization**: Color-coded severity levels

## 🔧 Integration Options

### With Shuffle SOAR:
- Automated report processing
- Workflow-triggered analysis
- Multi-format output for different teams
- Integration with ticketing systems

### With Other Tools:
- Import CSV data into spreadsheets
- Feed JSON to security analytics tools
- Embed HTML reports in wikis/portals
- API integration via JSON output

---

For complete documentation see: [qualys_formatter/README.md](qualys_formatter/README.md)