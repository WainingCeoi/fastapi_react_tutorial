"""One-command LAN host for the app (API + built UI from one process).

Run it via `make host` (which builds the frontend first). It:
  1. finds a free TCP port starting at $PORT (default 8000, walking up to +20),
  2. binds $HOST (default 0.0.0.0 = every network interface; set 127.0.0.1 for
     local-only) with ONE worker — the app seeds/creates its schema at startup,
     so multiple workers would double-run that,
  3. prints the URLs other devices on the Wi-Fi can actually use, reading this
     machine's own mDNS/Bonjour name at runtime (never hardcoded).

This is a production-STYLE convenience host over plain HTTP for a trusted LAN —
not a hardened deployment. See the security banner it prints, and README hosting notes.
"""

import os
import socket
import subprocess
import sys

import uvicorn

APP = "app.main:app"
PORT_SCAN_LIMIT = 20  # how many ports to try before giving up


def find_free_port(host: str, base: int, tries: int = PORT_SCAN_LIMIT) -> int:
    """Return the first free port >= base by actually attempting to bind it.

    No SO_REUSEADDR on the probe — we want an honest "is anyone here?" check, so a
    port lingering in TIME_WAIT reads as busy and we walk past it.
    """
    for port in range(base, base + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind((host, port))
            except OSError:
                continue  # in use → try the next one
            return port
    sys.exit(f"host.py: no free port in {base}..{base + tries - 1} — is something looping?")


def mdns_name() -> str | None:
    """This machine's mDNS name (e.g. 'weining.local'), read at runtime."""
    if sys.platform == "darwin":
        try:
            out = subprocess.run(
                ["scutil", "--get", "LocalHostName"],
                capture_output=True, text=True, timeout=2,
            ).stdout.strip()
            if out:
                return f"{out.lower()}.local"
        except (OSError, subprocess.SubprocessError):
            pass
    # Linux (avahi) and macOS fallback: the short hostname resolves over mDNS as <name>.local
    short = socket.gethostname().split(".")[0].strip().lower()
    if not short:
        return None
    return short if short.endswith(".local") else f"{short}.local"


def _is_private(ip: str) -> bool:
    """True for RFC1918 LAN ranges (10/8, 172.16/12, 192.168/16)."""
    return (
        ip.startswith("192.168.")
        or ip.startswith("10.")
        or any(ip.startswith(f"172.{n}.") for n in range(16, 32))
    )


def _interface_ips() -> list[str]:
    """IPv4 addresses of physical interfaces (used to find the real LAN IP).

    On macOS we scan en0..en9 — VPN tunnels are utunN, not enN, so this naturally
    ignores them. On Linux, `hostname -I` lists the host's addresses.
    """
    ips: list[str] = []
    try:
        if sys.platform == "darwin":
            for i in range(10):
                out = subprocess.run(
                    ["ipconfig", "getifaddr", f"en{i}"],
                    capture_output=True, text=True, timeout=1,
                ).stdout.strip()
                if out:
                    ips.append(out)
        else:
            out = subprocess.run(
                ["hostname", "-I"], capture_output=True, text=True, timeout=1,
            ).stdout
            ips.extend(out.split())
    except (OSError, subprocess.SubprocessError):
        pass
    return ips


def lan_ip() -> str | None:
    """The address other devices on the Wi-Fi would use — a private LAN IP.

    Fast path: the interface that routes outward (a no-op UDP 'connect' just selects
    it). But on a VPN that can be an off-LAN address, so we only trust it when it's a
    private LAN IP; otherwise we scan the physical interfaces for one.
    """
    primary = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            primary = s.getsockname()[0]
    except OSError:
        pass
    if primary and _is_private(primary):
        return primary
    for ip in _interface_ips():
        if _is_private(ip):
            return ip
    return primary  # nothing better (may be None)


def main() -> None:
    # Flush the URLs immediately even when stdout is a pipe/file (e.g. `make host`
    # output captured by a process manager) — otherwise block buffering hides them.
    sys.stdout.reconfigure(line_buffering=True)

    host = os.environ.get("HOST", "0.0.0.0").strip() or "0.0.0.0"
    base_port = int(os.environ.get("PORT", "8000"))
    port = find_free_port(host, base_port)

    lan_exposed = host in ("0.0.0.0", "::", "")

    print("\n  Serving the app (single origin: UI + API) — 1 worker\n")
    if base_port != port:
        print(f"  note: base port {base_port} was busy → using {port}\n")
    print(f"  • this machine : http://localhost:{port}")
    if lan_exposed:
        name = mdns_name()
        ip = lan_ip()
        if name:
            print(f"  • other devices: http://{name}:{port}")
        if ip:
            print(f"  • or via IP    : http://{ip}:{port}")
        print(
            "\n  ⚠️  Bound to 0.0.0.0 — reachable by EVERY device on this network.\n"
            "     • Only do this on a network you trust.\n"
            "     • SECRET_KEY must be a real 32+ char value (the app won't boot otherwise).\n"
            "     • Plain HTTP, no TLS — fine for a trusted LAN; an installable PWA\n"
            "       would need a secure context (HTTPS) to work.\n"
        )
    else:
        print(f"  (HOST={host} → local only; not exposed to the LAN)\n")

    # One worker: the FastAPI lifespan runs create_all + seed at startup — running it
    # in several worker processes would race/duplicate that boot work.
    uvicorn.run(APP, host=host, port=port, workers=1, log_level="info")


if __name__ == "__main__":
    main()
