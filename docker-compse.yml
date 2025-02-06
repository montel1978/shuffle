version: '3'
services:
  frontend:
    image: ghcr.io/shuffle/shuffle-frontend:latest
    container_name: shuffle-frontend
    hostname: shuffle-frontend
    ports:
      - "${FRONTEND_PORT}:80"
      - "${FRONTEND_PORT_HTTPS}:443"
    networks:
      - shuffle
    environment:
      - BACKEND_HOSTNAME=${BACKEND_HOSTNAME}
    restart: unless-stopped
    depends_on:
      - backend
  backend:
    image: ghcr.io/shuffle/shuffle-backend:latest
    container_name: shuffle-backend
    hostname: ${BACKEND_HOSTNAME}
    # Here for debugging:
    ports:
      - "${BACKEND_PORT}:5001"
    networks:
      - shuffle
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ${SHUFFLE_APP_HOTLOAD_LOCATION}:/shuffle-apps     
      - ${SHUFFLE_FILE_LOCATION}:/shuffle-files
      #- ${SHUFFLE_OPENSEARCH_CERTIFICATE_FILE}:/shuffle-files/es_certificate
    env_file: .env
    environment:
      - SHUFFLE_APP_HOTLOAD_FOLDER=/shuffle-apps
      - SHUFFLE_FILE_LOCATION=/shuffle-files
    restart: unless-stopped
    depends_on:
      - opensearch
  opensearch:
    image: opensearchproject/opensearch:2.5.0
    hostname: shuffle-opensearch
    container_name: shuffle-opensearch
    environment:
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms4096m -Xmx4096m" # minimum and maximum Java heap size, recommend setting both to 50% of system RAM
      - cluster.routing.allocation.disk.threshold_enabled=false
      - cluster.name=shuffle-cluster
      - node.name=shuffle-opensearch
      - discovery.seed_hosts=shuffle-opensearch
      - cluster.initial_master_nodes=shuffle-opensearch
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536 # maximum number of open files for the OpenSearch user, set to at least 65536 on modern systems
        hard: 65536
    volumes:
      - ${DB_LOCATION}:/usr/share/opensearch/data:rw
    networks:
      - shuffle
    restart: unless-stopped
networks:
  shuffle:
    driver: bridge
