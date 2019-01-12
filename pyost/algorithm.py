from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type
import ed25519
import ecdsa

from pyost.rpc.pb import rpc_pb2 as pb
from pyost import signature


def get_algorithm_by_id(id: int) -> Type[Algorithm]:
    """Factory that returns an `Algorithm`'s class type from its id.
    The `id` is used internally by the blockchain's node.

    Args:
        id: The id of the `Algorithm`.

    Returns:
        The corresponding `Algorithm`'s class type.

    Raises:
        ValueError: If no `Algorithm` corresponds to the `id`.
    """
    if id == Ed25519.ID:
        return Ed25519
    elif id == Secp256k1.ID:
        return Secp256k1
    else:
        raise ValueError(f'no algorithm correspond to id {id}')


def get_algorithm_by_name(name: str) -> Type[Algorithm]:
    """Factory that returns an `Algorithm`'s class type from its name.
    This can be used with arguments from the command line.

    Args:
        name: The name of the `Algorithm`.

    Returns:
        The corresponding `Algorithm`'s class type.

    Raises:
        ValueError: If no `Algorithm` corresponds to the `name`.
    """
    if name == Ed25519.NAME:
        return Ed25519
    elif name == Secp256k1.NAME:
        return Secp256k1
    else:
        raise ValueError(f'no algorithm correspond to name {name}')


class Algorithm(ABC):
    """Super class of Algorithm."""
    ID = pb.Signature.UNKNOWN  #: The id of the Algorithm as used internally by the blockchain's nodes.
    NAME = 'UNKNOWN'  #: The name of the Algorithm, for display purpose.

    @classmethod
    @abstractmethod
    def create_key_pair(cls) -> signature.KeyPair:
        """Creates a `KeyPair` object with this `Algorithm`.

        Returns:
            A `KeyPair` object.
        """
        pass

    @classmethod
    @abstractmethod
    def __int__(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def __str__(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        """Signs a message with a secret key.

        Args:
            message: The binary message to sign.
            seckey: The binary representation of the secret key.

        Returns:
            A binary signature.
        """
        pass

    @classmethod
    @abstractmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        """Verifies if a message has been signed by the private key corresponding to a public key.

        Args:
            message: The binary message to verify.
            pubkey: The public key that corresponds to the private key that signed the message.
            sig: The signature that was generated with the message and the private key.

        Returns:
            ``True`` if the sig was generated from the message and the public key's corresponding private key.
        """
        pass

    @classmethod
    @abstractmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        """Gets the public key corresponding to a private key.

        Args:
            seckey: The private key.

        Returns:
            The corresponding public key.
        """
        pass

    @classmethod
    @abstractmethod
    def gen_seckey(cls) -> bytes:
        """Generates a secret key.

        Returns:
            A binary representation of the secret key.
        """
        pass


class Secp256k1(Algorithm):
    """Contains methods for the Secp256k1 algorithm."""
    ID = pb.Signature.SECP256K1  #: The id of the Algorithm as used internally by the blockchain's nodes.
    NAME = 'secp256k1'  #: The name of the Algorithm, for display purpose.

    @classmethod
    def create_key_pair(cls) -> signature.KeyPair:
        """Creates a `KeyPair` object with this `Algorithm`.

        Returns:
            A `KeyPair` object.
        """
        return signature.KeyPair(Secp256k1)

    @classmethod
    def __int__(cls) -> int:
        return Secp256k1.ID

    @classmethod
    def __str__(cls) -> str:
        return Secp256k1.NAME

    @classmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        """Signs a message with a secret key.

        Args:
            message: The binary message to sign.
            seckey: The binary representation of the secret key.

        Returns:
            A binary signature.
        """
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        return sk.sign(message)

    @classmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        """Verifies if a message has been signed by the private key corresponding to a public key.

        Args:
            message: The binary message to verify.
            pubkey: The public key that corresponds to the private key that signed the message.
            sig: The signature that was generated with the message and the private key.

        Returns:
            ``True`` if the sig was generated from the message and the public key's corresponding private key.
        """
        vk = ecdsa.VerifyingKey.from_string(pubkey, ecdsa.SECP256k1)
        try:
            vk.verify(sig, message)
        except ecdsa.BadSignatureError:
            return False
        return True

    @classmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        """Gets the public key corresponding to a private key.

        Args:
            seckey: The private key.

        Returns:
            The corresponding public key.
        """
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()

    @classmethod
    def get_compressed_pubkey(cls, seckey: bytes) -> bytes:
        """Generates a compressed version of the public key corresponding to a private key.

        Args:
            seckey: The private key.

        Returns:
            The compressed public key.
        """
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        p = sk.get_verifying_key().pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), ecdsa.SECP256k1.generator.order())
        compressed = bytes(chr(2 + (p.y() & 1)), 'ascii') + x_str
        return compressed

    @classmethod
    def gen_seckey(cls) -> bytes:
        """Generates a secret key.

        Returns:
            A binary representation of the secret key.
        """
        sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
        return sk.to_string()


class Ed25519(Algorithm):
    """Contains methods for the Ed25519 algorithm."""
    ID = pb.Signature.ED25519  #: The id of the Algorithm as used internally by the blockchain's nodes.
    NAME = 'ed25519'  #: The name of the Algorithm, for display purpose.

    @classmethod
    def create_key_pair(cls) -> signature.KeyPair:
        """Creates a `KeyPair` object with this `Algorithm`.

        Returns:
            A `KeyPair` object.
        """
        return signature.KeyPair(Ed25519)

    @classmethod
    def __int__(cls) -> int:
        return Ed25519.ID

    @classmethod
    def __str__(cls) -> str:
        return Ed25519.NAME

    @classmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        """Signs a message with a secret key.

        Args:
            message: The binary message to sign.
            seckey: The binary representation of the secret key.

        Returns:
            A binary signature.
        """
        sk = ed25519.SigningKey(seckey)
        return sk.sign(message)

    @classmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        """Verifies if a message has been signed by the private key corresponding to a public key.

        Args:
            message: The binary message to verify.
            pubkey: The public key that corresponds to the private key that signed the message.
            sig: The signature that was generated with the message and the private key.

        Returns:
            ``True`` if the sig was generated from the message and the public key's corresponding private key.
        """
        vk = ed25519.VerifyingKey(pubkey)
        try:
            vk.verify(sig, message)
        except ed25519.BadSignatureError:
            return False
        return True

    @classmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        """Gets the public key corresponding to a private key.

        Args:
            seckey: The private key.

        Returns:
            The corresponding public key.
        """
        sk = ed25519.SigningKey(seckey)
        return sk.get_verifying_key().to_bytes()

    @classmethod
    def gen_seckey(cls) -> bytes:
        """Generates a secret key.

        Returns:
            A binary representation of the secret key.
        """
        sk, vk = ed25519.create_keypair()
        return sk.to_bytes()
