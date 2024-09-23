# Orchestrate

Orchestrate is a framework to maintain data workflows, orchestrate flows, keep track of flow history in Python. Inspired by *[Prefect](https://www.prefect.io/ "Prefect")*,  Orchestrate allows its users to build resilient and dynamic data pipelines,  and keep platform to monitor history of each flow.

Easy to use because of its low to zero learning curve, you can integrate Orchestrate in your python project instantly. No need to memorize syntax. Just add a simple decorator from Orchestate and the rest will be taken care of.

## Before getting started
Please note that Orchestrate is currently in actve developement stage.  Please do not use it in an production environment.

## Getting Started
Orchestrate requires Python >=3.9  Since the application is currently in development stage, you can try it out by installating via the pypi package manager. 
[https://test.pypi.org/project/orchestrate/](https://test.pypi.org/project/orchestrate/)

To install, open the terminal in the root directory of your project, and:
```bash
pip install -i https://test.pypi.org/simple/ orchestrate
```

A hello world application for Orchestrate would look like this:
```python
#main.py
from orchestrate import flow, task
import httpx

@task
def get_coffee_data():
    url = "https://api.sampleapis.com/coffee/hot"
    data = httpx.get(url).json()
    return data

@task
def get_wine_data():
    url = "https://api.sampleapis.com/beers/ale"
    data = httpx.get(url).json()
    return data

@flow(name="Food Enquiry")
def enquire_food():
    get_coffee_data()
    get_wine_data()

# run the flow!
if __name__=="__main__":
    enquire_food()
```

To start the orchestrate server, enter the following command:
```bash
orchestrate server start
```

In order to run a flow,you need to run the python file containing the flow definition. In our example, the command would be:
```bash
py main.py
```


## Screenshots
![Screenshot 2024-09-22 141333](https://github.com/user-attachments/assets/e0f7f664-839b-41e1-b08e-b86843953a0f)

![Screenshot 2024-09-22 141618](https://github.com/user-attachments/assets/cd67d7d4-75b9-4881-8610-ab0f90b8e2a2)


