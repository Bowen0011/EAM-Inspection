"""
点检模板表 (inspection_templates)
作为点检模板的主表，inspection_items 通过 template_id 关联到此表
"""
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, func
from app.database import Base


class InspectionTemplate(Base):
    __tablename__ = "inspection_templates"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    template_name = Column(String(50), nullable=False, comment="模板名称")
    device_type = Column(String(50), nullable=True, comment="适用设备类型")
    is_deleted = Column(SmallInteger, default=0, nullable=False, comment="软删除标记，0正常/1已删除")
    created_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    def to_dict(self):
        return {
            "id": self.id,
            "template_name": self.template_name,
            "device_type": self.device_type,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }