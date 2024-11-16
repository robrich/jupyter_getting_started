The Culture of Python
=====================

This is a demo of getting started with Jupyter, and shows the culture of Python.

Install
-------

You can use [Anaconda](https://www.anaconda.com/) or Python to run Jupyter. Anaconda is great for the non-geeks. We'll use Python.

1. Create a virtual environment:

   ```
   python -m venv .venv
   ```

   Activate it:

   Linux:
   ```
   source .venv/bin/activate
   ```

   Windows Powershell:
   ```
   .venv/Scripts/activate
   ```

   Windows Batch:
   ```
   .venv/Scripts/activate.bat
   ```

2. Install Python libraries:

   ```
   pip install -r requirements.txt
   ```


Run Jupyter
-----------

Pick one:

### Launch as a web page:

```
jupyter notebook
```

then open the browser as directed in the console output

OR

### Launch in VS Code:

1. Install [VS Code](https://code.visualstudio.com/download)

2. Install the [Python extension](hurchofjesuschrist.org) and/or the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter). (The Python extension installs the Jupyter extension too)

3. Choose the Python environment:

   a. cntrl-shift-P

   b. type `Python: Select interpreter`

   c. choose the line with `.ven` in it


Playing with Jupyter
--------------------

1. Open `1-fibonacci.ipynb`

2. Run each cell by clicking the triangle to the left of each code block


Use case 1: Data transform from MSSQL to Postgres
-------------------------------------------------

The main libraries are:

- [SqlAlchemy](https://pypi.org/project/SQLAlchemy/): SQL ORM (requires drivers)
- [Pandas](https://pypi.org/project/pandas/): data processing

1. Start the databases

   ```
   docker-compose up
   ```

   This will launch SQL Server and Postgres and load up data into SQL Server

2. Open `2-etl.ipynb`

3. Run each cell by clicking the triangle to the left of each code block


Use case 2: Debugging an app with a Runbook
-------------------------------------------

1. Open `3-runbook.ipynb`

2. Run each cell by clicking the triangle to the left of each code block


Use case 3: Graphing data
-------------------------

The main libraries here are:

- [NumPy](https://pypi.org/project/numpy/): scientific math
- [Pandas](https://pypi.org/project/pandas/): data processing, [data frames](data-frames.png)
- [MatPlotLib](https://pypi.org/project/matplotlib/): graphing library

1. Open `4-graphing.ipynb`

2. Run each cell by clicking the triangle to the left of each code block

3. Start the databases if they're not running already

   ```
   docker-compose up
   ```

4. Open `5-graph-from-db.ipynb`

5. Run each cell by clicking the triangle to the left of each code block


Moving from notebooks to Python program
---------------------------------------

1. Open VS Code

2. Right-click on a notebook and choose `Import notebook to script`

3. Save as, renaming to `myapp.py`

4. Run the program: `python myapp.py`


API to stream graphs
--------------------

1. Run the api:

   `uvicorn 6-api:app --reload`

2. Go to http://127.0.0.1:8000/docs

3. Play with each endpoint


License
-------

MIT
