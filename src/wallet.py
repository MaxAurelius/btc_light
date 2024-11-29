from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Dict
from .transactions import Transaction
from .blockchain import Blockchain

import hashlib

class Wallet:

    """
    Represents a user's wallet, managing key pairs and addresses.

    Attributes:
        private_key (EllipticCurvePrivateKey): The user's private key.
        public_key (EllipticCurvePublicKey): The user's public key.
        address (str): The user's wallet address derived from the public key.
    """

    def __init__(self, blockhain: Blockchain) -> None:
        """
        Initializes a new wallet by assigning public, private keys and generating an address.
        """
        self.private_key = self.generate_private_key()
        self.public_key = self.private_key.public_key()
        self.address = self.get_address()
        self.blockchain = blockhain

    def generate_private_key(self) -> ec.EllipticCurvePrivateKey:
        """
        Generates a new ECDSA private key.

        Returns:
            EllipticCurvePrivateKey: The generated private key.
        """
        return ec.generate_private_key(ec.SECP256K1())
    
    def get_pem_public_key(self) -> str:
        """
        Serializes the public key to PEM format.

        Returns:
            str: the PEM-formatted public key.
        """
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode()
        

    def get_address(self) -> str:
        """
        Derives the wallet addres from the public key using SHA-256 hashing.

        Returns:
            str: Derived wallet address.
        """
        pem_public_key = self.get_pem_public_key()
        sha256 = hashlib.sha256()
        sha256.update(pem_public_key.encode())
        return sha256.hexdigest()


    def sign_transaction(self, transaction: Transaction) -> None:
        """
        Sing a transaction using wallet's private key.

        Args:
            transaction (Transaction): The transaction to sign.
        """
        transaction.sign_transaction(self.private_key)

    def to_dict(self) -> Dict[str, any]:
        """
        TESTING ONLY
        Serializes the wallet into a dictionary.

        Returns:
            Dict[str, any]: The serialized wallet
        """
        return {
            'public_key': self.get_pem_public_key(),
            'address': self.address
        }
    
    def get_balance(self) -> float:
        """
        Retrieves the current balance of the wallet.

        Returns:
            float: The wallet's balance.
        """
        return self.blockchain.get_balance(self.address)