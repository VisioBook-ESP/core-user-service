"""
RSA key management for JWT signing and JWKS endpoint.
"""

import base64
import logging
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.settings import settings

logger = logging.getLogger(__name__)


def _base64url_encode(data: bytes) -> str:
    """Base64url encode bytes without padding (per RFC 7515)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _load_or_generate_private_key() -> rsa.RSAPrivateKey:
    """Load RSA private key from settings, or generate one for development."""
    if settings.rsa_private_key:
        pem_data = settings.rsa_private_key.replace("\\n", "\n").encode("utf-8")
        loaded_key = serialization.load_pem_private_key(pem_data, password=None)
        if not isinstance(loaded_key, rsa.RSAPrivateKey):
            raise TypeError("RSA_PRIVATE_KEY must be an RSA private key")
        logger.info("Loaded RSA private key from environment")
        return loaded_key

    if settings.env.lower() != "dev":
        raise RuntimeError(
            "RSA_PRIVATE_KEY environment variable is required in non-dev environments. "
            "Generate one with: openssl genrsa -out private.pem 2048"
        )

    logger.warning(
        "No RSA_PRIVATE_KEY set -- generating ephemeral key for development. "
        "DO NOT use this in production!"
    )
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


# Module-level singletons
private_key: rsa.RSAPrivateKey = _load_or_generate_private_key()
public_key: rsa.RSAPublicKey = private_key.public_key()


def get_jwks() -> dict[str, Any]:
    """Build the JWKS document from the current public key."""
    pub_numbers = public_key.public_numbers()

    n_bytes = pub_numbers.n.to_bytes((pub_numbers.n.bit_length() + 7) // 8, byteorder="big")
    e_bytes = pub_numbers.e.to_bytes((pub_numbers.e.bit_length() + 7) // 8, byteorder="big")

    return {
        "keys": [
            {
                "kty": "RSA",
                "kid": settings.jwt_kid,
                "use": "sig",
                "alg": "RS256",
                "n": _base64url_encode(n_bytes),
                "e": _base64url_encode(e_bytes),
            }
        ]
    }
