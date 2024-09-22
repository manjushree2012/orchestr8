# Orchestrate

Orchestrate is a framework to maintain data workflows, orchestrate flows, keep track of flow history in Python. Inspired by *[Prefect](https://www.prefect.io/ "Prefect")*,  Orchestrate allows its users to build resilient and dynamic data pipelines,  and keep platform to monitor history of each flow.

Easy to use because of its low to zero learning curve, you can integrate Orchestrate in your python project instantly. No need to memorize syntax. Just add a simple decorator from Orchestate and the rest will be taken care of.

## Before getting started
Please note that Orchestrate is currently in actve developement stage.  Please do not use it in an production environment.

## Getting Started
Orchestrate requires Python >=3.9  Since the application is currently in development stage, you can try it out by installating via the pypi package manager. 
[https://test.pypi.org/project/orchestrate/](https://test.pypi.org/project/orchestrate/)

To install, open the terminal in the root directory of your project, and:
`pip install -i https://test.pypi.org/simple/ orchestrate`

For this tutorial, we will just create a simple application.

```python
from prefect import flow, task
from typing import list
import httpx


@task(log_prints=True)
def get_stars(repo: str):
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    print(f"{repo} has {count} stars!")


@flow(name="GitHub Stars")
def github_stars(repos: list[str]):
    for repo in repos:
        get_stars(repo)


# run the flow!
if __name__=="__main__":
    github_stars(["PrefectHQ/Prefect"])
```

