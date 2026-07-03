"""
WebSocket 连接管理器
用于向在线工程师推送异常通知
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import asyncio


class ConnectionManager:
    """
    WebSocket 连接管理
    维护所有在线工程师的 WebSocket 连接
    """

    def __init__(self):
        # {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """
        接受 WebSocket 连接并注册
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        """
        断开 WebSocket 连接
        """
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, user_id: int):
        """
        向指定用户发送消息
        """
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(user_id)

    async def broadcast(self, message: dict):
        """
        向所有在线用户广播消息
        """
        for user_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, user_id)

    def is_online(self, user_id: int) -> bool:
        """
        检查用户是否在线
        """
        return user_id in self.active_connections


# 全局连接管理器实例
manager = ConnectionManager()


async def notify_engineers_abnormal(record_data: dict):
    """
    当出现异常点检时，通知所有在线工程师
    """
    message = {
        "type": "abnormal_alert",
        "title": "新异常点检通知",
        "content": f"设备 {record_data.get('device_code', '未知')} 点检异常",
        "record_id": record_data.get("id"),
        "device_code": record_data.get("device_code"),
        "check_time": record_data.get("check_time"),
        "remark": record_data.get("remark"),
        "timestamp": asyncio.get_event_loop().time()
    }
    await manager.broadcast(message)