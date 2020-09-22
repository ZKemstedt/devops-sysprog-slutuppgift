# devops-sysprog-slutuppgift

## Setup

### Python version
This project was written in Python 3.8.5, but any python 3.6 or higher should work fine.

### About Pipenv

This project uses [Pipenv](https://github.com/pypa/pipenv) to manage python packages, but at this time the only one used is yaml.
Therefore it might be a bit overboard to use Pipenv for this project. Therefore it's completely optional to use Pipenv.


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