# src/modules folder
This folder is set up as a local package.

To install it in the virtualenv the command is:
```
pip install -e ${PROJECT_PATH}/src/modules
```

If we do any changes to the package, after commiting to the repository the changes, we have to update the pip requirements.

```
pip freeze > setup/requirements.txt
```

And when pulling we need to reinstall wit pip
```
pip install requirements.txt
```