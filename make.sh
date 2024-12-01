#!/bin/bash

# Run the Python command
python3 -m scripts.cli create_wallet Alice
python3 -m scripts.cli create_wallet Bob
python3 -m scripts.cli mine_block Alice
python3 -m scripts.cli check_balance Alice
python3 -m scripts.cli send_transaction Alice Bob 20
python3 -m scripts.cli mine_block Alice
python3 -m scripts.cli check_balance Alice
python3 -m scripts.cli check_balance Bob
python3 -m scripts.cli view_chain
