# Stock market service

A simplified, highly available stock exchange simulation with a REST API.

## Features
- **High availability**: Architecture with multiple application instances and a load balancer.
- **Data integrity**: Uses Redis to maintain shared state across all instances.
- **Audit log**: Every successful transaction is recorded for audit purposes.
- **Fault tolerance**: Includes a `/chaos` endpoint to simulate instance failures and test resilience.

## Tech Stack
- **Backend**: Python 3.11 (FastAPI) 
- **Database**: Redis (Alpine)
- **Infrastructure**: Docker & Docker Compose
- **Load balancer**: Nginx

## Architecture
The system consists of two FastAPI instances behind an Nginx Load Balancer. All application state is stored in a centralized Redis database, ensuring that if one instance is terminated, the service remains operational without data loss.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed.

### Running the application
To start the entire cluster on a specific port (e.g., 8080), run:
```bash
chmod +x start.sh  # Only needed once
./start.sh 8080