#!/bin/bash

# Remove all JSON files from the wallets directory
rm -f /home/imperiumnova/btc_light/wallets/*.json

# Remove blockchain.json from the root directory
rm -f /home/imperiumnova/btc_light/blockchain.json

echo "Cleanup completed."