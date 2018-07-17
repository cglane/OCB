# These targets are not files
.PHONY: install sandbox docs coverage lint messages compiledmessages css clean sandbox_image

install:
	pip install -r requirements.txt

sandbox_image:
	docker build -t django-oscar-sandbox:latest .

docs:
	cd docs && make html

test:
	py.test 

retest:
	py.test --lf 

coverage:
	py.test --cov=oscar --cov-report=term-missing

lint:
	flake8 src/oscar/
	flake8 tests/
	isort -q --recursive --diff src/
	isort -q --recursive --diff tests/

testmigrations:
	pip install -r requirements_migrations.txt
	cd sandbox && ./test_migrations.sh

messages:
	# Create the .po files used for i18n
	cd src/oscar; django-admin.py makemessages -a

compiledmessages:
	# Compile the gettext files
	cd src/oscar; django-admin.py compilemessages

css:
	npm install
	npm run build

clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt

todo:
	# Look for areas of the code that need updating when some event has taken place (like 
	# Oscar dropping support for a Django version)
	-grep -rnH TODO *.txt
	-grep -rnH TODO src/oscar/apps/
	-grep -rnH "django.VERSION" src/oscar/apps


release: clean
	pip install twine wheel
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload -s dist/*
