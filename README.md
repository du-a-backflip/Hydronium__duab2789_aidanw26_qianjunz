# HydroChef by Hydronium

## Roster

**Project Manager (Frontend):** Dua Baig

**Backend (Database and API Functions):** Aidan Wong

**Backend (Python Logic and Website Flow):** Qianjun Zhou

## Site Description

This project is a multifunctional cooking website that contains recipes for every occasion. Users can search a collection of recipes drawn from an API and other users and contribute and save recipes from this collection. They can also edit recipes to add details, clarify a vague concept, or revise an incorrect recipe step. Users also have access to a holiday calendar, which is used to explore recipes for various holidays, and a random recipe generator for days they are unsure what to cook. This website can be viewed without an account but requires one to contribute and save recipes from the recipe collection. 

## Install Guide

**Prerequisites**

Ensure that **Git** and **Python** are installed on your machine. It is recommended that you use a virtual machine when running this project to avoid any possible conflicts. For help, refer to the following documentation:
   1. Installing Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git 
   2. Installing Python: https://www.python.org/downloads/ 

   3. (Optional) Setting up Git with SSH (Ms. Novillo's APCSA Guide): https://novillo-cs.github.io/apcsa/tools/ 
         

**Cloning the Project**
1. Create Python virtual environment:

```
$ python3 -m PATH/TO/venv_name
```

2. Activate virtual environment 

   - Linux: `$ . PATH/TO/venv_name/bin/activate`
   - Windows (PowerShell): `> . .\PATH\TO\venv_name\Scripts\activate`
   - Windows (Command Prompt): `>PATH\TO\venv_name\Scripts\activate`
   - macOS: `$ source PATH/TO/venv_name/bin/activate`

   *Notes*

   - If successful, command line will display name of virtual environment: `(venv_name) $ `

   - To close a virtual environment, simply type `$ deactivate` in the terminal


3. In terminal, clone the repository to your local machine: 

HTTPS METHOD (Recommended)

```
$ git clone https://github.com/du-a-backflip/Hydronium__duab2789_aidanw26_qianjunz.git        
```

SSH METHOD (Requires SSH Key to be set up):

```
$ git clone git@github.com:du-a-backflip/Hydronium__duab2789_aidanw26_qianjunz.git
```

4. Navigate to project directory

```
$ cd PATH/TO/Hydronium__duab2789_aidanw26_qianjunz/
```

5. Install dependencies

```
$ pip install -r requirements.txt
```
        
# Launch Codes

1. Navigate to project directory:

```
$ cd PATH/TO/Hydronium__duab2789_aidanw26_qianjunz/
```
 
2. Navigate to 'app' directory

```
 $ cd app/
```

3. Run App

```
 $ python3 __init__.py
```
4. Open the link that appears in the terminal to be brought to the website
    - You can visit the link via several methods:
        - Control + Clicking on the link
        - Typing/Pasting http://127.0.0.1:5000 in any browser
    - To close the app, press control + C when in the terminal

```    
* Running on http://127.0.0.1:5000
``` 
