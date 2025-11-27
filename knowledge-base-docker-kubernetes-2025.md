<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Docker & Kubernetes Complete Guide (2025-2026)
## Container Orchestration & DevOps for LightSpeedUp Infrastructure

**Docker**: 24+ (Latest stable)  
**Kubernetes**: 1.28+ (Latest stable)  
**Use**: Containerization, deployment, scalability, microservices

## DOCKER BASICS

### What is Docker?
Containerization platform that packages applications with dependencies
Runs consistently across development, testing, and production

### Installation
```bash
# Ubuntu
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### Basic Commands
```bash
# Pull image
docker pull nginx

# Run container
docker run -d -p 80:80 --name mynginx nginx

# List containers
docker ps
docker ps -a  # All (including stopped)

# Stop/Start
docker stop mynginx
docker start mynginx

# Remove
docker rm mynginx
docker rmi nginx
```

## DOCKERFILE (BUILD IMAGES)

### Simple Example
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Advanced Example (Multi-stage Build)
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/server.js"]
```

### Build & Run
```bash
# Build image
docker build -t myapp:latest .

# Run with environment variables
docker run -d -p 3000:3000 -e DB_HOST=localhost myapp:latest
```

## DOCKER COMPOSE (MULTI-CONTAINER)

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### Compose Commands
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose build
```

## DOCKER VOLUMES (DATA PERSISTENCE)

```bash
# Create volume
docker volume create mydata

# Run with volume
docker run -v mydata:/app/data myapp

# List volumes
docker volume ls

# Remove volume
docker volume rm mydata
```

## DOCKER NETWORKING

```bash
# Create network
docker network create mynet

# Run containers on same network
docker run -d --name app1 --network mynet myapp
docker run -d --name app2 --network mynet myapp

# Containers can communicate using container names as hostnames
```

## KUBERNETES (K8S) BASICS

### What is Kubernetes?
Container orchestration platform for deploying, scaling, and managing containerized applications

### Components
- **Pod**: Smallest deployable unit (1+ containers)
- **Deployment**: Manages pod replicas
- **Service**: Exposes pods to network
- **Ingress**: HTTP/HTTPS routing
- **ConfigMap**: Configuration data
- **Secret**: Sensitive data

### Installation (K3s - Lightweight K8s)
```bash
# Install K3s (Proxmox VMs)
curl -sfL https://get.k3s.io | sh -

# Check status
sudo kubectl get nodes
```

## KUBERNETES YAML MANIFESTS

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: DB_HOST
          value: "db-service"
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

### Apply Manifests
```bash
# Apply configuration
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Or apply directory
kubectl apply -f k8s/
```

## KUBECTL COMMANDS

```bash
# Get resources
kubectl get pods
kubectl get deployments
kubectl get services

# Describe resource
kubectl describe pod myapp-abc123

# Logs
kubectl logs myapp-abc123
kubectl logs -f myapp-abc123  # Follow

# Execute command in pod
kubectl exec -it myapp-abc123 -- /bin/bash

# Scale deployment
kubectl scale deployment myapp --replicas=5

# Delete resources
kubectl delete pod myapp-abc123
kubectl delete deployment myapp
```

## CONFIGMAPS & SECRETS

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgres://db:5432"
  LOG_LEVEL: "info"
```

```bash
# Create from literal
kubectl create configmap app-config --from-literal=KEY=VALUE

# Use in deployment
env:
- name: DATABASE_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: DATABASE_URL
```

### Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  password: bm9yZWxlYzch  # base64 encoded
```

```bash
# Create secret
kubectl create secret generic app-secret --from-literal=password: "<VM_PASSWORD>"  # See credentials.json

# Use in deployment
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secret
      key: password
```

## PERSISTENT VOLUMES

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
# Use in deployment
volumes:
- name: data
  persistentVolumeClaim:
    claimName: data-pvc

volumeMounts:
- name: data
  mountPath: /app/data
```

## INGRESS (HTTP ROUTING)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp.lightspeedup.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## HELM (PACKAGE MANAGER)

```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add repository
helm repo add stable https://charts.helm.sh/stable

# Install chart
helm install myapp stable/nginx

# List releases
helm list

# Upgrade
helm upgrade myapp stable/nginx

# Uninstall
helm uninstall myapp
```

## CI/CD PIPELINE EXAMPLE

### GitHub Actions + Docker + K8s
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
    
    - name: Deploy to K8s
      run: |
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

## BEST PRACTICES (2025-2026)

### Docker
1. Use multi-stage builds to reduce image size
2. Don't run as root (use USER directive)
3. Use .dockerignore to exclude unnecessary files
4. Pin base image versions (python:3.11.5, not python:3.11)
5. Scan images for vulnerabilities (docker scout)

### Kubernetes
1. Use resource limits and requests
2. Use liveness and readiness probes
3. Use Helm for complex deployments
4. Use namespaces to organize resources
5. Use RBAC (Role-Based Access Control)
6. Use Horizontal Pod Autoscaler (HPA) for auto-scaling
7. Monitor with Prometheus + Grafana

## DOCKER FOR DELL R730 / PROXMOX

### Run Docker on Proxmox VMs
```bash
# VM150 (Ubuntu) - Already running Docker
sudo systemctl status docker

# Create new container VM
docker run -d -p 8080:80 --name web nginx

# Access from host
curl http://<VM150_IP>:8080
```

### Docker Swarm (Alternative to K8s)
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml mystack

# List services
docker service ls

# Scale service
docker service scale mystack_web=5
```

## MONITORING & LOGGING

### Docker Logs
```bash
docker logs -f container_name
docker logs --tail 100 container_name
```

### Kubernetes Logs
```bash
kubectl logs -f deployment/myapp
kubectl logs --previous pod/myapp-abc123  # Previous crash
```

### Prometheus + Grafana
```bash
# Install with Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack

# Access Grafana (default: admin/prom-operator)
kubectl port-forward svc/prometheus-grafana 3000:80
```

## LEARNING RESOURCES

- Docker Docs: docs.docker.com
- Kubernetes Docs: kubernetes.io/docs
- Helm Docs: helm.sh/docs
- Docker Hub: hub.docker.com (public images)
- Kubernetes Playground: play.k8s.io

**Complete Docker & Kubernetes reference for SHENRON**

