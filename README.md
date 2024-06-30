# Database Backup Solution

## Files Used in the Solution

### Python Backup Script: `backup.py`
- Creates encrypted backups of a PostgreSQL database.
- Removes old backups based on a retention period.
- Executes inside a Docker container in Linux servers.

### Dockerfile: `Dockerfile`
- Sets up the container environment for the backup script.
- Installs necessary packages for the server.
- Makes the Entrypoint script executable.

### Entrypoint Script: `entrypoint.sh`
Runs the backup script inside the Docker container using the `bash` shell.

### Crontab Configuration: `cronjob`
- Runs the Docker container at 03:00 and 14:00 UTC every day.
- Passes environment variables from the `env-file` to the container.
- Mounts the backup directory from the server to the container, ensuring that backups are stored persistently.

### Docker Compose Configuration: `docker-compose.yml`
Simplifies the management of the Docker container, environment variables, and volumes.

### Environment File: `env-file`
Stores database credentials (host, port, user, password, and name), path to the backup directory, GPG public key, and number of retention days.

## Packages Required for the Linux Server

- Docker
- Docker Compose
- GPG: `gnupg`
- PostgreSQL client: `postgresql-client`

### How to Install Docker and Docker Compose
1. [Uninstall old versions](https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions)
2. [Install using the `apt` repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

### How to Install GPG Outside the Docker Container
```bash
sudo apt-get update
sudo apt-get install -y gnupg
```

### About the PostgreSQL Client and GPG Packages
- In addtion to being installed outside the Docker container, `gnupg` is also installed inside this container by the `Dockerfile`.
- The `postgresql-client` package, however, is only installed inside the container.

## Starting and Stopping the Backup Process

### What to Do Beforehand
1. Place `python.py`, `Dockerfile`, `entrypoint.sh`, `cronjob`, and `docker-compose.yml` in your project directory.
2. Set the environment variables in the `env-file`, protect this file, and store it in a secure location outside the project directory.

### How to Start the Process
1. Navigate to your project directory:
```bash
cd path/to/your/project/directory
```
2. Build the Docker image:
```bash
docker build -t backup-container .
```
3. Start the process with Docker Compose:
```bash
docker-compose up -d
```
4. Add `cronjob` to the crontab to schedule the backups:
```bash
crontab -l > mycron
cat cronjob >> mycron
crontab mycron
rm mycron
```

### How to Stop the Process
1. Navigate to your project directory:
```bash
cd path/to/your/project/directory
```
2. Stop the process:
```bash
docker-compose down
```
3. Remove `cronjob` from the crontab:
```bash
crontab -l > mycron
grep -v "cron job pattern" mycron > mycron_new
crontab mycron_new
rm mycron mycron_new

# Replace "cron job pattern" with the contents of the cronjob file in string format
```

### When to Restart the Process
The process should be stopped and restarted when any of the project files (including `env-file`) are changed, in order to avoid running an outdated container version.

## Other Variables Used
- `/path/to/env-file`
- `GPG_PUBLIC_KEY`

### Where `/path/to/env-file` is Used
This variable is used in the `cronjob` and `docker-compose.yml` files, and needs to be replaced with the actual location of the `env-file`.

### How to Handle the `GPG_PUBLIC_KEY` Variable
1. [Generate a GPG key.](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key?platform=linux#generating-a-gpg-key)
2. Open the `env-file` and add the GPG public key.

### The Importance of the GPG Public Key
This key is an essential part of this project, since its purpose is to encrypt the backup files.