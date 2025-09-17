Shuffle
Shuffle SOAR is a powerful open source platform that centralizes and automates security operations. It integrates various security tools, orchestrates incident response workflows, and automates routine tasks through predefined playbooks. With advanced intelligence and reporting capabilities, it empowers cybersecurity professionals to respond to security incidents effectively and efficiently, ultimately strengthening an organization's security posture.

## Qualys Vulnerability Report Formatter 🔍

This repository now includes a comprehensive **Qualys Vulnerability Report Formatter** that transforms raw Qualys scan data into beautiful, interactive dashboards and reports.

### Features:
- 📊 **Interactive HTML dashboards** with charts and visualizations
- 📋 **Multi-format support**: XML, CSV, and JSON input formats
- 📈 **Summary statistics** and vulnerability analytics
- 🎯 **CVSS score analysis** and severity categorization
- 🖥️ **Responsive design** for desktop and mobile
- 📄 **Multiple export formats**: HTML, CSV, JSON

### Quick Start:
```bash
# Format a Qualys XML report
./format_qualys.sh your_qualys_scan.xml

# Generate all formats with custom name
./format_qualys.sh your_scan.csv security_report all

# View sample reports
./format_qualys.sh qualys_formatter/sample_data/sample_qualys_report.xml demo
```

📖 **[Complete documentation](qualys_formatter/README.md)**

---

Let’s see how to deploye Shuffle

git clone https://github.com/Shuffle/Shuffle
CD Shuffle

Create folder name shuffle-database and change permission

mkdir shuffle-database
sudo chown -R 1000:1000 shuffle-database
# If you get an error using “ chown ”, add the user first with “ sudo useradd opensearch ”

Then we are going to face used port problem if we run it because we have Wazuh running on port 80, so we need to change the port

nano docker-compose.yml

Run the docker compose in background

docker-compose up -d

Go browser and tape https:ip_address:port


login Shuffle
Username=admin & Password=admin

Create new workflow and name it “Wazuh integration test”


Create Workflow
Inside the workflow we add Webhook, then we change the name of the webhook to “wazuh_alert” and change the name of the Shuffle tools to “response”


