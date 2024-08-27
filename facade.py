import time

# This is the decorator factory function that accepts any number of keyword arguments
def flow(**kwargs):
    # This is ther decorator function that takes the function 'func' to be decorated
    def decorator(func):
        #This is the wrapper function that can access both the decorator’s keyword arguments (kwargs) and the original function’s arguments (args and inner_kwargs).
        def wrapper(*args, **inner_kwargs): 
            start_time = time.time()
            print("Decorator parameters:", kwargs)
            print("Inner params:", inner_kwargs)

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