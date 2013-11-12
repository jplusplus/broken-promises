# Makefile -- Broken Promises

WEBAPP     = $(wildcard */webapp.py)
TEST       = Tests/all.py

run:
	mongod&
	. `pwd`/.env ; python $(WEBAPP)

install:
	virtualenv venv --no-site-packages --distribute --prompt=BrokenPromises
	. `pwd`/.env ; pip install -r requirements.txt

test:
	. `pwd`/.env ; python $(TEST)

# EOF
