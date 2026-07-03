"""
EAM-Inspection 演示启动脚本
使用 SQLite 数据库，无需 Docker/MySQL，预置演示数据
启动后浏览器打开 http://localhost:8000/docs

测试账号：
  工程师 - admin / admin123456
  技术员 - 张师傅 / 123456
         李师傅 / 123456
         王师傅 / 123456
"""
import os
import sys

# 在导入任何 app 模块前设置环境变量
os.environ["USE_SQLITE"] = "true"
os.environ["MYSQL_HOST"] = "127.0.0.1"

import uvicorn

# 先填充种子数据
from seed_demo import seed_database

if __name__ == "__main__":
    print("=" * 50)
    print("  EAM-Inspection 演示环境")
    print("=" * 50)
    print()

    # 填充数据
    seed_database()

    print()
    print("=" * 50)
    print("  Swagger UI: http://localhost:8000/docs")
    print("  测试账号:")
    print("    工程师: admin / admin123456")
    print("    技术员: 张师傅 / 123456")
    print("    技术员: 李师傅 / 123456")
    print("    技术员: 王师傅 / 123456")
    print("=" * 50)
    print()

    # 启动服务器
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)