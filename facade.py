import time
from database.repository import Repository

# This is the decorator factory function that accepts any number of keyword arguments
def flow(**kwargs):
    # This is ther decorator function that takes the function 'func' to be decorated
    def decorator(func):
        #This is the wrapper function that can access both the decorator’s keyword arguments (kwargs) and the original function’s arguments (args and inner_kwargs).
        def wrapper(*args, **inner_kwargs): 
            start_time = time.time()
            print("Decorator parameters:", kwargs)
            print("Inner params:", inner_kwargs)

            # Create a flow in the database first, if not exist
            flow_name = kwargs['name']
            print(flow_name)

            # GET THE ENTRY POINT OF THAT FLOW HERE
            print(' Function here')
            print(func.__module__)
            print(func.__name__)


            db_manager = Repository()
            newFlow = db_manager.create_flow(flow_name, 'main.py')
            newFlowRun = db_manager.create_flow_run(flow_id=newFlow.id)
            db_manager.close_session()

            try:
                result = func(*args, **inner_kwargs)
                return result
            except Exception as e:
                print("An exception occcured")
                result = e
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")
                return result
        return wrapper
    return decorator