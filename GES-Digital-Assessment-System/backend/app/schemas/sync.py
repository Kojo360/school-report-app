"""Schemas for offline-client synchronization."""

from typing import Any

from pydantic import BaseModel, Field


class SyncItem(BaseModel):
    """One locally queued create action from a teacher device."""

    local_id: int
    entity_type: str = Field(pattern="^(student|grade)$")
    action: str = Field(pattern="^CREATE$")
    payload: dict[str, Any]


class SyncRequest(BaseModel):
    items: list[SyncItem]


class SyncResult(BaseModel):
    local_id: int
    sync_status: str
    server_id: int | None = None
    error: str | None = None


class SyncResponse(BaseModel):
    items: list[SyncResult]
