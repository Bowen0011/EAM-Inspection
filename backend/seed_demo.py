"""
种子数据脚本
预置演示数据：用户、设备、模板、点检记录
运行方式：python seed_demo.py
"""
import os
os.environ["USE_SQLITE"] = "true"

from datetime import datetime, timedelta
import random
from passlib.hash import bcrypt

from app.database import Base, engine, SessionLocal
from app.models.user import User, UserRole
from app.models.device import Device
from app.models.inspection_template import InspectionTemplate
from app.models.inspection_item import InspectionItem, DataType
from app.models.inspection_record import InspectionRecord, ResultStatus


def seed_database():
    """填充演示数据"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 如果已有数据则跳过
        if db.query(User).count() > 0:
            print("数据库已有数据，跳过种子填充")
            return

        print("正在填充演示数据...")

        # ==================== 用户 ====================
        users = [
            User(username="admin", password_hash=bcrypt.hash("admin123456"),
                 role=UserRole.ENGINEER, real_name="管理员", is_active=1),
            User(username="zhang", password_hash=bcrypt.hash("123456"),
                 role=UserRole.TECH, real_name="张师傅", is_active=1),
            User(username="li", password_hash=bcrypt.hash("123456"),
                 role=UserRole.TECH, real_name="李师傅", is_active=1),
            User(username="wang", password_hash=bcrypt.hash("123456"),
                 role=UserRole.TECH, real_name="王师傅", is_active=1),
            User(username="disabled_tech", password_hash=bcrypt.hash("123456"),
                 role=UserRole.TECH, real_name="已禁用技术员", is_active=0),
        ]
        for u in users:
            db.add(u)
        db.flush()
        user_map = {u.username: u for u in users}
        print(f"  ✓ 用户: {len(users)} 个")

        # ==================== 模板 ====================
        templates_data = [
            {
                "template_name": "数控车床日常点检",
                "device_type": "车床类",
                "items": [
                    {"item_name": "主轴温度", "data_type": "number", "standard_min": 20, "standard_max": 65, "unit": "℃"},
                    {"item_name": "润滑油位", "data_type": "boolean"},
                    {"item_name": "冷却液压力", "data_type": "number", "standard_min": 0.3, "standard_max": 0.6, "unit": "MPa"},
                    {"item_name": "异响检查", "data_type": "boolean"},
                    {"item_name": "刀具磨损情况", "data_type": "text"},
                ]
            },
            {
                "template_name": "空压机日常点检",
                "device_type": "动力设备",
                "items": [
                    {"item_name": "排气温度", "data_type": "number", "standard_min": 60, "standard_max": 100, "unit": "℃"},
                    {"item_name": "油位正常", "data_type": "boolean"},
                    {"item_name": "排水阀状态", "data_type": "boolean"},
                    {"item_name": "运行电流", "data_type": "number", "standard_min": 10, "standard_max": 50, "unit": "A"},
                ]
            },
            {
                "template_name": "环保废气处理系统点检",
                "device_type": "环保设备",
                "items": [
                    {"item_name": "风机电流", "data_type": "number", "standard_min": 5, "standard_max": 30, "unit": "A"},
                    {"item_name": "活性炭压差", "data_type": "number", "standard_min": 0, "standard_max": 2, "unit": "kPa"},
                    {"item_name": "排放风机运行", "data_type": "boolean"},
                ]
            },
        ]
        templates = []
        for tdata in templates_data:
            t = InspectionTemplate(template_name=tdata["template_name"], device_type=tdata["device_type"])
            db.add(t)
            db.flush()
            for item_data in tdata["items"]:
                item = InspectionItem(
                    template_id=t.id,
                    item_name=item_data["item_name"],
                    data_type=item_data["data_type"],
                    standard_min=item_data.get("standard_min"),
                    standard_max=item_data.get("standard_max"),
                    unit=item_data.get("unit", ""),
                )
                db.add(item)
            templates.append(t)
        db.flush()
        print(f"  ✓ 模板: {len(templates)} 套")

        # ==================== 设备 ====================
        devices_data = [
            ("CSGZ-A01-DBC-01", "数控车床 #1", "A车间-加工区-01工位", templates[0].id),
            ("CSGZ-A01-DBC-02", "数控车床 #2", "A车间-加工区-02工位", templates[0].id),
            ("CSGZ-A02-WT-01", "卧式加工中心 #1", "A车间-精加工区-01工位", templates[0].id),
            ("CSGZ-A03-PT-01", "空压机 #1", "B车间-动力站-01位", templates[1].id),
            ("CSGZ-A03-PT-02", "空压机 #2", "B车间-动力站-02位", templates[1].id),
            ("CSGZ-A04-MMIT-01", "三坐标测量机", "C车间-质检区-01位", templates[0].id),
            ("CSGZ-P05-MT-01", "铣床 #1", "A车间-铣削区-01工位", templates[0].id),
            ("CSGZ-S02-UT-01", "环保废气处理系统", "F车间-环保区-01位", templates[2].id),
        ]
        devices = []
        for code, name, loc, tid in devices_data:
            d = Device(device_code=code, device_name=name, location=loc, template_id=tid)
            db.add(d)
            devices.append(d)
        db.flush()
        print(f"  ✓ 设备: {len(devices)} 台")

        # ==================== 点检记录 ====================
        now = datetime.now()
        techs = [user_map["zhang"], user_map["li"], user_map["wang"]]
        records = []

        record_id = 1
        for day_offset in range(7):
            check_date = now - timedelta(days=day_offset)
            for tech in techs:
                assigned = devices[:4] if tech.username == "zhang" else (devices[4:6] if tech.username == "li" else devices[6:])
                for dev in assigned[:random.randint(2, len(assigned))]:
                    is_fail = random.random() < 0.15
                    record = InspectionRecord(
                        id=record_id,
                        device_code=dev.device_code,
                        tech_id=tech.id,
                        check_time=check_date.replace(hour=random.randint(7, 17), minute=random.randint(0, 59)),
                        gps_lat=22.53 + random.random() * 0.01,
                        gps_lng=113.93 + random.random() * 0.01,
                        photo_urls=["/static/uploads/demo.jpg"],
                        result_status=ResultStatus.FAIL if is_fail else ResultStatus.PASS,
                        remark="主轴温度偏高，已通知维修" if is_fail else "",
                        engineer_remark="已安排检查冷却系统" if is_fail and random.random() < 0.5 else None,
                        is_deleted=0,
                    )
                    db.add(record)
                    records.append(record)
                    record_id += 1

        db.commit()
        print(f"  ✓ 点检记录: {len(records)} 条")
        print("✅ 演示数据填充完成！")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()