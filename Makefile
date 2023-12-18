CONTAINER_NAME:=github-sync-api

.PHONY: build
build:
	docker build \
	-t $(CONTAINER_NAME) .

.PHONY: run
run:
	docker run -it --env-file .env -p 8092:8092 $(CONTAINER_NAME)
