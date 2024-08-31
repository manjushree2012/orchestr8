from facade import flow
def first_task(num1, num2):
    total = 0
    for i in range(1000000):
        total += i
    return total

@flow(name="Transforming X to Y on an schedule")
def migrate():
    # Do something time consuming here
    print("This is a log message from the flow.")
    print("Another log message.")
    
    first_task(100,200)
    return 1

if __name__ == '__main__':
    migrate()
