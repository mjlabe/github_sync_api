CONTAINER_NAME:=github-sync-api

.PHONY: build
build:
	docker build \
	-t $(CONTAINER_NAME) .

.PHONY: buildnc
buildnc:
	docker build \
	--no-cache \
	-t $(CONTAINER_NAME) .

.PHONY: run
run:
	docker run -it \
		-v $(shell pwd)/settings.ini:/src/settings.ini:ro \
		-p 8092:8092 \
		$(CONTAINER_NAME)

.PHONY: up
up:
	docker compose down
	docker compose up