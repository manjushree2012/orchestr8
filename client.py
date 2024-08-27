from facade import flow
def first_task(num1, num2):
    total = 0
    for i in range(1000000):
        total += i
    return total

@flow(name="Transforming X to Y on an schedule")
def migrate():
    # Do something time consuming here
    first_task(100,200)
    return 1

if __name__ == '__main__':
    migrate()
