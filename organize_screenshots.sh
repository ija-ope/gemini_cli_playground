#!/bin/bash
find ~/Desktop -name "Screenshot*.png" -mtime +1 -exec mv {} ~/Documents/old\ files/ \;
