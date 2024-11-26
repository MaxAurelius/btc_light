from typing import Optional, Dict
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.exceptions import InvalidSignature
import json

class Transaction:
    """
    Represents a transaction within the blockchain.

    Attributes:
        sender_address (str): The address of the sender.
        recipient_address (str): The address of the recipient.
        amount (float): The amount of cryptocurrency being transferred.
        signature (Optional[bytes]): The digital signature verifying the transaction.
    """

    def __init__(
            self,
            sender_address:str,
            receipient_address:str,
            amount:float,
            signature: Optional[bytes] = None,
            ) -> None:
        
        self.sender_address: str = sender_address
        self.receipient_address: str = receipient_address
        self.amount: float = amount
        self.signature: Optional[bytes] = signature

    def to_dict(self) -> Dict[str, any]:
        """
        Serializes the transaction into a dictionary.

        Returns:
            Dict[str, any]: The serialized transaction
        """
        return {
            'sender_address': self.sender_address,
            'receipient_address': self.receipient_address,
            'amount': self.amount
        }
    
    def sign_transaction(self, private_key: bytes) -> None:
        """
        Signs the transaction using the sender's private key.

        Args:
            private_key (bytes): The sender's private key for signing the transaction.
        """
        pass  # TODO

    def verify_signature(self) -> bool:
        """
        Verifies the transaction's signature to ensure its authenticity.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        pass  # TODO
