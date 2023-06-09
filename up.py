"""Plugin's commands definition."""

import functools
import os
import random

import requests
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
)
session.request = functools.partial(session.request, timeout=60 * 5)  # type: ignore


@simplebot.hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    _getdefault(
        bot, "server", "https://0x0.st/ https://ttm.sh/ https://envs.sh/ https://x0.at/"
    )


@simplebot.command
def up(bot: DeltaBot, message: Message, replies: Replies, payload) -> None:
    """Envia cualquier archivo comentado por el cmd y name.Ej: /up Loli Ricolilla\nEsto subira el archivo con nombre a mostrar\nUtil para compartir varias veces y en un superGrupo ya q ai limites en estos"""
    payload = payload.replace('_', ' ')
    if message.text=='/up' or message.text=='/up ' or not message.filename:
        replies.add("Esto se usa para subir archivos comentando con un nombre ej:\n/up Foto de Loli\n Asi reciviras un enlace de descarga directa del archivo!",  quote=message)
        return
    if not message.chat.is_multiuser() and message.filename:
        num = os.stat(message.filename).st_size
        if num > 1024**2:
            rep = Replies(message, bot.logger)
            rep.add(text="⬆️ Subiendo...", quote=message)
            rep.send_reply_messages()
        urls = _getdefault(bot, "server").split()
        while urls:
            url = urls.pop(random.randrange(len(urls)))
            try:
                with open(message.filename, "rb") as file:
                    with session.post(url, files=dict(file=file)) as resp:
                        resp.raise_for_status()
                        name = os.path.basename(message.filename)
                        size = _sizeof_fmt(num)
                        replies.add(
                            text=f"### ☁️`Archivo subido`☁️\n\n**😪-Nombre:** {payload}\n**📦-Archivo:** `{name}`\n**⚖️-Peso:** {size}\n**🔗-Enlace:** [**`Descargar`**](mailto:?body={resp.text.strip()})"
                        )
                        return
            except requests.RequestException as ex:
                bot.logger.exception(ex)
        replies.add(text="😨 Sorry hubo un error!!️ ", quote=message)


def _getdefault(bot: DeltaBot, key: str, value: str = None) -> str:
    val = bot.get(key, scope=__name__)
    if val is None and value is not None:
        bot.set(key, value, scope=__name__)
        val = value
    return val


def _sizeof_fmt(num: float) -> str:
    suffix = "B"
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)  # noqa
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)  # noqa
