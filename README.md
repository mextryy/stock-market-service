# Stock market service

A simplified, highly available stock exchange simulation with a REST API.

## Features
- **High availability**: Architecture designed to survive instance failures.
- **Audit log**: Every successful transaction is recorded and traceable.
- **Liquidity provider**: Centralized bank entity managing stock availability.
- **Fault tolerance**: Includes a `/chaos` endpoint to test system resilience.

## Tech Stack
- **Language**: Python (FastAPI) 
- **Database**: Redis 
- **Infrastructure**: Docker & Docker Compose
- **Load balancer**: Nginx / HAProxy

## Getting Started

### Prerequisites
- Docker and Docker Compose installed.

### Running the application
To start the entire cluster on a specific port (e.g., 8080), run:
```bash
./start.sh 8080
