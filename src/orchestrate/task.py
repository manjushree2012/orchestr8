import time
from src.orchestrate.server.database.repository import Repository
from src.orchestrate.data_store import flow_status_store
from functools import wraps
import asyncio
from src.orchestrate.logger.log import setup
import sys
from src.orchestrate.logger.wrapper import LoggerWrapper
from datetime import datetime


from src.orchestrate import globals

def task(**kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **inner_kwargs):

            """
             DATABASE CREATION
            """
            db_manager = Repository()
            newTaskRun = db_manager.create_task_run(flow_run_id=globals.current_flow_run.flow_run_id)
            try:
                result = func(*args, **inner_kwargs)
                return result
            except Exception as e:
                result = e
            finally:
                newTaskRun.end_time = datetime.utcnow()
                db_manager.session.commit()

                return result
        return wrapper
    return decorator