from app.api.v1.auth import router as auth_router
from app.api.v1.devices import router as devices_router
from app.api.v1.inspection import router as inspection_router
from app.api.v1.analysis import router as analysis_router

__all__ = ["auth_router", "devices_router", "inspection_router", "analysis_router"]