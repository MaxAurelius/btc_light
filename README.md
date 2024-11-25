# btc_light

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**btc_light** is a simplified Bitcoin-like blockchain implementation in Python, developed for educational purposes. This project demystifies the core concepts of blockchain technology by building a minimal, functional version from scratch.

## Features

- **Blockchain Ledger**
  - Block creation with index, transactions, timestamp, previous hash, nonce, and current hash.
  - Genesis block initialization.
  - Proof of Work (PoW) mining with adjustable difficulty.
  
- **Transactions**
  - Public-private key cryptography for secure transaction signing and verification.
  - Unspent Transaction Output (UTXO) model for tracking balances.
  
- **Mining and Consensus**
  - Mining logic to solve PoW puzzles and add new blocks.
  - Static block rewards for miners.
  
- **Wallets**
  - Key pair generation and address creation.
  - Balance inquiry and transaction creation via a Command-Line Interface (CLI).

## Project Structure

```
btc_light/
│
├── btc_light/                # Main package
│   ├── __init__.py
│   ├── blockchain.py         # Blockchain and block classes
│   ├── transactions.py       # Transactions and UTXO management
│   ├── mining.py             # Mining logic
│   ├── network.py            # Networking and P2P communication
│   ├── wallet.py             # Wallet and cryptographic key management
│   └── utils.py              # Utility functions
│
├── tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── test_blockchain.py
│   ├── test_transactions.py
│   └── ...
│
├── scripts/                  # Scripts for running the application
│   └── main.py               # CLI for user interaction
│
├── .gitignore                # Git ignore file
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── LICENSE                   # License information
```

## Getting Started

### Prerequisites

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Install Git](https://git-scm.com/downloads)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/btc_light.git
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

## Usage

### Running the CLI

Interact with the blockchain using the Command-Line Interface.

1. **Navigate to the Scripts Directory**

   ```bash
   cd scripts
   ```

2. **Run the Main Script**

   ```bash
   python main.py
   ```

### Available Commands

- **View Blockchain**

  Display all blocks in the blockchain.

  ```bash
  python main.py view_chain
  ```

- **Check Balance**

  View the balance of a specific wallet address.

  ```bash
  python main.py check_balance --address <your_address>
  ```

- **Send Transaction**

  Create and broadcast a transaction from one address to another.

  ```bash
  python main.py send_transaction --sender <sender_address> --recipient <recipient_address> --amount <amount>
  ```

- **Mine Block**

  Initiate mining to add pending transactions to the blockchain and receive rewards.

  ```bash
  python main.py mine_block --miner <miner_address>
  ```

- **Validate Blockchain**

  Verify the integrity and validity of the entire blockchain.

  ```bash
  python main.py is_valid
  ```