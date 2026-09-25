# -*- coding: utf-8 -*-
"""Decodificacion de JWT RS256 centralizada.

Antes duplicada en LKFBaseObject.decode_jwt (que lee self.config['JWT_KEY'])
y en el patron _caller_from_jwt de contratistas/service.py (que decodifica el
header Authorization a variables locales). Ambos casos delegan aqui.
"""
import jwt

PUB_KEY_PATH = '/etc/ssl/certs/lkf_jwt_key.pub'

_pub_key_cache = None


def _read_pub_key():
    global _pub_key_cache
    if _pub_key_cache is None:
        with open(PUB_KEY_PATH, 'r') as fh:
            _pub_key_cache = fh.read()
    return _pub_key_cache


def decode_jwt_token(token_or_header):
    """Acepta 'Bearer <jwt>' o el token pelado. Devuelve {} si no viene nada.
    Propaga la excepcion de PyJWT si el token es invalido/esta expirado --
    quien llama decide si eso es un 401, un log, o seguir de largo.
    """
    if not token_or_header:
        return {}
    token = token_or_header.split(' ')[-1].strip()
    if not token:
        return {}
    return jwt.decode(token, _read_pub_key(), algorithms='RS256')
