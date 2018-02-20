#!/bin/bash
# Order of execution of python scripts.
python3.5 create_cryptocurrencies_list.py
python3.5 scrape.py
python3.5 split.py
python3.5 prepare.py