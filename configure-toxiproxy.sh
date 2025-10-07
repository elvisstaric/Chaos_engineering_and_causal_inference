#!/bin/bash

# ToxiProxy Configuration Script for Kubernetes
# This script configures ToxiProxy to proxy the microservices

echo "Configuring ToxiProxy for Kubernetes deployment..."

# Wait for ToxiProxy to be ready
echo "Waiting for ToxiProxy to be ready..."
kubectl wait --for=condition=ready pod -l app=toxiproxy --timeout=60s

# Get ToxiProxy pod name
TOXIPROXY_POD=$(kubectl get pods -l app=toxiproxy -o jsonpath='{.items[0].metadata.name}')

echo "ToxiProxy pod: $TOXIPROXY_POD"

# Configure proxies
echo "Creating ToxiProxy proxies..."

# User Service Proxy (port 8600)
kubectl exec $TOXIPROXY_POD -- toxiproxy-cli create user-service -l 0.0.0.0:8600 -u user-service:8000

# Inventory Service Proxy (port 8601)
kubectl exec $TOXIPROXY_POD -- toxiproxy-cli create inventory-service -l 0.0.0.0:8601 -u inventory-service:8001

# Cart Service Proxy (port 8602)
kubectl exec $TOXIPROXY_POD -- toxiproxy-cli create cart-service -l 0.0.0.0:8602 -u cart-service:8002

# Order Service Proxy (port 8603)
kubectl exec $TOXIPROXY_POD -- toxiproxy-cli create order-service -l 0.0.0.0:8603 -u order-service:8003

echo "ToxiProxy configuration completed!"
echo "Proxies created:"
echo "- User Service: toxiproxy:8600 -> user-service:8000"
echo "- Inventory Service: toxiproxy:8601 -> inventory-service:8001"
echo "- Cart Service: toxiproxy:8602 -> cart-service:8002"
echo "- Order Service: toxiproxy:8603 -> order-service:8003"

# List all proxies
echo "Current ToxiProxy configuration:"
kubectl exec $TOXIPROXY_POD -- toxiproxy-cli list
