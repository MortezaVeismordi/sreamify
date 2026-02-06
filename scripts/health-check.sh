#!/bin/bash

echo "Checking service health..."

check_service() {
    local service=$1
    local port=$2
    
    if curl -f http://localhost:$port/health > /dev/null 2>&1; then
        echo "✓ $service is healthy"
    else
        echo "✗ $service is down"
    fi
}

check_service "auth-service" 8001
check_service "stream-service" 8002
check_service "chat-service" 8003
check_service "notification-service" 8004
