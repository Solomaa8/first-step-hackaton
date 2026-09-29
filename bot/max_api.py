"""
MAX Bot API Client — нативная обёртка для platform-api2.max.ru.
Использует Long Polling (GET /updates) и отправку сообщений (POST /messages).
"""
import httpx
import asyncio
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

MAX_API_BASE = "https://platform-api2.max.ru"


class MaxBotAPI:
    def __init__(self, token: str, base_url: str = MAX_API_BASE):
        self.token = token
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            timeout=60.0,
            verify=False,
            trust_env=False,
            headers={"Authorization": token}
        )
        self._marker: Optional[int] = None

    async def get_me(self) -> Dict[str, Any]:
        """Получить информацию о боте."""
        resp = await self._client.get(f"{self.base_url}/me")
        if resp.status_code >= 400:
            logger.error(f"API Error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
        return resp.json()

    async def send_message(
        self,
        chat_id: Optional[int] = None,
        user_id: Optional[int] = None,
        text: str = "",
        inline_keyboard: Optional[List[List[Dict[str, Any]]]] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """Отправить сообщение в чат или пользователю."""
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        elif user_id is not None:
            params["user_id"] = user_id

        body: Dict[str, Any] = {"text": text}
        if inline_keyboard:
            body["attachments"] = [
                {
                    "type": "inline_keyboard",
                    "payload": {"buttons": inline_keyboard}
                }
            ]
        if reply_to:
            body["link"] = {"type": "reply", "mid": reply_to}

        resp = await self._client.post(
            f"{self.base_url}/messages",
            params=params,
            json=body if body else {}
        )
        if resp.status_code >= 400:
            logger.error(f"API Error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
        return resp.json()

    async def edit_message(
        self,
        message_id: str,
        text: str,
        inline_keyboard: Optional[List[List[Dict[str, Any]]]] = None
    ) -> Dict[str, Any]:
        """Редактировать сообщение."""
        body: Dict[str, Any] = {"text": text}
        if inline_keyboard:
            body["attachments"] = [
                {
                    "type": "inline_keyboard",
                    "payload": {"buttons": inline_keyboard}
                }
            ]
        resp = await self._client.put(
            f"{self.base_url}/messages",
            params={"message_id": message_id},
            json=body if body else {}
        )
        if resp.status_code >= 400:
            logger.error(f"API Error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
        return resp.json()

    async def answer_callback(
        self,
        callback_id: str,
        notification: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ответить на callback от нажатия кнопки (параметр callback_id в query)."""
        params = {"callback_id": callback_id}
        body: Dict[str, Any] = {}
        if notification:
            body["notification"] = notification
        resp = await self._client.post(
            f"{self.base_url}/answers",
            params=params,
            json=body if body else {}
        )
        if resp.status_code >= 400:
            logger.error(f"API Error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
        return resp.json()

    async def get_updates(self, limit: int = 50, timeout: int = 25) -> List[Dict[str, Any]]:
        """Получить обновления через Long Polling."""
        params: Dict[str, Any] = {"limit": limit, "timeout": timeout}
        if self._marker is not None:
            params["marker"] = self._marker

        try:
            resp = await self._client.get(
                f"{self.base_url}/updates",
                params=params,
                timeout=timeout + 10
            )
            if resp.status_code >= 400:
                logger.error(f"API Error {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            data = resp.json()
            updates = data.get("updates", [])
            if "marker" in data:
                self._marker = data["marker"]
            return updates
        except httpx.ReadTimeout:
            return []
        except Exception as e:
            logger.error(f"Ошибка при получении updates: {e}")
            await asyncio.sleep(2)
            return []

    async def close(self):
        await self._client.aclose()

