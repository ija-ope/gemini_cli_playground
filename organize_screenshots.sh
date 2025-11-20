#!/bin/bash
find /Users/mac/Desktop -name "Screenshot*.png" -mtime +1 -exec mv {} /Users/mac/Documents/old\ files/ \;
