VENV=env/bin/

run: install
	$(VENV)python main.py

install:
	python3 -m venv env
	$(VENV)pip install -r requirements.txt
