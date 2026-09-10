# Task 9: Memory-Safe WebSocket Connection Pool
class WebSocketPool:
    def __init__(self):
        self.active_connections = set()

    def connect(self, conn_id: str):
        self.active_connections.add(conn_id)

    def disconnect(self, conn_id: str):
        self.active_connections.discard(conn_id)

    def broadcast_count(self) -> int:
        return len(self.active_connections)
