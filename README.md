Shuffle
Shuffle SOAR is a powerful open source platform that centralizes and automates security operations. It integrates various security tools, orchestrates incident response workflows, and automates routine tasks through predefined playbooks. With advanced intelligence and reporting capabilities, it empowers cybersecurity professionals to respond to security incidents effectively and efficiently, ultimately strengthening an organization's security posture.

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


