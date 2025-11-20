# Screenshot Archiver

This project contains a shell script to automatically archive screenshots on a macOS system.

## How it works

The `organize_screenshots.sh` script finds all screenshots on the Desktop that are more than a day old and moves them to a specified directory (`~/Documents/old files/` by default).

A CRON job is set up to run this script daily at midnight, ensuring that screenshots are regularly archived.

## Usage

1.  Place the `organize_screenshots.sh` script in a directory on your system.
2.  Make sure the script is executable (`chmod +x organize_screenshots.sh`).
3.  Add a CRON job to schedule the script's execution. For example, to run it daily at midnight, add the following line to your crontab:

    `0 0 * * * /bin/bash /path/to/organize_screenshots.sh`
