import pytest
from src.wallet import Wallet
from src.transactions import Transaction

def test_transaction_signature():
    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create a transaction
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=25.0
    )

    # Sign the transaction
    sender_wallet.sign_transaction(tx)

    # Verify the signature
    assert tx.verify_signature() == True, "Transaction signature should be valid."

def test_invalid_signature():
    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()
    malicious_wallet = Wallet()

    # Create a transaction
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=50.0
    )

    # Maliciously sign the transaction with a different private key
    malicious_wallet.sign_transaction(tx)

    # Verify the signature
    assert tx.verify_signature() == False, "Transaction signature should be invalid."

def test_missing_signature():
    # Initialize wallets
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    # Create a transaction without signing
    tx = Transaction(
        sender_address=sender_wallet.get_pem_public_key(),
        recipient_address=recipient_wallet.get_pem_public_key(),
        amount=15.0
    )

    # Verify the signature
    assert tx.verify_signature() == False, "Transaction without signature should be invalid."
