"""
Проверка статуса Minecraft Bedrock/PE серверов: онлайн, версия, макс. слоты.

Установка зависимости:
    pip install mcstatus

Запуск:
    python check_servers.py

Ввод: вводи сервера в формате host:port по одному на строку.
Пустая строка — запуск проверки. Пустой список — выход.
"""

import asyncio

from mcstatus import BedrockServer

TIMEOUT = 5          # секунд на ответ одного сервера
DEFAULT_PORT = 19132

BANNER = r"""
 +--------------------------------------------+
 |      MINECRAFT BEDROCK SERVER CHECKER      |
 |                                            |
 |   by notevelin                             |
 |   github.com/notevelin                     |
 +--------------------------------------------+
"""


def parse_server(line: str) -> tuple[str, int] | None:
    """Разбирает 'host' или 'host:port'. Возвращает None, если строка некорректна."""
    line = line.strip()
    if not line:
        return None

    if ":" in line:
        host, port_str = line.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            print(f"  Некорректный порт в '{line}', пропускаю")
            return None
        if not 1 <= port <= 65535:
            print(f"  Порт вне диапазона 1-65535 в '{line}', пропускаю")
            return None
    else:
        host, port = line, DEFAULT_PORT

    host = host.strip()
    if not host:
        print(f"  Пустой адрес в '{line}', пропускаю")
        return None
    return host, port


def parse_input() -> list[tuple[str, int]]:
    print("Вводи сервера в формате host:port (например play.example.com:19133).")
    print(f"Порт можно не указывать — по умолчанию {DEFAULT_PORT}.")
    print("Пустая строка — начать проверку.\n")

    servers: list[tuple[str, int]] = []
    seen: set[tuple[str, int]] = set()
    while True:
        line = input("> ").strip()
        if not line:
            break
        parsed = parse_server(line)
        if parsed is None:
            continue
        if parsed in seen:
            print(f"  '{line}' уже в списке, пропускаю")
            continue
        seen.add(parsed)
        servers.append(parsed)
    return servers


async def check_one(host: str, port: int) -> dict:
    name = f"{host}:{port}"
    try:
        server = BedrockServer(host, port, timeout=TIMEOUT)
        status = await asyncio.wait_for(server.async_status(), timeout=TIMEOUT + 2)
        ver_name = getattr(status.version, "name", "") or ""
        protocol = getattr(status.version, "protocol", None)
        version = ver_name or (f"proto {protocol}" if protocol is not None else "?")
        return {
            "host": name,
            "online": status.players.online,
            "max": status.players.max,
            "version": version,
            "ok": True,
        }
    except asyncio.TimeoutError:
        return {"host": name, "ok": False, "error": "таймаут (сервер не ответил)"}
    except Exception as e:
        # у некоторых исключений str(e) пустой — показываем хотя бы тип
        return {"host": name, "ok": False, "error": str(e) or type(e).__name__}


async def check_and_print(servers: list[tuple[str, int]]) -> None:
    print(f"\nПроверяю {len(servers)} серверов...\n")
    results = await asyncio.gather(*(check_one(h, p) for h, p in servers))

    alive = [r for r in results if r["ok"]]
    dead = [r for r in results if not r["ok"]]
    alive.sort(key=lambda r: r["online"], reverse=True)

    if alive:
        w = max(30, max(len(r["host"]) for r in alive))
        print(f"{'Сервер':{w}} {'Онлайн':>8} {'Макс':>6} {'Версия':>10}")
        print("-" * (w + 27))
        for r in alive:
            print(f"{r['host']:{w}} {r['online']:>8} {r['max']:>6} {r['version']:>10}")
    else:
        print("Ни один сервер не ответил.")

    if dead:
        print("\nНе ответили:")
        for r in dead:
            print(f"  {r['host']}: {r['error']}")


async def main() -> None:
    print(BANNER)
    print("Для выхода оставь список пустым (просто нажми Enter без адресов).\n")
    while True:
        servers = parse_input()
        if not servers:
            print("Список пуст, выходим.")
            break
        await check_and_print(servers)
        print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nВыход.")
