import time
from database.repository import Repository
from data_store import flow_status_store
from functools import wraps

import logging
from websocket_handler import WebSocketHandler
import asyncio

current_flow = None
current_flow_run = None

# This is the decorator factory function that accepts any number of keyword arguments
def flow(**kwargs):
    
    # This is the decorator function that takes the function 'func' to be decorated
    def decorator(func):
        
        # This is the wrapper function that can access both the decorator’s keyword arguments (kwargs) and the original function’s arguments (args and inner_kwargs).
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            global current_flow, current_flow_run
            """
             INITIAL SETUP
            """
            start_time = time.time()

            """
             DATABASE CREATION
            """
            # Create a flow in the database first, if not exist
            flow_name = kwargs['name']

            # Store the flow information in the database, if not already
            db_manager = Repository()
            newFlow = db_manager.create_flow(flow_name, 'main.py')
            newFlowRun = db_manager.create_flow_run(flow_id=newFlow.flow_id)

            current_flow = newFlow
            current_flow_run = newFlowRun

            db_manager.close_session()

            """
            LOGGER SESSION STARTS HERE
            """
            # Create a logger for the flow
            logger = logging.getLogger(flow_name)
            logger.setLevel(logging.INFO)

            # Set up a WebSocket handler
            handler = WebSocketHandler("ws://localhost:8000/ws/flow_run")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # Redirect print to logger
            import sys
            from logger import LoggerWrapper
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
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")

                # Restore the original stdout
                sys.stdout = original_stdout
                logger.removeHandler(handler)

                return result
        return wrapper
    return decorator

def task(**kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            global current_flow,current_flow_run

            """
             DATABASE CREATION
            """
            db_manager = Repository()
            newTaskRun = db_manager.create_task_run(flow_run_id=current_flow_run.flow_run_id)
            db_manager.close_session()

            print(current_flow)

            result = func(*args, **inner_kwargs)
            return result
        return wrapper
    return decorator

