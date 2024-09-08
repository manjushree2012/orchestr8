from facade import flow, task

@task(name='fetch-api-data')
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
    
    sum = first_task(num1=100,num2=200)
    return sum

if __name__ == '__main__':
    migrate()
