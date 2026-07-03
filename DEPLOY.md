# EAM-Inspection 企业点检管理系统 - 部署文档

## 1. 环境要求
- Linux（Ubuntu 20.04+）或 Windows Server 2019+
- Docker 20.10+ + Docker Compose 2.0+
- 开放端口：80（Web）、443（HTTPS 可选）

## 2. 快速启动

### 2.1 获取代码
```bash
git clone https://github.com/Bowen0011/EAM-Inspection.git
cd EAM-Inspection
```

### 2.2 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，修改以下必填项
```

| 变量 | 说明 | 建议值 |
|------|------|--------|
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 | 随机 16 位强密码 |
| `JWT_SECRET_KEY` | JWT 加密密钥 | 随机 32 位字符串 |
| `WECHAT_APPID` | 微信小程序 AppID | 从微信公众平台获取 |
| `WECHAT_SECRET` | 微信小程序 Secret | 从微信公众平台获取 |

### 2.3 启动服务
```bash
# 生产环境
docker-compose -f docker-compose.prod.yml up -d

# 查看状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

### 2.4 初始化数据库
```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### 2.5 访问系统
- PC 后台：http://服务器IP
- API 文档：http://服务器IP/docs
- 默认管理员：`admin` / `admin123456`（首次登录请立即修改密码）

## 3. 升级指南
```bash
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## 4. 备份与恢复

### 4.1 数据库备份
```bash
docker exec eam-mysql mysqldump -uroot -p${MYSQL_ROOT_PASSWORD} eam_inspection > backup_$(date +%Y%m%d).sql
```

### 4.2 恢复数据库
```bash
docker exec -i eam-mysql mysql -uroot -p${MYSQL_ROOT_PASSWORD} eam_inspection < backup_20260701.sql
```

### 4.3 上传文件备份
```bash
tar -czf uploads_$(date +%Y%m%d).tar.gz volumes/uploads/
```

## 5. 常见问题

### Q1: MySQL 容器启动失败
```bash
docker-compose -f docker-compose.prod.yml logs mysql
sudo chown -R 999:999 volumes/mysql/
```

### Q2: 后端连接不上数据库
- 确认 MySQL 容器已完全启动（`docker-compose ps` 状态为 healthy）
- 检查 `.env` 中的 `MYSQL_PASSWORD` 是否与 `docker-compose.prod.yml` 一致

### Q3: Nginx 端口被占用
修改 `docker-compose.prod.yml`：
```yaml
ports:
  - "8080:80"
```

## 6. 架构图
```
┌─────────┐    ┌──────────┐    ┌──────────┐
│  用户   │ ──▶│  Nginx   │ ──▶│ FastAPI  │
│ (浏览器) │    │   (80)   │    │  (8000)   │
└─────────┘    └──────────┘    └─────┬────┘
                                      │
                             ┌────────▼──────┐
                             │   MySQL 8.0    │
                             │   + Redis 7    │
                             └───────────────┘