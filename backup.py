import os
import subprocess
from datetime import datetime, timezone

# Environment variables

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "7"))
BACKUP_DIR = "/mnt/backups"

# Create backup

def create_backup():
    timestamp = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d_%H%M")
    backup_filename = f"bica-backup-{timestamp}.tar.gz"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    backup_command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} {DB_NAME} | gzip > {backup_path}"
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    try:
        subprocess.run(backup_command, shell=True, check=True, env=env)
        print(f"Backup created successfully: {backup_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")

# Remove old backups

def remove_old_backups():
    now_str = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d_%H%M")
    now_tuple = datetime.strptime(now_str, "%Y-%m-%d_%H%M")

    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("bica-backup-") and filename.endswith(".tar.gz"):
            file_time_str = filename[len("bica-backup-"):-len(".tar.gz")]
            file_time_tuple = datetime.strptime(file_time_str, "%Y-%m-%d_%H%M")
            file_path = os.path.join(BACKUP_DIR, filename)

            if (now_tuple - file_time_tuple).days >= RETENTION_DAYS:
                os.remove(file_path)
                print(f"Removed old backup: {file_path}")

# Main function

def main():
    create_backup()
    if datetime.now().astimezone(timezone.utc).hour == 3:
        remove_old_backups()

# Call main function if script is run directly

if __name__ == "__main__":
    main()