# tests/test_blockchain.py

from src.wallet import Wallet
from src.transactions import Transaction
from src.block import Block

from datetime import datetime, timezone
import pytest

def test_block_creation_and_hash():
    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create a transaction
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=20.0
    )

    # Sign the transaction
    sender_wallet.sign_transaction(tx)

    # Verify the transaction
    assert tx.verify_signature() == True, "Transaction signature should be valid."

    # Create a block
    block = Block(
        index=1,
        transactions=[tx],
        timestamp=datetime.now(timezone.utc).isoformat(),
        prev_hash='0'
    )

    # Calculate hash
    calculated_hash = block.calculate_hash()

    # Ensure the hash is a valid SHA-256 hex string (64 characters)
    assert isinstance(calculated_hash, str), "Hash should be a string."
    assert len(calculated_hash) == 64, "Hash should be 64 hexadecimal characters."

def test_proof_of_work():
    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create a transaction
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=15.0
    )

    # Sign the transaction
    sender_wallet.sign_transaction(tx)

    # Verify the transaction
    assert tx.verify_signature() == True, "Transaction signature should be valid."

    # Create a block
    block = Block(
        index=1,
        transactions=[tx],
        timestamp=datetime.now(timezone.utc).isoformat(),
        prev_hash='0'
    )

    # Mine the block with difficulty 2
    difficulty = 2
    block.mine_block(difficulty)

    # Check if the hash meets the difficulty
    assert block.hash.startswith('0' * difficulty), f"Hash should start with {'0' * difficulty}."

def test_block_linking():
    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create and mine the genesis block
    genesis_tx = Transaction(
        sender_address="0",
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=50.0
    )
    genesis_block = Block(
        index=0,
        transactions=[genesis_tx],
        timestamp=datetime.now(timezone.utc).isoformat(),
        prev_hash='0'
    )
    genesis_block.mine_block(difficulty=2)

    # Create a new transaction
    tx = Transaction(
        sender_address=recipient_wallet.get_pem_public_key(),
        recipient_address=sender_wallet.get_pem_public_key(),
        amount=10.0
    )
    # For simplicity, assuming sender has enough balance and is authorized
    # Normally, you'd verify balance and signatures here
    # Since recipient is '0', they don't need to sign in this simplified test

    # Create a new block referencing the genesis block's hash
    new_block = Block(
        index=1,
        transactions=[tx],
        timestamp=datetime.now(timezone.utc).isoformat(),
        prev_hash=genesis_block.hash
    )
    new_block.mine_block(difficulty=2)

    # Verify the linking
    assert new_block.prev_hash == genesis_block.hash, "New block's previous hash should match genesis block's hash."
