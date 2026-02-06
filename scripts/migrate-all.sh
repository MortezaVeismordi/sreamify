#!/bin/bash
set -e

echo "Running migrations for all services..."

cd services/auth-service/src && python manage.py migrate --noinput && cd ../../..
cd services/stream-service/src && python manage.py migrate --noinput && cd ../../..
cd services/chat-service/src && python manage.py migrate --noinput && cd ../../..
cd services/notification-service/src && python manage.py migrate --noinput && cd ../../..

echo "All migrations completed!"
