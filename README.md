# Github Sync API

API to fetch remote changes on Github via webhook

## Getting started

### Setup

The repos the API should manage are defined in `settings.ini`.

1. Create the [`settings.ini`](example/settings.ini) file in the root project directory with the following settings:

```ini
[repos]
some_repo=/path/to/some_repo
some_other_repo=/path/to/some_other_repo
[secrets]
token=your_github_webhook_token
[environment]
log_level=INFO
log_to_file=true
```

If you prefer, you can use environment variables:
- `TOKEN` for the token
- `LOG_LEVEL` for the log level (defaults to `ERROR`)
- `LOG_TO_FILE` logs to file when `true`

Run the following command to start the app:

```shell
docker run -it \
	-v $(shell pwd)/settings.ini:/src/settings.ini:ro \
	-p 8092:8092 \
	github-sync-api:latest
```

Be sure to mount the volumes your repos reside in and your ssh key:

```shell
docker run -it \
	-v $(HOME)/.ssh/your_github_ssh_key:/root/.ssh/your_github_ssh_key
	-v $(shell pwd)/settings.ini:/src/settings.ini:ro \
	-v /my/project/directory/some_repo/:/path/to/some_repo/ \
	-v /my/project/directory/some_other_repo/:/path/to/some_other_repo/ \
	-p 8092:8092 \
	github-sync-api:latest
```

Alternatively, you can use `docker compose` like the [example](example/docker-compose.yaml).

> WARNING: By default, the container checks for updated GitHub fingerprints from https://api.github.com/meta and updates 
> them in `known_hosts` automatically. If you find this too insecure, set the environment variable
> `AUTO_UPDATE_FINGERPRINT=False` and manually manage `known_hosts` yourself.
