.PHONY: install load show

install:
	pip install -r requirements.txt

load:
	python  load.py

show:
	dlt pipeline spotify_pipeline show
