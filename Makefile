CONTAINER_NAME:=github-sync-api

.PHONY: build
build:
	docker build \
	-t $(CONTAINER_NAME) .

.PHONY: run
run:
	docker run -it \
		-v $(shell pwd)/settings.ini:/code/settings.ini:ro \
		-p 8092:8092 \
		$(CONTAINER_NAME)
