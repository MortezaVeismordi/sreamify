#!/bin/bash
set -e

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Backing up databases..."

pg_dump -U postgres streamify_auth > $BACKUP_DIR/auth_$DATE.sql
pg_dump -U postgres streamify_streams > $BACKUP_DIR/streams_$DATE.sql
pg_dump -U postgres streamify_chat > $BACKUP_DIR/chat_$DATE.sql
pg_dump -U postgres streamify_notifications > $BACKUP_DIR/notifications_$DATE.sql

echo "Backup completed!"
