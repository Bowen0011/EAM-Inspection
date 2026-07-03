"""
点检执行记录表 (inspection_records) —— 核心不可变表
禁止物理删除，只有 is_deleted 软删除和工程师备注字段允许修改
"""
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, Enum as SAEnum, \
    DECIMAL, JSON, SmallInteger, func
from app.database import Base
import enum
from datetime import datetime


class ResultStatus(str, enum.Enum):
    PASS = "pass"   # 合格
    FAIL = "fail"   # 异常


class InspectionRecord(Base):
    __tablename__ = "inspection_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_code = Column(String(50), nullable=False, index=True, comment="关联设备编号")
    tech_id = Column(Integer, nullable=False, comment="技术员ID")
    check_time = Column(DateTime, nullable=False, default=func.now(), comment="提交时间（服务器时间）")
    gps_lat = Column(DECIMAL(10, 7), nullable=True, comment="纬度（防作弊）")
    gps_lng = Column(DECIMAL(10, 7), nullable=True, comment="经度（防作弊）")
    photo_urls = Column(JSON, nullable=True, comment="拍照图片URL数组")
    result_status = Column(SAEnum(ResultStatus), nullable=False, comment="pass(合格)/fail(异常)")
    remark = Column(Text, nullable=True, comment="异常原因（fail时必填）；工程师可追加备注")
    engineer_remark = Column(Text, nullable=True, comment="工程师追加备注")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="软删除标记，默认0（禁止物理删除）")

    def to_dict(self):
        return {
            "id": self.id,
            "device_code": self.device_code,
            "tech_id": self.tech_id,
            "check_time": self.check_time.isoformat() if self.check_time else None,
            "gps_lat": float(self.gps_lat) if self.gps_lat else None,
            "gps_lng": float(self.gps_lng) if self.gps_lng else None,
            "photo_urls": self.photo_urls,
            "result_status": self.result_status.value if self.result_status else None,
            "remark": self.remark,
            "engineer_remark": self.engineer_remark,
            "is_deleted": self.is_deleted
        }