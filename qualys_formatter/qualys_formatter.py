#!/usr/bin/env python3
"""
Qualys Vulnerability Report Formatter

This script parses Qualys vulnerability reports in various formats (XML, CSV, JSON)
and generates formatted, easy-to-read reports with visualizations.

Author: Shuffle SOAR Integration
"""

import argparse
import csv
import json
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
import sys
import re

class QualysReportFormatter:
    """Main class for formatting Qualys vulnerability reports."""
    
    def __init__(self):
        self.vulnerabilities = []
        self.summary_stats = {}
        
    def parse_xml_report(self, file_path):
        """Parse Qualys XML vulnerability report."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Handle different XML structures based on common Qualys formats
            hosts = root.findall('.//HOST') or root.findall('.//host')
            
            for host in hosts:
                host_ip_element = host.find('IP') or host.find('ip')
                host_ip = host_ip_element.text if host_ip_element is not None else host.get('IP', 'N/A')
                
                # Look for vulnerabilities in different possible structures
                vulns = (host.findall('.//VULN_INFO') or 
                        host.findall('.//VULN') or 
                        host.findall('.//vuln_info') or 
                        host.findall('.//vuln'))
                
                for vuln in vulns:
                    # Extract CVE list from CVE_ID_LIST structure
                    cve_list_element = vuln.find('CVE_ID_LIST')
                    cve_list = 'N/A'
                    if cve_list_element is not None:
                        cve_ids = [cve.text for cve in cve_list_element.findall('CVE_ID') if cve.text]
                        cve_list = ', '.join(cve_ids) if cve_ids else 'N/A'
                    
                    vuln_data = {
                        'host_ip': host_ip,
                        'qid': self._get_text_content(vuln, ['QID', 'qid', 'number']),
                        'title': self._get_text_content(vuln, ['TITLE', 'title']),
                        'severity': self._get_text_content(vuln, ['SEVERITY', 'severity']),
                        'cvss_score': self._get_text_content(vuln, ['CVSS_SCORE', 'cvss_score', 'CVSS3_SCORE']),
                        'category': self._get_text_content(vuln, ['CATEGORY', 'category']),
                        'cve_list': cve_list,
                        'solution': self._get_text_content(vuln, ['SOLUTION', 'solution']),
                        'results': self._get_text_content(vuln, ['RESULT', 'results']),
                        'port': self._get_text_content(vuln, ['PORT', 'port']),
                        'protocol': self._get_text_content(vuln, ['PROTOCOL', 'protocol'])
                    }
                    self.vulnerabilities.append(vuln_data)
                    
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error parsing XML: {e}")
            return False
            
        return True
    
    def parse_csv_report(self, file_path):
        """Parse Qualys CSV vulnerability report."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                # Try to detect delimiter
                sample = file.read(1024)
                file.seek(0)
                
                delimiter = ',' if sample.count(',') > sample.count(';') else ';'
                reader = csv.DictReader(file, delimiter=delimiter)
                
                for row in reader:
                    # Map common CSV column names to our standard format
                    vuln_data = {
                        'host_ip': row.get('IP') or row.get('Host') or row.get('Target') or 'N/A',
                        'qid': row.get('QID') or row.get('Vuln ID') or row.get('ID') or 'N/A',
                        'title': row.get('Title') or row.get('Vulnerability') or row.get('Name') or 'N/A',
                        'severity': row.get('Severity') or row.get('Risk') or 'N/A',
                        'cvss_score': row.get('CVSS Score') or row.get('CVSS') or row.get('Score') or 'N/A',
                        'category': row.get('Category') or row.get('Type') or 'N/A',
                        'cve_list': row.get('CVE') or row.get('CVE ID') or 'N/A',
                        'solution': row.get('Solution') or row.get('Remediation') or 'N/A',
                        'results': row.get('Results') or row.get('Evidence') or 'N/A',
                        'port': row.get('Port') or 'N/A',
                        'protocol': row.get('Protocol') or 'N/A'
                    }
                    self.vulnerabilities.append(vuln_data)
                    
        except Exception as e:
            print(f"Error parsing CSV file: {e}")
            return False
            
        return True
    
    def parse_json_report(self, file_path):
        """Parse Qualys JSON vulnerability report."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Handle different JSON structures
                vulns = []
                if isinstance(data, list):
                    vulns = data
                elif 'vulnerabilities' in data:
                    vulns = data['vulnerabilities']
                elif 'results' in data:
                    vulns = data['results']
                elif 'data' in data:
                    vulns = data['data']
                
                for vuln in vulns:
                    vuln_data = {
                        'host_ip': vuln.get('ip') or vuln.get('host') or vuln.get('target') or 'N/A',
                        'qid': str(vuln.get('qid') or vuln.get('id') or vuln.get('vuln_id') or 'N/A'),
                        'title': vuln.get('title') or vuln.get('name') or vuln.get('vulnerability') or 'N/A',
                        'severity': vuln.get('severity') or vuln.get('risk') or 'N/A',
                        'cvss_score': str(vuln.get('cvss_score') or vuln.get('cvss') or vuln.get('score') or 'N/A'),
                        'category': vuln.get('category') or vuln.get('type') or 'N/A',
                        'cve_list': vuln.get('cve') or vuln.get('cve_id') or 'N/A',
                        'solution': vuln.get('solution') or vuln.get('remediation') or 'N/A',
                        'results': vuln.get('results') or vuln.get('evidence') or 'N/A',
                        'port': str(vuln.get('port') or 'N/A'),
                        'protocol': vuln.get('protocol') or 'N/A'
                    }
                    self.vulnerabilities.append(vuln_data)
                    
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error parsing JSON: {e}")
            return False
            
        return True
    
    def _get_text_content(self, element, tag_names):
        """Helper method to extract text content from XML element."""
        for tag_name in tag_names:
            found = element.find(tag_name)
            if found is not None:
                return found.text or 'N/A'
        return 'N/A'
    
    def calculate_summary_stats(self):
        """Calculate summary statistics from parsed vulnerabilities."""
        if not self.vulnerabilities:
            return
            
        self.summary_stats = {
            'total_vulnerabilities': len(self.vulnerabilities),
            'unique_hosts': len(set(v['host_ip'] for v in self.vulnerabilities)),
            'severity_distribution': Counter(v['severity'] for v in self.vulnerabilities),
            'category_distribution': Counter(v['category'] for v in self.vulnerabilities),
            'top_vulnerabilities': Counter(v['title'] for v in self.vulnerabilities).most_common(10),
            'hosts_by_vuln_count': Counter(v['host_ip'] for v in self.vulnerabilities).most_common(10)
        }
        
        # Calculate CVSS score distribution
        cvss_ranges = {'Low (0-3.9)': 0, 'Medium (4.0-6.9)': 0, 'High (7.0-8.9)': 0, 'Critical (9.0-10.0)': 0, 'Unknown': 0}
        for vuln in self.vulnerabilities:
            try:
                score = float(vuln['cvss_score'])
                if score < 4.0:
                    cvss_ranges['Low (0-3.9)'] += 1
                elif score < 7.0:
                    cvss_ranges['Medium (4.0-6.9)'] += 1
                elif score < 9.0:
                    cvss_ranges['High (7.0-8.9)'] += 1
                else:
                    cvss_ranges['Critical (9.0-10.0)'] += 1
            except (ValueError, TypeError):
                cvss_ranges['Unknown'] += 1
                
        self.summary_stats['cvss_distribution'] = cvss_ranges
    
    def generate_html_report(self, output_path):
        """Generate an HTML report with visualizations."""
        html_template = self._get_html_template()
        
        # Generate summary cards
        summary_html = self._generate_summary_cards()
        
        # Generate charts data
        charts_data = self._generate_charts_data()
        
        # Generate vulnerability table
        table_html = self._generate_vulnerability_table()
        
        # Replace placeholders in template
        html_content = html_template.replace('{{SUMMARY_CARDS}}', summary_html)
        html_content = html_content.replace('{{CHARTS_DATA}}', charts_data)
        html_content = html_content.replace('{{VULNERABILITY_TABLE}}', table_html)
        html_content = html_content.replace('{{REPORT_TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
            
        print(f"HTML report generated: {output_path}")
    
    def generate_csv_summary(self, output_path):
        """Generate a CSV summary report."""
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write summary statistics
            writer.writerow(['Qualys Vulnerability Report Summary'])
            writer.writerow(['Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            writer.writerow(['Total Vulnerabilities:', self.summary_stats.get('total_vulnerabilities', 0)])
            writer.writerow(['Unique Hosts:', self.summary_stats.get('unique_hosts', 0)])
            writer.writerow([])
            
            # Severity distribution
            writer.writerow(['Severity Distribution'])
            writer.writerow(['Severity', 'Count'])
            for severity, count in self.summary_stats.get('severity_distribution', {}).items():
                writer.writerow([severity, count])
            writer.writerow([])
            
            # Top vulnerabilities
            writer.writerow(['Top 10 Vulnerabilities'])
            writer.writerow(['Vulnerability', 'Count'])
            for vuln, count in self.summary_stats.get('top_vulnerabilities', []):
                writer.writerow([vuln, count])
                
        print(f"CSV summary generated: {output_path}")
    
    def generate_json_report(self, output_path):
        """Generate a JSON structured report."""
        report_data = {
            'metadata': {
                'generated_on': datetime.now().isoformat(),
                'total_vulnerabilities': len(self.vulnerabilities),
                'unique_hosts': len(set(v['host_ip'] for v in self.vulnerabilities))
            },
            'summary_statistics': self.summary_stats,
            'vulnerabilities': self.vulnerabilities
        }
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(report_data, file, indent=2, ensure_ascii=False)
            
        print(f"JSON report generated: {output_path}")
    
    def _generate_summary_cards(self):
        """Generate HTML for summary cards."""
        stats = self.summary_stats
        
        return f"""
        <div class="summary-cards">
            <div class="card">
                <h3>Total Vulnerabilities</h3>
                <div class="stat-number">{stats.get('total_vulnerabilities', 0)}</div>
            </div>
            <div class="card">
                <h3>Unique Hosts</h3>
                <div class="stat-number">{stats.get('unique_hosts', 0)}</div>
            </div>
            <div class="card critical">
                <h3>Critical Severity</h3>
                <div class="stat-number">{stats.get('severity_distribution', {}).get('5', 0)}</div>
            </div>
            <div class="card high">
                <h3>High Severity</h3>
                <div class="stat-number">{stats.get('severity_distribution', {}).get('4', 0)}</div>
            </div>
        </div>
        """
    
    def _generate_charts_data(self):
        """Generate JavaScript data for charts."""
        severity_data = self.summary_stats.get('severity_distribution', {})
        cvss_data = self.summary_stats.get('cvss_distribution', {})
        
        return f"""
        var severityData = {json.dumps(dict(severity_data))};
        var cvssData = {json.dumps(cvss_data)};
        """
    
    def _generate_vulnerability_table(self):
        """Generate HTML table for vulnerabilities."""
        if not self.vulnerabilities:
            return "<p>No vulnerabilities found.</p>"
        
        rows = []
        for vuln in self.vulnerabilities[:100]:  # Limit to first 100 for performance
            severity_class = self._get_severity_class(vuln['severity'])
            rows.append(f"""
            <tr class="{severity_class}">
                <td>{vuln['host_ip']}</td>
                <td>{vuln['qid']}</td>
                <td>{vuln['title'][:80]}...</td>
                <td><span class="severity-badge {severity_class}">{vuln['severity']}</span></td>
                <td>{vuln['cvss_score']}</td>
                <td>{vuln['category']}</td>
                <td>{vuln['port']}</td>
            </tr>
            """)
        
        return f"""
        <table class="vulnerability-table">
            <thead>
                <tr>
                    <th>Host IP</th>
                    <th>QID</th>
                    <th>Title</th>
                    <th>Severity</th>
                    <th>CVSS Score</th>
                    <th>Category</th>
                    <th>Port</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
        """
    
    def _get_severity_class(self, severity):
        """Get CSS class for severity level."""
        severity_str = str(severity).lower()
        if severity_str in ['5', 'critical']:
            return 'critical'
        elif severity_str in ['4', 'high']:
            return 'high'
        elif severity_str in ['3', 'medium']:
            return 'medium'
        elif severity_str in ['2', 'low']:
            return 'low'
        else:
            return 'info'
    
    def _get_html_template(self):
        """Get HTML template for report."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qualys Vulnerability Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .card.critical {
            border-left-color: #dc3545;
        }
        
        .card.high {
            border-left-color: #fd7e14;
        }
        
        .card h3 {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }
        
        .charts-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .chart-container h3 {
            margin-bottom: 1rem;
            color: #333;
        }
        
        .vulnerability-table {
            width: 100%;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .vulnerability-table th {
            background: #667eea;
            color: white;
            padding: 1rem;
            text-align: left;
        }
        
        .vulnerability-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #eee;
        }
        
        .vulnerability-table tbody tr:hover {
            background: #f8f9fa;
        }
        
        .severity-badge {
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .severity-badge.critical {
            background: #dc3545;
            color: white;
        }
        
        .severity-badge.high {
            background: #fd7e14;
            color: white;
        }
        
        .severity-badge.medium {
            background: #ffc107;
            color: #333;
        }
        
        .severity-badge.low {
            background: #28a745;
            color: white;
        }
        
        .severity-badge.info {
            background: #17a2b8;
            color: white;
        }
        
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            color: #666;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .charts-section {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Qualys Vulnerability Report</h1>
        <p>Comprehensive Security Assessment Dashboard</p>
        <p><small>Generated on: {{REPORT_TIMESTAMP}}</small></p>
    </div>
    
    <div class="container">
        {{SUMMARY_CARDS}}
        
        <div class="charts-section">
            <div class="chart-container">
                <h3>Severity Distribution</h3>
                <canvas id="severityChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>CVSS Score Distribution</h3>
                <canvas id="cvssChart"></canvas>
            </div>
        </div>
        
        <div class="table-section">
            <h2 style="margin-bottom: 1rem;">Vulnerability Details</h2>
            {{VULNERABILITY_TABLE}}
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by Shuffle SOAR Qualys Formatter | For internal security use only</p>
    </div>
    
    <script>
        {{CHARTS_DATA}}
        
        // Severity Chart
        const severityCtx = document.getElementById('severityChart').getContext('2d');
        new Chart(severityCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(severityData),
                datasets: [{
                    data: Object.values(severityData),
                    backgroundColor: [
                        '#dc3545',
                        '#fd7e14', 
                        '#ffc107',
                        '#28a745',
                        '#17a2b8'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
        // CVSS Chart
        const cvssCtx = document.getElementById('cvssChart').getContext('2d');
        new Chart(cvssCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(cvssData),
                datasets: [{
                    label: 'Vulnerability Count',
                    data: Object.values(cvssData),
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#fd7e14',
                        '#dc3545',
                        '#6c757d'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
        """

def main():
    """Main function to handle command line arguments and execute formatting."""
    parser = argparse.ArgumentParser(description='Format Qualys vulnerability reports')
    parser.add_argument('input_file', help='Path to the Qualys report file (XML, CSV, or JSON)')
    parser.add_argument('-o', '--output', default='qualys_report', help='Output file prefix (default: qualys_report)')
    parser.add_argument('-f', '--format', choices=['html', 'csv', 'json', 'all'], default='html', 
                       help='Output format (default: html)')
    
    args = parser.parse_args()
    
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    formatter = QualysReportFormatter()
    
    # Determine file type and parse accordingly
    file_ext = Path(args.input_file).suffix.lower()
    
    if file_ext == '.xml':
        success = formatter.parse_xml_report(args.input_file)
    elif file_ext == '.csv':
        success = formatter.parse_csv_report(args.input_file)
    elif file_ext == '.json':
        success = formatter.parse_json_report(args.input_file)
    else:
        print(f"Error: Unsupported file format '{file_ext}'. Supported formats: .xml, .csv, .json")
        sys.exit(1)
    
    if not success:
        print("Failed to parse input file.")
        sys.exit(1)
    
    if not formatter.vulnerabilities:
        print("No vulnerabilities found in the input file.")
        sys.exit(1)
    
    # Calculate summary statistics
    formatter.calculate_summary_stats()
    
    # Generate output files
    if args.format == 'html' or args.format == 'all':
        formatter.generate_html_report(f"{args.output}.html")
    
    if args.format == 'csv' or args.format == 'all':
        formatter.generate_csv_summary(f"{args.output}_summary.csv")
    
    if args.format == 'json' or args.format == 'all':
        formatter.generate_json_report(f"{args.output}.json")
    
    print(f"\nProcessed {len(formatter.vulnerabilities)} vulnerabilities from {formatter.summary_stats.get('unique_hosts', 0)} hosts.")

if __name__ == "__main__":
    main()