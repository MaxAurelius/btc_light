from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Dict, Tuple
from .transactions import Transaction
from .blockchain import Blockchain
import json
import os

import hashlib

class Wallet:

    """
    Represents a user's wallet, managing key pairs and addresses.

    Attributes:
        private_key (EllipticCurvePrivateKey): The user's private key.
        public_key (EllipticCurvePublicKey): The user's public key.
        address (str): The user's wallet address derived from the public key.
    """

    def __init__(self, blockhain: Blockchain, label: str) -> None:
        """
        Initializes a new wallet by assigning public, private keys and generating an address.
        """
        self.label = label
        self.blockchain = blockhain
        self.private_key, self.public_key, self.address = self.load_or_create_wallet()

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
        

    def get_address(self, public_key) -> str:
        """
        Derives the wallet address from the public key using SHA-256 hashing.

        Args:
            public_key (EllipticCurvePublicKey): The public key.

        Returns:
            str: The derived wallet address.
        """
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
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
    

    def load_or_create_wallet(self) -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey, str]:
        """
        Load or create a wallet from a file.

        Returns:
           Tuple (private_key, public_key, address)
        """

        wallet_file = f"wallets/{self.label}.json"
        if os.path.exists(wallet_file):
            with open(wallet_file, 'r') as f:
                data = json.load(f)
                private_key = serialization.load_pem_private_key(
                    data['private_key'].encode(),
                    password=None
                )
                public_key = private_key.public_key()
                address = data['address']
                return private_key, public_key, address
        else:
            private_key = self.generate_private_key()
            public_key = private_key.public_key()
            address = self.get_address(public_key)
            self.save_wallet(private_key, address)
            return private_key, public_key, address


    def save_wallet(self, private_key: ec.EllipticCurvePrivateKey, address: str) -> None:
        """
        Save the wallet's private key and address to a file.

        Args:
            private_key (EllipticCurvePrivateKey): The private.
            address (str): The wallet address.
        """
        
        if not os.path.exists("wallets"):
            os.makedirs("wallets")
        wallet_file = f"wallets/{self.label}.json"
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        data = {
            'private_key': pem_private_key,
            'address': address
        }
        with open(wallet_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Wallet '{self.label}' saved to '{wallet_file}'.")