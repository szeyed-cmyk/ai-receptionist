from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Conversation, Message, KnowledgeItem, Appointment, Setting
from app.ai_service import generate_reply, get_setting, set_setting
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def require_admin(request: Request):
    if request.cookies.get("admin") != "true":
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/chat")
async def web_chat(message: str = Form(...), conversation_id: int = Form(None), db: Session = Depends(get_db)):
    if not conversation_id:
        conv = Conversation(channel="web")
        db.add(conv)
        db.commit()
        db.refresh(conv)
        conversation_id = conv.id
    else:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(404, "Conversation not found")

    user_msg = Message(conversation_id=conversation_id, role="user", content=message)
    db.add(user_msg)
    db.commit()

    reply = await generate_reply(db, conversation_id, message)
    assistant_msg = Message(conversation_id=conversation_id, role="assistant", content=reply)
    db.add(assistant_msg)
    db.commit()

    return {"conversation_id": conversation_id, "reply": reply}


# ---------- Admin ----------
@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/admin/login")
async def do_login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    stored_password = get_setting(db, "admin_password", settings.admin_password)
    if username == settings.admin_username and password == stored_password:
        response = RedirectResponse("/admin", status_code=303)
        response.set_cookie("admin", "true", httponly=True)
        return response
    return RedirectResponse("/admin/login?error=1", status_code=303)


@router.get("/admin/logout")
async def logout():
    response = RedirectResponse("/admin/login", status_code=303)
    response.delete_cookie("admin")
    return response


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    conv_count = db.query(Conversation).count()
    msg_count = db.query(Message).count()
    appt_count = db.query(Appointment).count()
    kb_count = db.query(KnowledgeItem).count()
    recent = db.query(Conversation).order_by(Conversation.updated_at.desc()).limit(10).all()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "conv_count": conv_count,
            "msg_count": msg_count,
            "appt_count": appt_count,
            "kb_count": kb_count,
            "recent": recent,
        },
    )


@router.get("/admin/knowledge", response_class=HTMLResponse)
async def knowledge_list(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    items = db.query(KnowledgeItem).order_by(KnowledgeItem.id.desc()).all()
    return templates.TemplateResponse("knowledge.html", {"request": request, "items": items})


@router.post("/admin/knowledge")
async def knowledge_add(
    request: Request,
    question: str = Form(...),
    answer: str = Form(...),
    category: str = Form("general"),
    db: Session = Depends(get_db),
):
    require_admin(request)
    item = KnowledgeItem(question=question, answer=answer, category=category)
    db.add(item)
    db.commit()
    return RedirectResponse("/admin/knowledge", status_code=303)


@router.post("/admin/knowledge/{item_id}/delete")
async def knowledge_delete(item_id: int, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    item = db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse("/admin/knowledge", status_code=303)


@router.get("/admin/settings", response_class=HTMLResponse)
async def settings_page(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    current = {
        "ai_base_url": get_setting(db, "ai_base_url", settings.ai_base_url),
        "ai_api_key": get_setting(db, "ai_api_key", ""),
        "ai_model": get_setting(db, "ai_model", settings.ai_model),
        "business_name": get_setting(db, "business_name", settings.business_name),
    }
    return templates.TemplateResponse("settings.html", {"request": request, "current": current})


@router.post("/admin/settings")
async def save_settings(
    request: Request,
    ai_base_url: str = Form(...),
    ai_api_key: str = Form(""),
    ai_model: str = Form(...),
    business_name: str = Form(...),
    db: Session = Depends(get_db),
):
    require_admin(request)
    set_setting(db, "ai_base_url", ai_base_url)
    if ai_api_key.strip():
        set_setting(db, "ai_api_key", ai_api_key.strip())
    set_setting(db, "ai_model", ai_model)
    set_setting(db, "business_name", business_name)
    return RedirectResponse("/admin/settings?saved=1", status_code=303)


@router.post("/admin/change-password")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    require_admin(request)
    stored_password = get_setting(db, "admin_password", settings.admin_password)

    if current_password != stored_password:
        return RedirectResponse("/admin/settings?error=wrong_password", status_code=303)
    if new_password != confirm_password:
        return RedirectResponse("/admin/settings?error=mismatch", status_code=303)
    if len(new_password) < 6:
        return RedirectResponse("/admin/settings?error=too_short", status_code=303)

    set_setting(db, "admin_password", new_password)
    return RedirectResponse("/admin/settings?password_changed=1", status_code=303)


@router.get("/admin/appointments", response_class=HTMLResponse)
async def appointments_list(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    items = db.query(Appointment).order_by(Appointment.appointment_time.desc()).all()
    return templates.TemplateResponse("appointments.html", {"request": request, "items": items})


@router.post("/admin/appointments/{appt_id}/status")
async def update_appointment_status(
    appt_id: int,
    request: Request,
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    require_admin(request)
    appt = db.query(Appointment).filter(Appointment.id == appt_id).first()
    if appt:
        appt.status = status
        db.commit()
    return RedirectResponse("/admin/appointments", status_code=303)


@router.get("/admin/conversations", response_class=HTMLResponse)
async def conversations_list(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    items = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    return templates.TemplateResponse("conversations.html", {"request": request, "items": items})


@router.get("/admin/conversations/{conv_id}", response_class=HTMLResponse)
async def conversation_detail(conv_id: int, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(404)
    return templates.TemplateResponse("conversation_detail.html", {"request": request, "conv": conv})
