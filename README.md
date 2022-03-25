yieldcurves
====

Interface to search and analyze sovereign bond yields.


[//]: # (hidden GIF url below)

![](assets/demo.gif)

[//]: # (hidden GIF url above)


Requirements
-----

This project requires `python3` and, optionally, `mongodb` which is used for caching
data requests into a local database instance. Running without it is possible, but
discouraged (significantly slower).

* `python >= 3.7`
* `mongodb >= 4.0` (optional)

To install MongoDB, see [here](https://www.mongodb.com/docs/manual/installation/).

Setup
-----

Simply clone this repository and install the dependencies.

```shell
# Clone the repo
git clone git@github.com:felipeslanza/yieldcurves.git

# Setup environment and install dependencies
cd yieldcurves
virtualenv -p python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```


Usage
-----

Launch the `streamlit`-based app:

```shell
streamlit run yieldcurves/__main__.py
```
