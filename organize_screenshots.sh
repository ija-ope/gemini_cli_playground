#!/bin/bash
find /Users/mac/Desktop /Users/mac/Downloads /Users/mac/Documents -name "Screenshot*.png" -mtime +1 -exec mv {} /Users/mac/Documents/old\ files/ \;
