# devops-sysprog-slutuppgift

## Setup

### Python version
Python 3.8

### About Pipenv

This project uses [Pipenv](https://github.com/pypa/pipenv) to manage python packages, but at this time the only package used is yaml.
Since it might be a bit overboard to use Pipenv (or any virtual env to begin with) for a single package (a common one at that) it's completely optional to use Pipenv.


### If you only want to install yaml and get on with it:
All commands should be issued from the project's root folder

```bash
pip install --upgrade-pip   # always update pip
pip install pyyaml          # get packages
python -m app               # run the program
```

### If you want to use pipenv:
All commands should be issued from the project's root folder


```bash
pip install --upgrade-pip   # always update pip
pip install pipenv          # install pipenv
pipenv sync                 # get packages / create env
pipenv run start            # run the program in the env created by Pipenv