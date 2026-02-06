# Data Flow

## User Registration Flow

1. Client sends registration request to Auth Service
2. Auth Service validates data and creates user
3. Auth Service generates JWT tokens
4. Client receives tokens and stores them

## Stream Creation Flow

1. Client sends stream creation request with JWT token
2. Nginx validates token via Auth Service
3. Request forwarded to Stream Service
4. Stream Service creates stream and stores in database
5. Response returned to client

## Chat Message Flow

1. Client connects via WebSocket to Chat Service
2. Client sends message
3. Chat Service broadcasts to all connected clients
4. Message stored in database
