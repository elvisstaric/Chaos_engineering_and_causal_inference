#!/bin/bash

# Stress Testing Scripts for Docker Containers
# Usage: source stress_scripts.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if container exists
check_container() {
    local container=$1
    if ! docker ps --format "table {{.Names}}" | grep -q "^${container}$"; then
        echo -e "${RED}❌ Container '${container}' not found or not running${NC}"
        return 1
    fi
    return 0
}

# Function to install stress-ng in a container
install_stress_ng() {
    local container=$1
    echo -e "${BLUE}📦 Installing stress-ng in ${container}...${NC}"
    
    if check_container "$container"; then
        docker exec "$container" bash -c "
            if command -v apt-get &> /dev/null; then
                apt-get update && apt-get install -y stress-ng
            elif command -v yum &> /dev/null; then
                yum install -y stress-ng
            elif command -v apk &> /dev/null; then
                apk add stress-ng
            else
                echo 'No package manager found. Please install stress-ng manually.'
                exit 1
            fi
        "
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ stress-ng installed successfully in ${container}${NC}"
        else
            echo -e "${RED}❌ Failed to install stress-ng in ${container}${NC}"
        fi
    fi
}

# CPU Stress Test
cpu_stress() {
    local container=$1
    local duration=${2:-60}
    local workers=${3:-4}
    
    echo -e "${BLUE}🔥 Running CPU stress test on ${container}${NC}"
    echo -e "   Duration: ${duration}s"
    echo -e "   Workers: ${workers}"
    
    if check_container "$container"; then
        docker exec "$container" stress-ng --cpu "$workers" --timeout "${duration}s" --metrics
    fi
}

# Memory Stress Test
memory_stress() {
    local container=$1
    local duration=${2:-60}
    local workers=${3:-2}
    local bytes=${4:-"512M"}
    
    echo -e "${BLUE}💾 Running memory stress test on ${container}${NC}"
    echo -e "   Duration: ${duration}s"
    echo -e "   Workers: ${workers}"
    echo -e "   Memory per worker: ${bytes}"
    
    if check_container "$container"; then
        docker exec "$container" stress-ng --vm "$workers" --vm-bytes "$bytes" --timeout "${duration}s" --metrics
    fi
}

# Memory Leak Test
memory_leak_test() {
    local container=$1
    local duration=${2:-120}
    local bytes=${3:-"1G"}
    
    echo -e "${BLUE}🔍 Running memory leak test on ${container}${NC}"
    echo -e "   Duration: ${duration}s"
    echo -e "   Memory: ${bytes} (kept allocated)"
    
    if check_container "$container"; then
        docker exec "$container" stress-ng --vm 1 --vm-bytes "$bytes" --vm-keep --timeout "${duration}s" --metrics
    fi
}

# Mixed Stress Test (CPU + Memory)
mixed_stress() {
    local container=$1
    local duration=${2:-60}
    
    echo -e "${BLUE}⚡ Running mixed stress test on ${container}${NC}"
    echo -e "   Duration: ${duration}s"
    echo -e "   CPU workers: 2"
    echo -e "   Memory workers: 1 (256M each)"
    
    if check_container "$container"; then
        docker exec "$container" stress-ng --cpu 2 --vm 1 --vm-bytes 256M --timeout "${duration}s" --metrics
    fi
}

# I/O Stress Test
io_stress() {
    local container=$1
    local duration=${2:-60}
    local workers=${3:-4}
    
    echo -e "${BLUE}💿 Running I/O stress test on ${container}${NC}"
    echo -e "   Duration: ${duration}s"
    echo -e "   Workers: ${workers}"
    
    if check_container "$container"; then
        docker exec "$container" stress-ng --io "$workers" --timeout "${duration}s" --metrics
    fi
}

# Network Stress Test
network_stress() {
    local container=$1
    local duration=${2:-60}
    local workers=${3:-2}
    
    echo -e "${BLUE}🌐 Running network stress test on ${container}${NC}"
    echo -e "   Duration: ${duration}s"
    echo -e "   Workers: ${workers}"
    
    if check_container "$container"; then
        docker exec "$container" stress-ng --sock "$workers" --timeout "${duration}s" --metrics
    fi
}

