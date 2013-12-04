Broken-Promises
===============

[![Build Status](https://travis-ci.org/jplusplus/broken-promises.png)](http://travis-ci.org/jplusplus/broken-promises)

## Installation


**a. Requirements**
```bash
sudo apt-get install build-essential git-core python python-pip python-dev redis-server
sudo pip install virtualenv
```
And [MongoDB](http://www.mongodb.org/downloads).

**b.  Download the project**
```bash
git clone git@github.com:jplusplus/broken-promises.git
cd broken-promises
```

**c. Install**

Will download and install all the dependances in a `venv` directory. (Virtualenv required)

```bash
make install
```

## Run the Application (API + Control Tower)

Launch Mongodb, the workers and the web application (API + Control Tower)

```bash
make run
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

__password__ : brokenpromises


![screenshot](Webapp/static/img/1-jobs.png)
![screenshot](Webapp/static/img/2-reports.png)
![screenshot](Webapp/static/img/3-scheduled.png)

## CLI

In the `Scripts/` directory.

### Collect articles for a date

```
Usage: 
./collect_articles.py [options] year 
./collect_articles.py [options] year month
./collect_articles.py [options] year month day

Options:
  -h, --help            show this help message and exit
  -f CHANNELS_FILE, --channelslistfile=CHANNELS_FILE
                        Use this that as channels list to use
  -c CHANNELS_LIST, --channels=CHANNELS_LIST
                        channels list comma separated
  -s, --storage         Save the result with the default storage
  -d, --drop            drop the previous articles from database before
  --force               Force the scrap. If --storage is enable, the scrap
                        could be escape b/c of a previous similar scrap
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        Specify  a file to write the export to. If you do not
                        specify a file name, the program writes data to
                        standard output (e.g. stdout)

```

### Scrap a given page using the appropriate channel 

```
usage: scrap_article.py [-h] [--with-filters] [--dates] url

positional arguments:
  url             url to scrap

optional arguments:
  -h, --help      show this help message and exit
  --with-filters  Apply filters to remove unwanted dates
  --dates         Return the date found in the article

```
## Run tests

	$ make test
