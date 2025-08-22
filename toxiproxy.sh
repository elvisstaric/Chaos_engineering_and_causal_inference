#!/bin/bash

TOXIPROXY_API="http://localhost:8474"
SERVICES=("user_service" "inventory_service" "cart_service" "order_service")
PORTS=(8000 8001 8002 8003)
BASE_PORT=8600

for i in "${!SERVICES[@]}"; do
  SERVICE="${SERVICES[$i]}"
  UPSTREAM_PORT=${PORTS[$i]}
  PROXY_NAME="${SERVICE}_proxy"
  LISTEN_PORT=$((BASE_PORT + i))

  echo "Provjera postoji li proxy '$PROXY_NAME'..."
  proxy_exists=$(curl -s $TOXIPROXY_API/proxies | grep -o "\"name\":\"$PROXY_NAME\"")

  if [ "$proxy_exists" != "\"name\":\"$PROXY_NAME\"" ]; then
    echo "Proxy '$PROXY_NAME' ne postoji, kreiram ga..."
    curl -s -X POST $TOXIPROXY_API/proxies \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"$PROXY_NAME\",
        \"listen\": \"0.0.0.0:${LISTEN_PORT}\",
        \"upstream\": \"${SERVICE}:${UPSTREAM_PORT}\"
      }"
    echo "Proxy kreiran."
  else
    echo "Proxy '$PROXY_NAME' već postoji."
  fi
done
# echo "Dodajem latency toxic (30s kašnjenje)..."
# curl -s -X POST $TOXIPROXY_API/proxies/user_service_proxy/toxics \
# -H "Content-Type: application/json" \
# -d '{
#   "name": "user_latency",
#   "type": "latency",
#   "stream": "downstream",
#   "attributes": {
#     "latency": 1000,
#     "jitter": 500
#   }
# }'

# echo "Čekam 30 sekundi..."
# sleep 300

# echo "Brišem latency toxic..."
# curl -s -X DELETE $TOXIPROXY_API/proxies/user_service_proxy/toxics/user_latency -H "Content-Type: application/json" || true
# sleep 10

# echo "Dodajem user_timeot toxic (simulacija timeout)..."
# curl -s -X POST $TOXIPROXY_API/proxies/order_service_proxy/toxics \
#  -H "Content-Type: application/json" \
#  -d '{
#   "name": "user_timeout",
#   "type": "timeout",
#   "stream": "downstream",
#   "attributes": {
#     "timeout": 10000
#   }
# }'

# echo "Čekam 30 sekundi..."
# sleep 300

# echo "Brišem ruser_timeout toxic..."
# curl -s -X DELETE $TOXIPROXY_API/proxies/order_service_proxy/toxics/user_timeout -H "Content-Type: application/json" || true

# echo "Skripta završena."