![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# btc_light

**btc_light** is a simplified Bitcoin-like blockchain implementation in Python, developed for educational purposes.

## Features

- **Blockchain Ledger**
  - Block creation with index, transactions, timestamp, previous hash, nonce, and current hash.
  - Genesis block initialization.
  - Proof of Work (PoW) mining with adjustable difficulty.

- **Transactions**
  - Public-private key cryptography for secure transaction signing and verification.
  - Transaction signing ensures authenticity and integrity.

- **Mining and Consensus**
  - Mining logic to solve PoW puzzles and add new blocks.
  - Static block rewards for miners.

- **Wallets**
  - Key pair generation and address creation.
  - Balance inquiry and transaction creation via a Command-Line Interface (CLI).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MaxAurelius/btc_light.git
   cd btc_light
   ```

2. **Set Up Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Quick tests

- **test.sh**

  Executes a sequence of CLI commands to create wallets, mine blocks, send transactions, and check balances.

  ```bash
  ./test.sh
  ```

- **clean.sh**

  Cleans up the blockchain and wallet data by removing JSON files.

  ```bash
  ./clean.sh
  ```

## Usage

Interact with the blockchain using the Command-Line Interface (CLI) or provided scripts.

### Command-Line Interface (CLI)

The CLI allows you to perform various operations such as creating wallets, checking balances, sending transactions, and mining blocks.

#### Available Commands

- **Create Wallet**

  Create a new wallet with a unique label.

  ```bash
  python3 -m scripts.cli create_wallet <label>
  ```

  **Example:**

  ```bash
  python3 -m scripts.cli create_wallet Alice
  ```

- **Check Balance**

  Check the balance of a specific wallet.

  ```bash
  python3 -m scripts.cli check_balance <label>
  ```

  **Example:**

  ```bash
  python3 -m scripts.cli check_balance Alice
  ```

- **Send Transaction**

  Send a specified amount from one wallet to another.

  ```bash
  python3 -m scripts.cli send_transaction <from_label> <to_label> <amount>
  ```

  **Example:**

  ```bash
  python3 -m scripts.cli send_transaction Alice Bob 20
  ```

- **Mine Block**

  Mine pending transactions and receive block rewards.

  ```bash
  python3 -m scripts.cli mine_block <miner_label>
  ```

  **Example:**

  ```bash
  python3 -m scripts.cli mine_block Alice
  ```

- **View Blockchain**

  View the latest blocks in the blockchain.

  ```bash
  python3 -m scripts.cli view_chain [--num_blocks <number>]
  ```

  **Example:**

  ```bash
  python3 -m scripts.cli view_chain --num_blocks 10
  ```

- **Validate Blockchain**

  Verify the integrity and validity of the entire blockchain.

  ```bash
  python3 -m scripts.cli is_valid
  ```

---
