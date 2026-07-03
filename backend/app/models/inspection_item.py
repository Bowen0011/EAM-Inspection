"""
点检模板明细表 (inspection_items)
"""
from sqlalchemy import Column, Integer, String, Float, Enum as SAEnum
from app.database import Base
import enum


class DataType(str, enum.Enum):
    NUMBER = "number"
    BOOLEAN = "boolean"
    TEXT = "text"


class InspectionItem(Base):
    __tablename__ = "inspection_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_id = Column(Integer, nullable=False, index=True, comment="模板ID")
    item_name = Column(String(50), nullable=False, comment="项目名（如：主轴温度）")
    data_type = Column(SAEnum(DataType), nullable=False, comment="数据类型：number/boolean/text")
    standard_min = Column(Float, nullable=True, comment="下限值（数值类必填）")
    standard_max = Column(Float, nullable=True, comment="上限值（数值类必填）")
    unit = Column(String(10), nullable=True, comment="单位（℃/MPa）")

    def to_dict(self):
        return {
            "id": self.id,
            "template_id": self.template_id,
            "item_name": self.item_name,
            "data_type": self.data_type.value if self.data_type else None,
            "standard_min": self.standard_min,
            "standard_max": self.standard_max,
            "unit": self.unit
        }