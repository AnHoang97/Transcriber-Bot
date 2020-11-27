run: build
	docker run transcriberbot
	
build:
	docker build -t transcriberbot:latest .
