from typing import List, Optional
from sqlmodel import select
from app.models import Device, User


def get_device_by_device_id(session, device_id: str) -> Optional[Device]:
    statement = select(Device).where(Device.device_id == device_id)
    return session.exec(statement).first()


def list_devices(session) -> List[str]:
    statement = select(Device.device_id)
    return [r[0] for r in session.exec(statement).all()]


def create_device(session, device: Device) -> Device:
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


def update_device(session, existing: Device, new_data: dict) -> Device:
    for k, v in new_data.items():
        # map incoming schema key 'metadata' to the model attribute 'metadata_'
        if k == "metadata":
            setattr(existing, "metadata_", v)
            continue
        if hasattr(existing, k):
            setattr(existing, k, v)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


def delete_device(session, device: Device) -> None:
    session.delete(device)
    session.commit()


# Users


def get_user_by_username(session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def create_user(session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def list_users(session):
    statement = select(User.id, User.username, User.is_admin)
    return [
        dict(id=r[0], username=r[1], is_admin=bool(r[2]))
        for r in session.exec(statement).all()
    ]


def delete_user(session, user: User):
    session.delete(user)
    session.commit()


def device_to_dict(device: Device) -> dict:
    """
    Serialize a Device SQLModel instance to a dict matching DeviceRead schema.
    """
    return {
        "device_id": device.device_id,
        "name": device.name,
        "location": device.location,
        "model": device.model,
        "last_seen": device.last_seen,
        "metadata": getattr(device, "metadata_", None) or {},
    }
