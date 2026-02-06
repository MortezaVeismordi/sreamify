#!/bin/bash
set -e

echo "Initializing databases..."

# Create databases for each service
psql -U postgres -c "CREATE DATABASE streamify_auth;"
psql -U postgres -c "CREATE DATABASE streamify_streams;"
psql -U postgres -c "CREATE DATABASE streamify_chat;"
psql -U postgres -c "CREATE DATABASE streamify_notifications;"

echo "Databases created successfully!"
