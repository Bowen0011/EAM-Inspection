"""
RBAC 权限依赖
角色-权限映射及权限检查依赖工厂
"""
from fastapi import Depends, HTTPException, status
from app.api.v1.auth import get_current_user_role

ROLE_PERMISSIONS = {
    "admin": [
        "templates:create", "templates:edit", "templates:delete",
        "users:manage", "reports:export", "devices:manage",
        "inspection:submit",
    ],
    "engineer": [
        "templates:create", "templates:edit",
        "reports:export", "devices:manage",
    ],
    "tech": [
        "inspection:submit",
    ],
    "store": [
        "reports:export",
    ],
}


def require_permission(permission: str):
    """
    权限检查依赖工厂
    用法: Depends(require_permission("templates:create"))
    """
    def permission_checker(current_user: dict = Depends(get_current_user_role)):
        role = current_user.get("role")
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无法识别用户角色"
            )
        user_permissions = ROLE_PERMISSIONS.get(role, [])
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要 {permission} 权限"
            )
        return current_user
    return permission_checker