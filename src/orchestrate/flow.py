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

# This is the decorator factory function that accepts any number of keyword arguments
def flow(**kwargs):
    
    # This is the decorator function that takes the function 'func' to be decorated
    def decorator(func):
        
        # This is the wrapper function that can access both the decorator’s keyword arguments (kwargs) and the original function’s arguments (args and inner_kwargs).
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            """
             INITIAL SETUP
            """
            start_time = time.time()

            """
             DATABASE CREATION
            """
            # Create a flow in the database first, if not exist
            flow_name = kwargs['name']
            tags = kwargs['tags'] or None

            # Store the flow information in the database, if not already
            db_manager = Repository()
            newFlow = db_manager.create_flow(flow_name, 'main.py', tags=tags)
            newFlowRun = db_manager.create_flow_run(flow_id=newFlow.flow_id)

            globals.current_flow = newFlow
            globals.current_flow_run = newFlowRun

            """
            LOGGER SESSION STARTS HERE
            """
            logger, handler = setup(flow_name)

            # Redirect print to logger
            original_stdout = sys.stdout
            sys.stdout = LoggerWrapper(logger)

            try:
                # Send a status update when the flow starts
                asyncio.run(handler.send_status("RUNNING"))

                result = func(*args, **inner_kwargs)

                 # Send a status update when the flow completes
                asyncio.run(handler.send_status("COMPLETED"))
                return result
            except Exception as e:
                # Send a status update on error
                asyncio.run(handler.send_status("ERROR"))

                result = e
            finally:
                newFlowRun.end_time = datetime.utcnow()
                db_manager.session.commit()

                db_manager.close_session()

                # Restore the original stdout
                sys.stdout = original_stdout
                logger.removeHandler(handler)

                return result
        return wrapper
    return decorator