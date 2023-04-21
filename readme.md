# Chessr

This project is build with Python 3.10.10.

The Python solution is set-up for Visual Studio Code, and the C++ solution for Visual Studio.

## Environment Variables

The C++ solution expects an environment variable called PYTHONDIR containing your Python folder.

The Python solution expects an environment variable called PYTHONPATH containing the 'build' folder at the root of the solution.

## Packages

Use the requirements file in the Python solution to create an environment as the C++ solution accesses the installed packages. From within the `Chessr.Python` folder:

```
python -m venv .env
```

...and then with the environment activated:

```
pip install -r requirements.txt
```
