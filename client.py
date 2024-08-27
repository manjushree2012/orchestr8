import time
def task(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print("An exceptopn occcured")
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")
            return func(*args, **kwargs)
    print('INSIDE TASK WRAPPER')
    return wrapper

def flow(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print("An exceptopn occcured")
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")
            return func(*args, **kwargs)
    print('INSIDE FLOW WRAPPER')
    return wrapper

@task
def first_task(num1, num2):
    total = 0
    for i in range(1000000):
        total += i
    return total

@flow
def migrate():
    # Do something time consuming here
    first_task(100,200)
    return 1

if __name__ == '__main__':
    migrate()
