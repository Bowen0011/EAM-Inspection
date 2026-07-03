"""
点检模板管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.inspection_template import InspectionTemplate
from app.models.inspection_item import InspectionItem
from app.models.device import Device
from app.api.v1.auth import get_current_user_role
from app.schemas.template import TemplateCreateRequest, TemplateListItemResponse

router = APIRouter(prefix="/templates", tags=["模板管理"])


@router.get("/list", summary="获取模板列表")
def list_templates(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    templates = db.query(InspectionTemplate).filter(
        InspectionTemplate.is_deleted == 0
    ).order_by(InspectionTemplate.created_at.desc()).all()

    result = []
    for t in templates:
        item_count = db.query(func.count(InspectionItem.id)).filter(
            InspectionItem.template_id == t.id
        ).scalar()
        result.append({
            "id": t.id,
            "template_name": t.template_name,
            "device_type": t.device_type,
            "item_count": item_count,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "updated_at": t.updated_at.isoformat() if t.updated_at else None
        })
    return result


@router.get("/{template_id}", summary="获取模板详情")
def get_template_detail(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    template = db.query(InspectionTemplate).filter(
        InspectionTemplate.id == template_id,
        InspectionTemplate.is_deleted == 0
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    items = db.query(InspectionItem).filter(
        InspectionItem.template_id == template_id
    ).all()

    return {
        "id": template.id,
        "template_name": template.template_name,
        "device_type": template.device_type,
        "created_at": template.created_at.isoformat() if template.created_at else None,
        "updated_at": template.updated_at.isoformat() if template.updated_at else None,
        "items": [item.to_dict() for item in items]
    }


@router.post("", summary="创建模板", status_code=201)
def create_template(
    request: TemplateCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    template = InspectionTemplate(
        template_name=request.template_name,
        device_type=request.device_type
    )
    db.add(template)
    db.flush()

    for item_data in request.items:
        item = InspectionItem(
            template_id=template.id,
            item_name=item_data.item_name,
            data_type=item_data.data_type,
            standard_min=item_data.standard_min,
            standard_max=item_data.standard_max,
            unit=item_data.unit
        )
        db.add(item)

    db.commit()
    db.refresh(template)
    return {"message": "模板创建成功", "template_id": template.id}


@router.put("/{template_id}", summary="更新模板")
def update_template(
    template_id: int,
    request: TemplateCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    template = db.query(InspectionTemplate).filter(
        InspectionTemplate.id == template_id,
        InspectionTemplate.is_deleted == 0
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    template.template_name = request.template_name
    template.device_type = request.device_type

    db.query(InspectionItem).filter(
        InspectionItem.template_id == template_id
    ).delete()

    for item_data in request.items:
        item = InspectionItem(
            template_id=template.id,
            item_name=item_data.item_name,
            data_type=item_data.data_type,
            standard_min=item_data.standard_min,
            standard_max=item_data.standard_max,
            unit=item_data.unit
        )
        db.add(item)

    db.commit()
    return {"message": "模板更新成功"}


@router.delete("/{template_id}", summary="软删除模板")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    template = db.query(InspectionTemplate).filter(
        InspectionTemplate.id == template_id,
        InspectionTemplate.is_deleted == 0
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    device_count = db.query(func.count(Device.device_code)).filter(
        Device.template_id == template_id
    ).scalar()
    if device_count > 0:
        raise HTTPException(
            status_code=409,
            detail=f"该模板已被 {device_count} 台设备使用，无法删除"
        )

    template.is_deleted = 1
    db.commit()
    return {"message": "模板已删除"}