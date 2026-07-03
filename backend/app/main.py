"""
FastAPI 应用入口
注册所有路由、中间件、事件处理器
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db, SessionLocal
from app.api.v1 import auth_router, devices_router, inspection_router, analysis_router, templates_router, users_router, reports_router, logs_router
from app.services.auth_service import init_admin_user
from app.websocket.manager import manager
from app.services.log_service import log_operation
from app.utils.jwt_handler import verify_token
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="EAM-Inspection 企业点检管理系统",
    description="企业设备点检管理系统 API，支持移动端小程序和 PC Web 后台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 配置（允许小程序和前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api/v1")
app.include_router(devices_router, prefix="/api/v1")
app.include_router(inspection_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(templates_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(logs_router, prefix="/api/v1")


# 全局异常处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join([str(loc) for loc in error.get("loc", [])]),
            "message": error.get("msg", "")
        })
    return JSONResponse(
        status_code=422,
        content={"detail": "参数校验失败", "errors": errors}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )


@app.middleware("http")
async def operation_log_middleware(request, call_next):
    """操作日志中间件 — 记录所有 POST/PUT/DELETE 请求"""
    path = request.url.path
    if not path.startswith("/api/v1/") or request.method == "GET":
        return await call_next(request)

    method = request.method
    action_map = {"POST": "CREATE", "PUT": "UPDATE", "DELETE": "DELETE"}
    action_type = action_map.get(method, method)
    module = path.split("/")[3] if len(path.split("/")) > 3 else "unknown"

    response = await call_next(request)

    try:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = verify_token(token)
            if payload and 200 <= response.status_code < 300:
                user_id = int(payload.get("sub", 0))
                username = payload.get("username", "")
                # 提取操作目标（最后一段路径）
                parts = path.split("/")
                target = parts[-1] if len(parts) > 1 else ""

                db = SessionLocal()
                try:
                    log_operation(
                        db=db,
                        operator_id=user_id,
                        operator_name=username,
                        action_type=action_type,
                        module=module,
                        target=target,
                        ip_address=request.client.host if request.client else None
                    )
                finally:
                    db.close()
    except Exception:
        pass

    return response


@app.on_event("startup")
async def startup_event():
    """
    应用启动时的初始化操作
    - 初始化数据库表
    - 创建管理员账号
    """
    logger.info("正在初始化数据库...")
    init_db()
    logger.info("数据库表初始化完成")

    # 初始化管理员账号
    db = SessionLocal()
    try:
        init_admin_user(db)
        logger.info("管理员账号初始化完成")
    finally:
        db.close()

    logger.info("EAM-Inspection 系统启动完成")


@app.get("/api/v1/health", tags=["系统健康检查"])
def health_check():
    """
    系统健康检查接口
    """
    return {
        "status": "ok",
        "service": "EAM-Inspection",
        "version": "1.0.0"
    }


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 通知端点
    工程师通过此连接接收实时异常通知
    需在连接后立即发送 JSON: {"type": "auth", "user_id": 1}
    """
    await websocket.accept()

    user_id = None
    try:
        # 等待认证消息
        auth_data = await websocket.receive_json()
        if auth_data.get("type") == "auth" and auth_data.get("user_id"):
            user_id = int(auth_data["user_id"])
            await manager.connect(websocket, user_id)
            logger.info(f"用户 {user_id} 通过 WebSocket 连接")

            # 发送连接成功确认
            await websocket.send_json({
                "type": "auth_success",
                "message": f"用户 {user_id} 连接成功"
            })

            # 保持连接，等待消息
            while True:
                data = await websocket.receive_text()
                # 客户端可以发送 ping 保持连接
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
        else:
            await websocket.send_json({
                "type": "error",
                "message": "认证格式错误，请发送 {\"type\": \"auth\", \"user_id\": 1}"
            })
            await websocket.close()

    except WebSocketDisconnect:
        if user_id:
            manager.disconnect(user_id)
            logger.info(f"用户 {user_id} 断开 WebSocket 连接")
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
        if user_id:
            manager.disconnect(user_id)