# Comprehensive Stress Test
comprehensive_stress() {
    local container=$1
    local duration=${2:-300}
    
    echo -e "${BLUE}🎯 Running comprehensive stress test on ${container}${NC}"
    echo -e "   Total Duration: ${duration}s"
    echo -e "   Tests: CPU, Memory, Mixed, I/O, Network"
    
    if check_container "$container"; then
        local test_duration=$((duration / 5))
        
        echo -e "\n${YELLOW}--- CPU Stress Test ---${NC}"
        cpu_stress "$container" "$test_duration" 4
        sleep 5
        
        echo -e "\n${YELLOW}--- Memory Stress Test ---${NC}"
        memory_stress "$container" "$test_duration" 2 "512M"
        sleep 5
        
        echo -e "\n${YELLOW}--- Mixed Stress Test ---${NC}"
        mixed_stress "$container" "$test_duration"
        sleep 5
        
        echo -e "\n${YELLOW}--- I/O Stress Test ---${NC}"
        io_stress "$container" "$test_duration" 4
        sleep 5
        
        echo -e "\n${YELLOW}--- Network Stress Test ---${NC}"
        network_stress "$container" "$test_duration" 2
        
        echo -e "\n${GREEN}✅ Comprehensive stress test completed!${NC}"
    fi
}

# Monitor container resources during stress test
monitor_container() {
    local container=$1
    local duration=${2:-60}
    
    echo -e "${BLUE}📊 Monitoring ${container} for ${duration} seconds...${NC}"
    
    if check_container "$container"; then
        # Start monitoring in background
        (
            while [ $duration -gt 0 ]; do
                echo -e "\n${YELLOW}--- $(date) ---${NC}"
                docker stats "$container" --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
                sleep 5
                duration=$((duration - 5))
            done
        ) &
        
        local monitor_pid=$!
        wait $monitor_pid
    fi
}

# Run stress test with monitoring
stress_with_monitoring() {
    local container=$1
    local stress_type=$2
    local duration=${3:-60}
    
    echo -e "${BLUE}🚀 Running ${stress_type} stress test with monitoring on ${container}${NC}"
    
    # Start monitoring in background
    monitor_container "$container" "$duration" &
    local monitor_pid=$!
    
    # Run stress test
    case "$stress_type" in
        "cpu")
            cpu_stress "$container" "$duration"
            ;;
        "memory")
            memory_stress "$container" "$duration"
            ;;
        "leak")
            memory_leak_test "$container" "$duration"
            ;;
        "mixed")
            mixed_stress "$container" "$duration"
            ;;
        "io")
            io_stress "$container" "$duration"
            ;;
        "network")
            network_stress "$container" "$duration"
            ;;
        "comprehensive")
            comprehensive_stress "$container" "$duration"
            ;;
        *)
            echo -e "${RED}❌ Unknown stress type: ${stress_type}${NC}"
            echo -e "Available types: cpu, memory, leak, mixed, io, network, comprehensive"
            return 1
            ;;
    esac
    
    # Wait for monitoring to complete
    wait $monitor_pid
}

# Quick test all services
test_all_services() {
    local duration=${1:-60}
    local services=("chaos+causal-user_service-1" "chaos+causal-inventory_service-1" "chaos+causal-cart_service-1" "chaos+causal-order_service-1")
    
    echo -e "${BLUE}🎯 Testing all services with ${duration}s stress tests${NC}"
    
    for service in "${services[@]}"; do
        if check_container "$service"; then
            echo -e "\n${YELLOW}--- Testing ${service} ---${NC}"
            stress_with_monitoring "$service" "comprehensive" "$duration"
        fi
    done
    
    echo -e "\n${GREEN}✅ All service tests completed!${NC}"
}

# Help function
show_help() {
    echo -e "${BLUE}Stress Testing Scripts for Docker Containers${NC}"
    echo ""
    echo "Available functions:"
    echo "  install_stress_ng <container>                    - Install stress-ng in container"
    echo "  cpu_stress <container> [duration] [workers]      - CPU stress test"
    echo "  memory_stress <container> [duration] [workers] [bytes] - Memory stress test"
    echo "  memory_leak_test <container> [duration] [bytes] - Memory leak test"
    echo "  mixed_stress <container> [duration]              - Mixed CPU/Memory test"
    echo "  io_stress <container> [duration] [workers]      - I/O stress test"
    echo "  network_stress <container> [duration] [workers]  - Network stress test"
    echo "  comprehensive_stress <container> [duration]      - Comprehensive test suite"
    echo "  monitor_container <container> [duration]         - Monitor container resources"
    echo "  stress_with_monitoring <container> <type> [duration] - Run stress test with monitoring"
    echo "  test_all_services [duration]                     - Test all services"
    echo ""
    echo "Examples:"
    echo "  source stress_scripts.sh"
    echo "  install_stress_ng chaos+causal-user_service-1"
    echo "  cpu_stress chaos+causal-user_service-1 120 8"
    echo "  stress_with_monitoring chaos+causal-user_service-1 comprehensive 300"
    echo "  test_all_services 180"
}

# Show help when script is sourced
echo -e "${GREEN}✅ Stress testing functions loaded!${NC}"
echo -e "Type 'show_help' to see available functions" 