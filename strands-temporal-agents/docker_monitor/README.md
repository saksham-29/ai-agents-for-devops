# Docker Container Health Monitor

AI-powered Docker container monitoring with both simple and Temporal implementations. This is a practical DevOps use case demonstrating how to build production-ready monitoring tools with automatic retries, fault tolerance, and complete audit trails.

## What's This?

Two versions of the same Docker monitoring agent:

- **Simple Agent** (`docker_agent.py`) - Direct execution, perfect for development
- **Temporal Agent** (`docker_temporal_agent.py`) - Enterprise-grade with retries, monitoring, and fault tolerance

Both provide natural language interfaces for Docker operations:
- Check container status
- Monitor container health (CPU, memory, restart count)
- Retrieve container logs
- Restart unhealthy containers

## Quick Start

### Prerequisites

- Python 3.8+
- Docker Desktop running
- Temporal CLI (for Temporal version)
- Ollama with llama3.2 model

### Installation

```bash
# From repository root
cd strands-temporal-agents
source venv/bin/activate
pip install -r requirements.txt
```

### Start Demo Containers

```bash
cd docker_monitor
docker compose -f docker-compose.demo.yml up -d
```

This starts 3 demo containers:
- **demo-nginx** - Web server with health checks (port 8080)
- **demo-redis** - Redis cache with verbose logging (port 6379)
- **demo-logger** - Python app generating continuous logs

**Verify containers are running:**
```bash
docker ps --filter "name=demo-"
```

**Stop demo containers:**
```bash
docker compose -f docker-compose.demo.yml down
```

### Run Simple Agent

```bash
python docker_agent.py
```

Try these queries:
- "Check container status"
- "Is demo-nginx healthy?"
- "Show me logs for demo-logger"
- "Restart demo-redis"

### Run Temporal Agent

**Terminal 1: Start Temporal Server**
```bash
temporal server start-dev
```

**Terminal 2: Start Worker**
```bash
python docker_worker.py
```

**Terminal 3: Run Client**
```bash
python docker_client.py
```

**Browser: Open Temporal UI**
```
http://localhost:8233
```

## Files

### Core Implementation
- `docker_utils.py` - Docker SDK wrapper and data models
- `docker_agent.py` - Simple agent with @tool decorators
- `docker_temporal_agent.py` - Temporal workflows and activities
- `docker_worker.py` - Temporal worker process
- `docker_client.py` - Temporal client interface

### Demo & Testing
- `docker-compose.demo.yml` - Demo container definitions
- `test_docker_agent_basic.py` - Basic functionality tests
- `validate_docker_monitor.py` - Validation script

### Documentation
- `docs/DEMO-GUIDE.md` - Complete demo script (5-7 minutes)
- `docs/DEMO-QUICK-START.md` - Fast setup guide (2 minutes)
- `docs/DEMO-CHEATSHEET.md` - Quick reference for demos
- `docs/DEMO-READY.md` - Pre-demo checklist

## Configuration

Environment variables (optional):
```bash
export DOCKER_HOST="unix:///var/run/docker.sock"  # Default
export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_MODEL="llama3.2:latest"
```

Configuration is centralized in `../config.py`:
- Docker connection settings
- Temporal task queue names
- Ollama model configuration
- Timeout values

## Why Temporal for DevOps?

The Temporal version adds critical production features:

### Automatic Retries
Different retry policies for different operations:
- **Status checks**: 3 attempts, 1s→5s backoff (fast, low cost)
- **Health checks**: 3 attempts, 2s→10s backoff (may need stabilization)
- **Log retrieval**: 2 attempts, 1s→5s backoff (usually succeeds or fails quickly)
- **Restart operations**: 5 attempts, 5s→30s backoff (critical, needs more retries)
- **AI orchestrator**: 2 attempts, no backoff (LLM calls are expensive)

### Execution History
Complete audit trail of all container operations:
- Who ran what command
- When it was executed
- What was the result
- How many retries occurred

### Fault Tolerance
Operations continue even if:
- Worker process crashes
- Network connection drops
- Docker daemon temporarily unavailable

### Monitoring Dashboard
Web UI at `http://localhost:8233` shows:
- All workflow executions
- Activity timelines
- Retry attempts
- Input/output for each step

## Architecture

### Simple Agent Flow
```
User Query → Agent → Docker SDK → Result
```

### Temporal Agent Flow
```
User Query → Client → Temporal Server → Worker → Activities → Docker SDK → Result
                                          ↓
                                    AI Orchestrator
                                    (Plans operations)
```

The AI orchestrator analyzes user queries and determines which Docker operations to execute and in what order.

## Example Queries

### Basic Status
```
"Check container status"
"Show me all running containers"
"List stopped containers"
```

### Health Monitoring
```
"Is demo-nginx healthy?"
"Check health of all running containers"
"Show me CPU and memory usage for demo-redis"
```

### Log Retrieval
```
"Show me logs for demo-logger"
"Show me the last 50 lines from demo-nginx"
"Get recent logs from demo-redis"
```

### Log Analysis (NEW!)
```
"Analyze logs from demo-logger"
"Give me a summary of demo-redis logs"
"Summarize the last 100 lines from demo-nginx"
```

### Container Management
```
"Restart demo-nginx"
"Restart the unhealthy container"
```

### Complex Queries (Temporal AI Orchestration)
```
"Check demo-nginx health and show me its logs"
"Is demo-redis healthy? If not, restart it"
"Check all containers and show logs for unhealthy ones"
```

## Demo Scripts

### Quick Demo (2 minutes)
See `docs/DEMO-QUICK-START.md` for a fast walkthrough.

### Full Demo (5-7 minutes)
See `docs/DEMO-GUIDE.md` for a comprehensive demo script with talking points.

### Demo Cheatsheet
See `docs/DEMO-CHEATSHEET.md` for quick reference during presentations.

## Troubleshooting

**Docker connection errors?**
```bash
# Check Docker is running
docker ps

# Check Docker socket
ls -la /var/run/docker.sock
```

**Demo containers not starting?**
```bash
# Check status
docker ps --filter "name=demo-"

# View logs
docker logs demo-nginx
docker logs demo-redis
docker logs demo-logger

# Restart containers
docker compose -f docker-compose.demo.yml restart

# Stop and remove
docker compose -f docker-compose.demo.yml down
```

**Worker won't start?**
```bash
# Ensure Temporal server is running first
temporal server start-dev

# Check Temporal connection
curl http://localhost:7233
```

**Ollama issues?**
```bash
# Check Ollama is running
ollama list

# Pull model if needed
ollama pull llama3.2:latest
```

**Container not found?**
```bash
# List all containers
docker ps -a

# Check container name
docker ps --filter "name=demo-"
```

## Testing

Run basic tests:
```bash
pytest test_docker_agent_basic.py
```

Validate installation:
```bash
python validate_docker_monitor.py
```

## Cleanup

Stop demo containers:
```bash
docker compose -f docker-compose.demo.yml down
```

Stop Temporal server:
```bash
# Ctrl+C in the terminal running temporal server
```

## The Point

This demonstrates how to start with a simple agent for rapid development, then add enterprise features when needed. The core logic stays the same - you're just changing how it runs.

Perfect for:
- Learning Temporal workflows
- Building DevOps automation
- Understanding AI agent patterns
- Demonstrating production-ready monitoring

## Related

This is part of the Strands Temporal Agents repository. See the main README for the original simple agent demo (file/time operations).
