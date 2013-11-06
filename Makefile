# Makefile -- Broken Promises

WEBAPP     = $(wildcard */webapp.py)
TEST       = Tests/all.py
VIRTUALENV = venv/

run:
	mongod&
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/Sources/:`pwd`/Webapp/:$(PYTHONPATH) ; python $(WEBAPP)

install:
	virtualenv venv --no-site-packages --distribute --prompt=BrokenPromises
	. $(VIRTUALENV)bin/activate ; pip install -r requirements.txt

test:
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/Sources/:`pwd`/Webapp/:$(PYTHONPATH) ; python $(TEST)

# EOF
