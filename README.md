# Github Sync API

API to fetch remote changes on Github via webhook

## Getting started

The repos the API should manage are defined in `settings.ini`.

Create the `settings.ini` file in the root project directory with the following settings:

```ini
[repos]
some_repo=/path/to/some_repo
some_other_repo=/path/to/some_other_repo
[secrets]
token=your_github_webhook_token
```

Run the following command to start the repo:

```shell
docker run -it \
		-v $(shell pwd)/settings.ini:/code/settings.ini:ro \
		-p 8092:8092 \
		$(CONTAINER_NAME)
```


