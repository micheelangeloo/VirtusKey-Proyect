import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def crear_llave(contrasena: str, sal: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sal,
        iterations=100000,
    )
    return kdf.derive(contrasena.encode())


def encriptar(texto: bytes, contrasena: str) -> bytes:
    sal = os.urandom(16)
    llave = crear_llave(contrasena, sal)

    motor_aes = AESGCM(llave)
    numero_unico = os.urandom(12)

    texto_oculto = motor_aes.encrypt(numero_unico, texto, None)

    return sal + numero_unico + texto_oculto


def desencriptar(paquete: bytes, contrasena: str) -> bytes:
    sal = paquete[:16]
    numero_unico = paquete[16:28]
    texto_oculto = paquete[28:]

    llave = crear_llave(contrasena, sal)
    motor_aes = AESGCM(llave)
    return motor_aes.decrypt(numero_unico, texto_oculto, None)