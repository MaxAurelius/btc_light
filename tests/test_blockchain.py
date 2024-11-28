# tests/test_blockchain.py

import pytest
from src.wallet import Wallet
from src.transactions import Transaction
from src.blockchain import Blockchain, Block
from datetime import datetime

def test_genesis_block_creation():
    # Initialize blockchain with empty chain and mempool
    blockchain = Blockchain(
        chain=[],
        difficulty=2,
        mempool=[],
        block_reward=50.0
    )

    # Create the genesis block
    genesis_block = blockchain.create_genesis_block()

    # Assertions
    assert genesis_block.index == 0, "Genesis block index should be 0."
    assert genesis_block.prev_hash == '0', "Genesis block previous hash should be '0'."
    assert genesis_block.hash.startswith('0' * blockchain.difficulty), "Genesis block hash does not meet difficulty."
    assert len(blockchain.chain) == 1, "Blockchain should contain only the genesis block."

def test_add_new_block():
    # Initialize blockchain and create genesis block
    blockchain = Blockchain(
        chain=[],
        difficulty=2,
        mempool=[],
        block_reward=50.0
    )
    genesis_block = blockchain.create_genesis_block()

    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create and sign a transaction
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=20.0
    )
    sender_wallet.sign_transaction(tx)
    blockchain.add_transaction(tx)

    # Mine pending transactions
    miner_wallet = Wallet()
    blockchain.mine_pending_transactions(miner_wallet.address)

    # Assertions
    assert len(blockchain.chain) == 2, "Blockchain should contain two blocks."
    new_block = blockchain.chain[1]
    assert new_block.index == 1, "New block index should be 1."
    assert new_block.prev_hash == genesis_block.hash, "New block's previous hash should match genesis block's hash."
    assert new_block.hash.startswith('0' * blockchain.difficulty), "New block's hash does not meet difficulty."
    assert len(new_block.transactions) == 2, "New block should contain two transactions (original and reward)."

def test_chain_validation():
    # Initialize blockchain and create genesis block
    blockchain = Blockchain(
        chain=[],
        difficulty=2,
        mempool=[],
        block_reward=50.0
    )
    blockchain.create_genesis_block()

    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create and sign a transaction
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=30.0
    )
    sender_wallet.sign_transaction(tx)
    blockchain.add_transaction(tx)

    # Mine pending transactions
    miner_wallet = Wallet()
    blockchain.mine_pending_transactions(miner_wallet.address)

    # Validate the chain
    assert blockchain.is_chain_valid() == True, "Blockchain should be valid."

    # Tamper with the blockchain by altering a transaction
    blockchain.chain[1].transactions[0].amount = 1000.0
    blockchain.chain[1].hash = blockchain.chain[1].calculate_hash()

    # Validate the chain again
    assert blockchain.is_chain_valid() == False, "Blockchain should be invalid after tampering."
