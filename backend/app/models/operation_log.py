"""
操作日志表 (operation_logs)
用于审计追溯所有写操作
"""
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, JSON, func
from app.database import Base


class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    operator_id = Column(Integer, nullable=False, comment="操作人ID")
    operator_name = Column(String(50), nullable=True, comment="操作人姓名")
    action_type = Column(String(20), nullable=False, comment="操作类型: CREATE/UPDATE/DELETE/LOGIN")
    module = Column(String(50), nullable=False, comment="操作模块: devices/templates/users/inspection/auth")
    target = Column(String(100), nullable=True, comment="操作对象标识")
    changes = Column(JSON, nullable=True, comment="变更详情")
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    created_at = Column(DateTime, default=func.now(), nullable=False, comment="操作时间")

    def to_dict(self):
        return {
            "id": self.id,
            "operator_id": self.operator_id,
            "operator_name": self.operator_name,
            "action_type": self.action_type,
            "module": self.module,
            "target": self.target,
            "changes": self.changes,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }