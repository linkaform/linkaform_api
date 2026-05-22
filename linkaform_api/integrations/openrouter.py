# -*- coding: utf-8 -*-
"""
linkaform_api/integrations/openrouter.py

Cliente OpenRouter integrado en linkaform_api.
Se inicializa automáticamente en LKF_Base._set_connections()
si el usuario tiene OPENROUTER_API_KEY en su account_settings.py.

Uso básico desde cualquier módulo de lkf_addons:

    # Si el usuario configuró OPENROUTER_API_KEY, self.ai estará disponible
    if self.ai:
        result = self.ai.ocr_id("https://s3.../ine.jpg")
        result = self.ai.chat("¿Cuántos registros hay del form 345?")
        result = self.ai.chat("resume esto", image_url="https://...")
"""

import json
import base64
import requests
from pathlib import Path
from ..lkf_object import LKFBaseObject


# Modelo por default — puede sobreescribirse en account_settings con OPENROUTER_MODEL
DEFAULT_MODEL = 'google/gemini-2.5-flash'
# DEFAULT_MODEL = 'google/gemini-2.5-flash-light'
# DEFAULT_MODEL = 'anthropic/claude-haiku-4.5' Mejor modelo mas caro

OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'


class OpenRouter(LKFBaseObject):
    """
    Cliente OpenRouter para LinkaForm.

    Expone métodos de alto nivel listos para usar en lkf_addons:
        - chat()       → conversación general con o sin imagen
        - ocr_id()     → extrae datos de una identificación
        - ocr()        → OCR genérico para cualquier imagen

    Y métodos de bajo nivel para casos custom:
        - completion() → llamada directa a la API con messages completos
    """

    def __init__(self, config: dict):
        """
        Args:
            config: settings.config de LinkaForm.
                    Requiere: OPENROUTER_API_KEY
                    Opcional: OPENROUTER_MODEL, ACCOUNT_ID, USER_ID
        """
        self.api_key   = config.get('OPENROUTER_API_KEY', '')
        self.model     = config.get('OPENROUTER_MODEL', DEFAULT_MODEL)
        self.account_id = config.get('ACCOUNT_ID', '')
        self.user_id    = config.get('USER_ID', '')

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY no está configurada en account_settings.py"
            )

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type':  'application/json',
            'HTTP-Referer':  'https://web.clave10.com',
            'X-Title':       'Clave10',
        }

    # ──────────────────────────────────────────────────────────
    # MÉTODOS PÚBLICOS DE ALTO NIVEL
    # ──────────────────────────────────────────────────────────

    def chat(self, prompt: str, image_url = None,
             system: str = None, model: str = None,
             max_tokens: int = 1000, temperature: float = 0) -> str:
        """
        Conversación general con el LLM, con o sin imagen.

        Args:
            prompt:      El mensaje del usuario.
            image_url:   URL o ruta local de imagen (opcional).
            system:      System prompt custom (opcional).
            model:       Modelo a usar (opcional, usa el default del config).
            max_tokens:  Máximo de tokens en la respuesta.
            temperature: 0 = determinista, 1 = creativo.

        Returns:
            str con la respuesta del modelo.

        Ejemplo:
            texto = self.ai.chat("Resume este documento", image_url="https://...")
            texto = self.ai.chat("¿Qué es LinkaForm?")
        """
        messages = []

        if system:
            messages.append({'role': 'system', 'content': system})

        user_content = self._build_user_content(prompt, image_url)
        messages.append({'role': 'user', 'content': user_content})

        data = self.post(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return data

    def ocr_id(self, image_source: list, model: str = 'google/gemini-2.5-flash-lite', name: str=None) -> dict:
        """
        Extrae datos de una identificación (INE, pasaporte, licencia, etc.)
        y los retorna como dict.

        Args:
            image_source: URL remota o ruta local de la imagen.
            model:        Modelo a usar (opcional).

        Returns:
            dict con los campos extraídos. Ejemplo:
            {
                "nombre": "Juan",
                "apellido_paterno": "Pérez",
                "curp": "PEGJ850315HDFRMN01",
                "fecha_nacimiento": "1985-03-15",
                "tipo_documento": "INE",
                ...
            }

        Ejemplo:
            datos = self.ai.ocr_id("https://s3.amazonaws.com/.../ine.jpg")
            datos = self.ai.ocr_id("/tmp/identificacion.png")
        """
        self.headers['X-Title'] = 'Clave10: OCR ID'
        system = (
            "Eres un OCR especializado en identificaciones. "
            "Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, "
            "sin bloques de código. Usa null para campos ilegibles."
        )
        prompt = "Valida que sea una identificación sea real.\n"
        if name:
            prompt += f"""Valida que la identifcacion pertenezca a {name}. IMPORTANTE, si la identificación
             no pertenece a {name}, regresa un JSON status: La identificacion no pertences a {name},
             status_code: 406"""

        prompt += """Extrae todos los datos de esta identificación y devuélvelos como JSON.

            Incluye los campos que encuentres, y siempre contesta en este formato:
            - nombre, 
            - apellido_paterno,
            - apellido_materno
            - fecha_nacimiento (formato YYYY-MM-DD si es posible)
            - sexo
            - curp, 
            - rfc, 
            - direccion: {
                calle,    
                colonia, 
                municipio, 
                estado, 
                cp
            }
            - fecha_vigencia
            - fecha_expedicion
            - numero_documento
            - nacionalidad
            - tipo_documento (INE, pasaporte, licencia, etc.)
            - status_vigenica (indica con un vigente si fecha de vigencia esta vigente )
            Responde SOLO con el JSON, sin explicaciones."""
        
        raw = self.chat(
            prompt=prompt,
            image_url=image_source,
            system=system,
            model=model,
            max_tokens=600,
            temperature=0,
        )
        return self._parse_json(raw)

    def ocr(self, image_source: list, fields: list = None,
            extra_instructions: str = None, model: str = 'google/gemini-2.5-flash-lite') -> dict:
        """
        OCR genérico para cualquier imagen.

        Args:
            image_source:       URL remota o ruta local.
            fields:             Lista de campos a extraer (opcional).
                                Si no se especifica, extrae todo lo visible.
            extra_instructions: Instrucciones adicionales al modelo (opcional).
            model:              Modelo a usar (opcional).

        Returns:
            dict con los campos extraídos.

        Ejemplo:
            # Extraer campos específicos de una factura
            datos = self.ai.ocr(
                "https://.../factura.jpg",
                fields=["numero_factura", "total", "fecha", "rfc_emisor"],
            )
        """
        self.headers['X-Title'] = 'Clave10: OCR'

        system = (
            "Eres un OCR. Analiza la imagen y extrae los campos solicitados. "
            "Responde ÚNICAMENTE con JSON válido, sin texto adicional. "
            "Usa null si un campo no está visible."
        )

        if fields:
            fields_str = ", ".join(fields)
            prompt = f"Extrae los siguientes campos: {fields_str}."
        else:
            prompt = "Extrae todos los campos de texto visibles en la imagen."

        if extra_instructions:
            prompt += f" {extra_instructions}"

        prompt += " Responde SOLO el JSON."

        raw = self.chat(
            prompt=prompt,
            image_url=image_source,
            system=system,
            model=model,
            max_tokens=800,
            temperature=0,
        )
        return self._parse_json(raw)

    def ocr_general(self, image_source:list, system: str, prompt: str, 
            model: str = None, agent: str = 'Clave10', max_tokens: int = 600):
        """
        Extrae datos de una identificación (INE, pasaporte, licencia, etc.)
        y los retorna como dict.

        Args:
            image_source: URL remota o ruta local de la imagen.
            model:        Modelo a usar (opcional).

        Returns:
            dict con los campos extraídos. Ejemplo:
            {
                "nombre": "Juan",
                "apellido_paterno": "Pérez",
                "curp": "PEGJ850315HDFRMN01",
                "fecha_nacimiento": "1985-03-15",
                "tipo_documento": "INE",
                ...
            }

        Ejemplo:
            datos = self.ai.ocr_id("https://s3.amazonaws.com/.../ine.jpg")
            datos = self.ai.ocr_id("/tmp/identificacion.png")
        """
        self.headers['X-Title'] = agent
        # system = (
        #     "Eres un OCR especializado en Paquetes de entrega. "
        #     "Eres un guarida de segurida o recepcionista de un gran corportativo que recive"
        #     "Muchos paquetes, de paqueterias o de comida"
        # )
        # prompt = (
        #     "Lee la informacion de la etiqueta proporcionada. Regresa en un JSON los datos de:"
        #     "- remitente: 'str' Es el remitente, el orgien del paquete, el quien envia"
        #     "- telefono_remitente: 'str' telefono quien envia"
        #     "- direccion_remiente: es la direccion de quien envia"
        #     "- receptor: 'str' Es para quien va el paquete."
        #     "- telefono_receptor: 'str' telefono quien recibe    "
        #     "- email_receptor: 'str' email quien recibe    "
        #     "- paqueteria: 'str' Empresa quien envia el paquete, ej FedEx, USPS, UPS, UberEats"
        #     "- no_guia: 'str' Es el numero de guia o numero de orden o numero de paquete"
        #     "- telefono_receptor: 'str' Telefono de quien recibe"
        #     "- contenido: 'str' contenido"
        #     "- tipo_paquete: 'str' El tipo de paquete, caja, sobre, alimentos, folores"
        #     )

        raw = self.chat(
            prompt=prompt,
            image_url=image_source,
            system=system,
            model=model,
            max_tokens=max_tokens,
            temperature=0,
        )
        return self._parse_json(raw)

    # ──────────────────────────────────────────────────────────
    # MÉTODO DE BAJO NIVEL
    # ──────────────────────────────────────────────────────────

    def post(self, messages: list, model: str = None,
                   max_tokens: int = 1000, temperature: float = 0,
                   tools: list = None) -> dict:
        """
        Llamada directa a la API de OpenRouter.
        Útil para casos avanzados donde necesitas controlar
        el historial de mensajes completo o usar tools.

        Args:
            messages:    Lista completa de mensajes (system/user/assistant/tool).
            model:       Modelo a usar (opcional, usa el default del config).
            max_tokens:  Máximo de tokens en la respuesta.
            temperature: 0 = determinista, 1 = creativo.
            tools:       Lista de tool definitions para tool calling (opcional).

        Returns:
            dict completo del response de OpenRouter (choices, usage, etc.)

        Ejemplo:
            data = self.ai.completion(
                messages=[
                    {"role": "system", "content": "Eres un asistente."},
                    {"role": "user",   "content": "Hola"},
                ],
                max_tokens=200,
            )
            texto = data['choices'][0]['message']['content']
            tokens = data['usage']['prompt_tokens']
        """

        self.headers['X-Title'] = 'Clave10: Direct'

        payload = {
            'model':       model or self.model,
            'messages':    messages,
            'max_tokens':  max_tokens,
            'temperature': temperature,
        }
        if tools:
            payload['tools'] = tools
        resp = requests.post(
            OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"OpenRouter [{resp.status_code}]: {resp.text}"
            )

        return resp.json()

    # ──────────────────────────────────────────────────────────
    # HELPERS PRIVADOS
    # ──────────────────────────────────────────────────────────

    def _build_image_url(self, image_source: str) -> str:
        """
        Prepara la URL de la imagen para el payload.
        - URL remota  → la devuelve tal cual
        - Archivo local → convierte a base64
        """
        if image_source.startswith('http://') or image_source.startswith('https://'):
            return image_source

        # Archivo local → base64
        ext = Path(image_source).suffix.lower()
        media_types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png',  '.gif':  'image/gif',
            '.webp': 'image/webp',
        }
        media_type = media_types.get(ext, 'image/jpeg')
        with open(image_source, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        return f'data:{media_type};base64,{b64}'

    def _build_user_content(self, prompt: str, image_url=None):
        """
        Construye el content del mensaje user.
 
        - Sin imagen        → string simple
        - Una imagen (str)  → lista [image, text]
        - Varias imágenes   → lista [image1, image2, ..., text]
 
        Args:
            prompt:    Texto del mensaje.
            image_url: str, list o None.
        """
        if not image_url:
            return prompt
 
        # Normalizar siempre a lista
        if isinstance(image_url, str):
            images = [image_url]
        else:
            images = list(image_url)
 
        # Construir content: primero todas las imágenes, luego el texto
        content = [
            {
                'type':      'image_url',
                'image_url': {'url': self._build_image_url(img)},
            }
            for img in images
        ]
        content.append({'type': 'text', 'text': prompt})
 
        return content


    def _parse_json(self, raw_text: str) -> dict:
        """
        Parsea la respuesta del modelo como JSON.
        Limpia bloques de código markdown si los hay.
        Detecta respuestas truncadas por límite de tokens.
        """
        res = ""
        if raw_text.get('choices'):
            if isinstance(raw_text['choices'], list) and len(raw_text['choices']) > 0:
                choice = raw_text['choices'][0]

                # ── Detectar truncamiento ANTES de parsear ────────────
                finish_reason = choice.get('finish_reason')
                native_finish = choice.get('native_finish_reason')
                if finish_reason == 'length' or native_finish == 'MAX_TOKENS':
                    raise self.LKFException({
                        'msg':(
                        f"Respuesta truncada por límite de tokens (finish_reason='{finish_reason}'). "
                        f"Tokens usados: {raw_text.get('usage', {}).get('completion_tokens')}. "
                        f"Aumenta max_tokens en la llamada al modelo."),
                        'status_code': 422}
                    )

                if choice.get('message', {}).get('content'):
                    res = choice['message']['content'].strip()

        text = res.strip()

        # ── Limpiar bloques markdown ```json ... ``` ──────────────────
        if text.startswith('```'):
            lines = text.split('\n')
            # Remover primera línea (```json) y última (```)
            text = '\n'.join(lines[1:-1]).strip()

        # ── Parsear JSON ──────────────────────────────────────────────
        try:
            parsed = json.loads(text)
            raw_text['choices'][0]['message']['content'] = parsed
            return raw_text
        except json.JSONDecodeError as e:
            raise ValueError(
                f"El modelo no devolvió JSON válido: {e}\n"
                f"Fragmento problemático: ...{text[max(0, e.pos-50):e.pos+50]}..."
            )