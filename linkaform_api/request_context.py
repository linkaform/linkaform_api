# -*- coding: utf-8 -*-
"""Identidad de usuario aislada por-request via contextvars.

Sanic despacha cada conexion/request en su propio asyncio.Task, y
contextvars.ContextVar se copia automaticamente por Task -- por eso esto es
seguro para aislar el JWT/usuario de cada request aunque varias corran
"concurrentemente" sobre el mismo singleton de servicio (LKF_Base) del
proceso. A diferencia de mutar self.user/self.config directamente (lo que
hacia @reload_user), nada de esto toca self.config, que es settings.config:
un dict compartido por TODAS las instancias de TODOS los modulos del
proceso.
"""
import contextvars

# default=None (no {}) a proposito: None significa "nadie seteo contexto
# todavia" (bootstrap del singleton al importar routes.py, o script
# standalone con sys_argv). {} seria indistinguible de "el middleware corrio
# y el JWT vino vacio/invalido".
_current_user = contextvars.ContextVar('lkf_current_user', default=None)
_current_jwt_raw = contextvars.ContextVar('lkf_current_jwt_raw', default=None)


def set_current_user(user, raw_jwt=None):
    _current_user.set(user or {})
    _current_jwt_raw.set(raw_jwt)


def get_current_user():
    return _current_user.get() or {}


def get_current_jwt_raw():
    return _current_jwt_raw.get()


def has_request_context():
    return _current_user.get() is not None


def clear_current_user():
    _current_user.set(None)
    _current_jwt_raw.set(None)


def submit_with_context(executor, fn, *args, **kwargs):
    """Reemplazo de executor.submit(fn, *args, **kwargs) para
    ThreadPoolExecutor. ThreadPoolExecutor.submit() puro NO copia contextvars
    al hilo nuevo (a diferencia de loop.run_in_executor()) -- sin esto,
    cualquier self.user leido dentro del hilo caeria al default (usuario
    vacio) aunque el hilo llamador si tenga contexto de request.
    """
    ctx = contextvars.copy_context()
    return executor.submit(ctx.run, fn, *args, **kwargs)


_MISSING = object()


class JWTAwareConfig(dict):
    """settings.config, pero la key 'JWT_KEY' se resuelve contra el JWT de la
    request actual (ContextVar) cuando hay una, en vez de leer el valor
    guardado en el dict. Nunca escribe en el dict compartido -- evita la
    fuga de identidad que tenia @reload_user (que si mutaba config['JWT_KEY']
    in-place sobre este mismo dict, compartido por TODAS las instancias de
    TODOS los modulos del proceso).

    Fuera de una request Sanic (bootstrap del proceso, o un script standalone
    corriendo con sys_argv) se comporta como un dict normal: usa el valor
    real guardado, que es exactamente el que LKF_Base.__init__ escribe ahi
    a partir de sys_argv. Cualquier otra key (incluida APIKEY_JWT_KEY) se
    comporta como dict normal siempre.
    """

    def _request_jwt(self):
        if not has_request_context():
            return _MISSING
        raw = get_current_jwt_raw()
        if not raw:
            return None
        return raw.split(' ')[-1].strip()

    def __getitem__(self, key):
        if key == 'JWT_KEY':
            jwt = self._request_jwt()
            if jwt is not _MISSING:
                return jwt
        return super().__getitem__(key)

    def get(self, key, default=None):
        if key == 'JWT_KEY':
            jwt = self._request_jwt()
            if jwt is not _MISSING:
                return jwt
        return super().get(key, default)
