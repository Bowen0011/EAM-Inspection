"""
设备档案表 (devices)
device_code 为全局唯一主键
"""
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    device_code = Column(String(50), primary_key=True, comment="设备编号（全局唯一主键）")
    device_name = Column(String(100), nullable=False, comment="设备名称")
    location = Column(String(200), nullable=False, comment="具体位置（车间/工位）")
    template_id = Column(Integer, ForeignKey("inspection_items.template_id"), nullable=False, comment="关联点检模板")
    qr_url = Column(String(500), nullable=True, comment="二维码图片访问地址")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="退役标记 0正常 1已退役")

    def to_dict(self):
        return {
            "device_code": self.device_code,
            "device_name": self.device_name,
            "location": self.location,
            "template_id": self.template_id,
            "qr_url": self.qr_url,
            "is_deleted": self.is_deleted
        }
