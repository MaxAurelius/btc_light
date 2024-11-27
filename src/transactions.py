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
            recipient_address:str,
            amount:float,
            signature: Optional[bytes] = None,
            ) -> None:
        
        self.sender_address: str = sender_address
        self.recipient_address: str = recipient_address
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
            'recipient_address': self.recipient_address,
            'amount': self.amount
        }
    
    def sign_transaction(self, private_key: bytes) -> None:
        """
        Signs the transaction using the sender's private key.

        Args:
            private_key (bytes): The sender's private key for signing the transaction.
        """
        
        if self.sender_address is None:
            ValueError("Sender address is required to sign a transaction.")

        transaction_data = json.dumps(self.to_dict(), sort_keys=True).encode()

        try:
            signature = private_key.sign(
                transaction_data,
                ec.ECDSA(hashes.SHA256())
            )
            
            self.signature = signature
        except:
            ValueError("Unable to sign transaction.")


    def verify_signature(self) -> bool:
        """
        Verifies the transaction's signature to ensure its authenticity.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        if self.signature is None:
            print("No signature found for this transaction.")
            return False

        # Serialize the transaction data
        transaction_data = json.dumps(self.to_dict(), sort_keys=True).encode()

        try:
            # Load the sender's public key from the sender_address
            public_key = serialization.load_pem_public_key(
                self.sender_address.encode()
            )

            # Verify the signature
            public_key.verify(
                self.signature,
                transaction_data,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        
        except (InvalidSignature, ValueError) as e:
            print(f"Signature verification failed: {e}")
            return False
