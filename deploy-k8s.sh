#!/bin/bash

# Build and push Docker images for Kubernetes deployment
# Run this script on your Ubuntu server after pulling the code

echo "Building Docker images for Kubernetes deployment..."

# Build all service images
docker build -t user-service:latest ./user_service/
docker build -t cart-service:latest ./cart_service/
docker build -t inventory-service:latest ./inventory_service/
docker build -t order-service:latest ./order_service/

echo "Docker images built successfully!"

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."

kubectl apply -f k8s-configmap.yaml
kubectl apply -f k8s-deployments.yaml
kubectl apply -f k8s-services.yaml
kubectl apply -f k8s-toxiproxy.yaml
kubectl apply -f k8s-monitoring.yaml
kubectl apply -f k8s-locust.yaml
kubectl apply -f k8s-ingress.yaml

echo "Waiting for services to be ready..."
kubectl wait --for=condition=ready pod -l app=user-service --timeout=60s
kubectl wait --for=condition=ready pod -l app=cart-service --timeout=60s
kubectl wait --for=condition=ready pod -l app=inventory-service --timeout=60s
kubectl wait --for=condition=ready pod -l app=order-service --timeout=60s

echo "Configuring ToxiProxy..."
chmod +x configure-toxiproxy.sh
./configure-toxiproxy.sh

echo "Kubernetes deployment completed!"

# Check deployment status
echo "Checking deployment status..."
kubectl get pods
kubectl get services
kubectl get ingress

echo "Setup complete! Services should be accessible via:"
echo "- User Service: http://microservices.local/user"
echo "- Cart Service: http://microservices.local/cart"
echo "- Inventory Service: http://microservices.local/inventory"
echo "- Order Service: http://microservices.local/orders"
echo "- Prometheus: http://microservices.local/prometheus"
echo "- Locust: http://microservices.local/locust"
echo "- cAdvisor: http://microservices.local/cadvisor"
