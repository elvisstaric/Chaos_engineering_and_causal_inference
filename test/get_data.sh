#!/bin/bash

NOW=$(date +%s)
START=$((NOW - 330))  
PROM_URL="http://localhost:9090/api/v1/query_range"
SERVICES=("user_service" "inv_service" "cart_service" "order_service")

STEP=30
OUT_DIR="./test_1/results_io_order_test"

mkdir -p "$OUT_DIR"

for SERVICE in "${SERVICES[@]}"; do
    echo "Spremam metrike za $SERVICE..."

    # 1. Requests
    QUERY_REQUESTS="sum by (method, endpoint) (increase(${SERVICE}_requests_total[30s]))"
    curl -s -G "$PROM_URL" \
        --data-urlencode "query=$QUERY_REQUESTS" \
        --data-urlencode "start=$START" \
        --data-urlencode "end=$NOW" \
        --data-urlencode "step=$STEP" \
        > "${OUT_DIR}/${SERVICE}_requests.json"

    # 2. Latencija
    QUERY_LATENCY="sum by(endpoint) (rate(${SERVICE}_request_latency_seconds_sum[1m])) / sum by(endpoint) (rate(${SERVICE}_request_latency_seconds_count[30s]))*1000"
    curl -s -G "$PROM_URL" \
        --data-urlencode "query=$QUERY_LATENCY" \
        --data-urlencode "start=$START" \
        --data-urlencode "end=$NOW" \
        --data-urlencode "step=$STEP" \
        > "${OUT_DIR}/${SERVICE}_latency.json"

    # 3. Greške
    QUERY_ERRORS="sum by (method, endpoint, http_status_class) (increase(${SERVICE}_errors_total[30s]))"
    curl -s -G "$PROM_URL" \
        --data-urlencode "query=$QUERY_ERRORS" \
        --data-urlencode "start=$START" \
        --data-urlencode "end=$NOW" \
        --data-urlencode "step=$STEP" \
        > "${OUT_DIR}/${SERVICE}_errors.json"

    echo "  -> spremljeno: ${SERVICE}_requests.json, ${SERVICE}_latency.json, ${SERVICE}_errors.json"
done

echo "✅ Svi podaci spremljeni u ${OUT_DIR}"
