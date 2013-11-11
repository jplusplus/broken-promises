Broken-Promises
===============

[![Build Status](https://travis-ci.org/jplusplus/broken-promises.png)](http://travis-ci.org/jplusplus/broken-promises)

## Installation


**a. Requirements**
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
Usage: 
./collect_articles.py [options] year 
./collect_articles.py [options] year month
./collect_articles.py [options] year month day

Options:
  -h, --help            show this help message and exit
  -C, --nocache         Prevents from using the cache
  -f CHANNELS_FILE, --channelslistfile=CHANNELS_FILE
                        Use this that as channels list to use
  -c CHANNELS_LIST, --channels=CHANNELS_LIST
                        channels list comma separated
  -m MONGODB_URI, --mongodb=MONGODB_URI
                        uri to mongodb instance to persist results
  -d, --drop            drop the previous articles from database before
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        Specify  a file to write the export to. If you do not
                        specify a file name, the program writes data to
                        standard output (e.g. stdout)
```

## Run tests

	$ make test
