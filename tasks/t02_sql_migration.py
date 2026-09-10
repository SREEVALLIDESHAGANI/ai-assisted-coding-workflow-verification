# Task 2: SQL Migration Up & Down Schema Manager
class MigrationManager:
    def __init__(self):
        self.applied_migrations = []
        self.schema_state = {}

    def up(self):
        """Applies schema migration adding audit table."""
        self.schema_state["users"] = ["id", "username", "created_at"]
        self.schema_state["audit_logs"] = ["id", "user_id", "action", "timestamp"]
        self.applied_migrations.append("2026_01_add_audit_logs")
        return True

    def down(self):
        """Rolls back schema migration cleanly."""
        if "2026_01_add_audit_logs" in self.applied_migrations:
            self.schema_state.pop("audit_logs", None)
            self.applied_migrations.remove("2026_01_add_audit_logs")
            return True
        return False
