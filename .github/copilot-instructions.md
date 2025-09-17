# Shuffle SOAR Platform

Shuffle is a Docker-based Security Orchestration, Automation and Response (SOAR) platform that centralizes and automates security operations through workflow orchestration and app integrations.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

Bootstrap, build, and run the repository:
- Create required directories: `mkdir -p /tmp/shuffle-apps /tmp/shuffle-files /tmp/shuffle-database`
- Fix database permissions: `sudo chown -R 1000:1000 /tmp/shuffle-database` (required for OpenSearch)
- Start services: `docker compose up -d` -- takes ~1 second to start. NEVER CANCEL.
- Full initialization: Wait 60 seconds for OpenSearch to fully initialize. NEVER CANCEL.
- Pull images (first time): `docker compose pull` -- takes ~30 seconds. NEVER CANCEL.

Check service status:
- Verify all containers running: `docker compose ps`
- Frontend accessible at: http://localhost:3001 (should return HTTP 200)
- Backend accessible at: http://localhost:5001 (may return HTTP 500 until org setup)
- Check logs if issues: `docker compose logs [service-name]`

Stop services:
- Clean shutdown: `docker compose down`
- Full cleanup: `docker compose down --volumes --remove-orphans`

## Validation

ALWAYS manually validate functionality after making changes:
- Access frontend at http://localhost:3001
- Complete initial setup by creating admin account (username: admin, password: min 10 chars)
- Login with created credentials
- Navigate to Workflows section to verify dashboard loads
- Verify you can access "Create Workflow" functionality

Test the complete user workflow:
1. Initial admin setup at `/adminsetup` (first visit)
2. Login at `/login` with created admin credentials
3. App selection wizard at `/welcome` 
4. Main dashboard navigation (Workflows, Apps, etc.)
5. Workflow creation interface accessibility

ALWAYS run these validation steps after any configuration changes.

## Configuration

Required environment file (`.env`):
```
FRONTEND_PORT=3001
FRONTEND_PORT_HTTPS=3443
BACKEND_HOSTNAME=shuffle-backend
BACKEND_PORT=5001
SHUFFLE_APP_HOTLOAD_LOCATION=/tmp/shuffle-apps
SHUFFLE_FILE_LOCATION=/tmp/shuffle-files
DB_LOCATION=/tmp/shuffle-database
SHUFFLE_OPENSEARCH_URL=http://shuffle-opensearch:9200
SHUFFLE_OPENSEARCH_SKIP_SSL_VERIFY=true
```

Docker Compose configuration requires:
- OpenSearch security disabled: `plugins.security.disabled=true`
- Correct filename: `docker-compose.yml` (NOT `docker-compse.yml`)
- Proper volume mounts with correct permissions

## Common Tasks

### Repository Structure
```
.
├── README.md              # Basic deployment instructions
├── docker-compose.yml     # Service orchestration (corrected filename)
├── .env                   # Environment configuration
└── .github/
    └── copilot-instructions.md  # This file
```

### Default Credentials
- Initial setup: Create admin user via web interface
- Username: admin (or custom)
- Password: minimum 10 characters
- Access: http://localhost:3001

### Service Architecture
- **Frontend**: React web application (port 3001/3443)
- **Backend**: Go API service (port 5001)  
- **OpenSearch**: Database/search engine (internal ports 9200/9300)

### Port Configuration
- Frontend HTTP: 3001
- Frontend HTTPS: 3443
- Backend API: 5001
- OpenSearch: 9200 (internal only)

### Timing Expectations
- Container startup: ~1 second
- Full system ready: ~60 seconds (OpenSearch initialization)
- Docker image pull: ~30 seconds (first time)
- Login/page transitions: ~2-5 seconds

### Known Issues and Solutions
- OpenSearch permission errors: Ensure `sudo chown -R 1000:1000` on database directory
- Backend 500 errors: Normal until organization setup is complete
- SSL certificate errors: Use HTTP for OpenSearch in local development
- Container start failures: Run `docker compose down --volumes` and restart

### Development Workflow
1. Make configuration changes
2. Run `docker compose down && docker compose up -d`
3. Wait 60 seconds for full initialization
4. Access http://localhost:3001 to validate
5. Test complete user login and navigation workflow
6. Verify workflow creation interface is accessible

This platform does not require traditional build processes - it runs entirely via Docker containers using pre-built images from GitHub Container Registry.