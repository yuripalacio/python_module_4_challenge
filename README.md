<h1 align="center"> 
  Python Module 4 challenge
</h1>

<p align="center">	
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/yuripalacio/python_module_4_challenge">

  <a href="https://www.linkedin.com/in/yuripalacio/">
    <img alt="Made by yuripalacio" src="https://img.shields.io/badge/made%20by-Yuri%20Palacio-%2304D361">
  </a>
  
  <a href="https://github.com/yuripalacio/mychat/commits/master">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/yuripalacio/python_module_4_challenge">
  </a>
</p>

<p align="center">
  <a href="#introduction">Introduction</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#execution">Execution</a>
</p>

## Introduction
This project aims to reinforce the basic concepts learned in my first module of a Python course.
Here we have a simple project executed via the command line, simulating a contact schedule.

## Execution
1. Check if you have Python installed on your machine(I used Python `3.11.5`)

2. Perform the project clone.
    ```bash
    git clone https://github.com/yuripalacio/python_module_4_challenge.git
    ```

3. Access the project folder.
    ```bash
    cd python_module_1_challenge
    ```

4. Create a virtual environment. I used `conda` for that.
    ```bash
    conda create --name python-module-4-challenge python=3.11.15
    conda activate python-module-4-challenge
    ```

5. Install the project dependencies.
    ```bash
    pip3 install -r requirements.txt --upgrade
    ```

6. Rename the file `env.example` to `.env`

7. Turn up the container with `docker-compose` file.
    ```bash
    docker-compose up -d
    ```

8. Execute the project.
    ```bash
    python3 ./app.py
    ```

By [Yuri Palacio](https://www.linkedin.com/in/yuri-palacio/) :wave:
