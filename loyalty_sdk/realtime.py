"""
Realtime subscriptions over the Pusher wire protocol.

QR results arrive on a channel, not in a response body. Polling for them costs a
request per second per session while a customer stands at the till, so the SDK
speaks the socket directly rather than leaving you to write the loop.

The QR channels are public — the unguessable session id in the channel name is the
secret — so there is no token to manage and nothing to authorize.
"""

import json
import time
from typing import Any, Callable, Dict, Optional

try:
    import websocket  # websocket-client
except ImportError:  # pragma: no cover - surfaced with a useful message below
    websocket = None

from .exceptions import LoyaltySDKError

# The client name and protocol version the broker expects in the handshake query.
_PROTOCOL = 7
_CLIENT = "loyaltylt-python"


class RealtimeSubscriber:
    """
    One short-lived subscription to one public channel.

    Built by `LoyaltySDK.subscribe_qr_login()` / `subscribe_qr_card()`; you normally
    do not construct it yourself.
    """

    def __init__(self, config: Dict[str, Any], channel: str, events: list):
        if websocket is None:
            raise LoyaltySDKError(
                "Realtime needs the websocket-client package: pip install 'loyaltylt-sdk[realtime]'",
                "MISSING_DEPENDENCY",
            )

        self.config = config
        self.channel = channel
        self.events = events
        self._ws = None

    def _url(self) -> str:
        scheme = "wss" if self.config.get("scheme") == "https" else "ws"
        host = self.config["host"]
        port = self.config.get("port", 443)
        key = self.config["key"]
        return (
            f"{scheme}://{host}:{port}/app/{key}"
            f"?protocol={_PROTOCOL}&client={_CLIENT}&version=3.0.0"
        )

    def listen(
        self,
        callback: Callable[[str, Dict[str, Any]], Any],
        timeout: int = 300,
    ) -> Optional[Dict[str, Any]]:
        """
        Block until the callback returns a truthy value, or until `timeout` seconds.

        The callback receives `(event_name, payload)` for every frame on the channel.
        Return something truthy from it to stop listening; that value is returned here.
        Returns None on timeout — QR sessions expire after 5 minutes, so the default
        matches.
        """
        deadline = time.time() + timeout
        self._ws = websocket.create_connection(self._url(), timeout=10)

        try:
            # 1. The broker greets us and names the socket.
            self._recv(deadline)

            # 2. Public channel: no auth signature, just the name.
            self._ws.send(json.dumps({
                "event": "pusher:subscribe",
                "data": {"channel": self.channel},
            }))

            while time.time() < deadline:
                frame = self._recv(deadline)
                if frame is None:
                    return None

                event = frame.get("event", "")
                if event.startswith("pusher:") or event.startswith("pusher_internal:"):
                    continue

                # Reverb sends `data` as a JSON string; peer events keep the client- prefix.
                payload = frame.get("data")
                if isinstance(payload, str):
                    try:
                        payload = json.loads(payload)
                    except ValueError:
                        payload = {"raw": payload}

                name = event[len("client-"):] if event.startswith("client-") else event
                if self.events and name not in self.events:
                    continue

                result = callback(name, payload or {})
                if result:
                    return result if isinstance(result, dict) else payload

            return None
        finally:
            self.close()

    def _recv(self, deadline: float) -> Optional[Dict[str, Any]]:
        remaining = deadline - time.time()
        if remaining <= 0:
            return None
        self._ws.settimeout(min(remaining, 30))
        try:
            return json.loads(self._ws.recv())
        except websocket.WebSocketTimeoutException:
            return {} if time.time() < deadline else None
        except ValueError:
            return {}

    def close(self) -> None:
        if self._ws is not None:
            try:
                self._ws.close()
            finally:
                self._ws = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
