"""
操作日志服务
用于记录所有写操作的审计日志
"""
from sqlalchemy.orm import Session
from app.models.operation_log import OperationLog


def log_operation(
    db: Session,
    operator_id: int,
    operator_name: str,
    action_type: str,
    module: str,
    target: str = None,
    changes: dict = None,
    ip_address: str = None
):
    """
    记录操作日志
    """
    log = OperationLog(
        operator_id=operator_id,
        operator_name=operator_name,
        action_type=action_type,
        module=module,
        target=target,
        changes=changes,
        ip_address=ip_address
    )
    db.add(log)
    db.commit()