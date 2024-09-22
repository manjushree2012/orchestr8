import logging
from src.orchestrate import globals

class DatabaseHandler(logging.Handler):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

    def emit(self, record ):
        # Create a log entry in the database
        log_entry = self.format(record)
        self.db_manager.create_log(
            flow_run_id= globals.current_flow_run.flow_run_id,
            # task_run_id= task_run_id,
            level=record.levelname,
            message=log_entry
        )