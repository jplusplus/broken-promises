Broken-Promises
===============

## Installation

### 1. Set up your python environment

**a. Install python packages:**

```bash
sudo apt-get install build-essential git-core python python-pip python-dev
```

**b. Install virtualenv** a tool to isolate your dependencies

```bash
sudo pip install virtualenv
```

**c.  Download the project**
```bash
git clone git@github.com:jplusplus/broken-promises.git
```

**d.  Create the virtualenv folder for this project**
  > Every python dependencies will be installed in this folder to keep your system's environment clean.

```bash
cd broken-promises
virtualenv venv --no-site-packages --distribute --prompt=BrokenPromises
```

**e. Activate your new virtualenv**

```bash
source .env
```
  > Tips: you can install [autoenv](https://github.com/kennethreitz/autoenv) to source this file automatically each time you `cd` this folder.

### 2. Install dependencies
**a. Install python modules required**

```bash
pip install -r requirements.txt
```

## CLI

### Usage

	$ ./Scripts/collect_articles.py


```
Options:
  -h, --help            show this help message and exit
  -C, --nocache         Prevents from using the cache
  -f CHANNELS_FILE, --channelslistfile=CHANNELS_FILE
                        Use this that as channels list to use
  -c CHANNELS_LIST, --channels=CHANNELS_LIST
                        channels list comma separated
```

## Run tests

	$ python Tests/all.py
