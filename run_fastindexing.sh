#!/bin/bash
# Activate virtual environment if needed (optional)
# source /path/to/your/virtualenv/bin/activate

# Run the Python script
/usr/bin/python3 /var/indexing/fastindexing.py >> /var/log/fastindexing.log 2>&1

