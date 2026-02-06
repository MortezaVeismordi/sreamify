# Architecture

Streamify is built using a microservices architecture.

## Services

- **auth-service**: User authentication and authorization
- **stream-service**: Stream management and video processing
- **chat-service**: Real-time chat functionality
- **notification-service**: Email and push notifications

## Infrastructure

- **PostgreSQL**: Database for all services
- **Redis**: Caching and session storage
- **RabbitMQ**: Message queue for async tasks
- **Nginx**: API gateway and reverse proxy
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **ELK Stack**: Logging and log analysis

## Communication

- REST APIs for synchronous communication
- WebSockets for real-time chat
- Message queues for async processing
- gRPC for inter-service communication (planned)
