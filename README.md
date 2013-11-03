Broken-Promises
===============

## Installation


**a. Prerequired**
```bash
sudo apt-get install build-essential git-core python python-pip python-dev
sudo pip install virtualenv
```

**b.  Download the project**
```bash
git clone git@github.com:jplusplus/broken-promises.git
cd broken-promises
```

**c. Install**
```bash
make install
```

## Run Web Application
```bash
make run
```

Then visit [http://127.0.0.1/ui/](http://127.0.0.1/ui/)

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
