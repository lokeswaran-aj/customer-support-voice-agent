import uuid
from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from livekit import api
from livekit.api.access_token import ParseDict
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.settings import settings

app = FastAPI(
    title="Customer Support Voice Agent Server",
    description="A server for the Customer Support Voice Agent",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.get("/health")
async def health():
    return {"status": "ok"}


class TokenRequest(BaseModel):
    room_name: Optional[str] = None
    participant_identity: Optional[str] = None
    participant_name: Optional[str] = None
    participant_metadata: Optional[str] = None
    participant_attributes: Optional[Dict[str, str]] = None
    room_config: Optional[dict] = None


@app.post("/api/v1/token", status_code=201)
async def generate_token(request: TokenRequest):
    try:
        api_key = settings.api_key
        api_secret = settings.api_secret
        server_url = settings.server_url

        room_name = request.room_name or f"room_name_{uuid.uuid4().hex[:8]}"
        participant_identity = (
            request.participant_identity or f"participant_id_{uuid.uuid4().hex[:8]}"
        )
        participant_name = (
            request.participant_name or f"participant_{uuid.uuid4().hex[:8]}"
        )

        token = (
            api.AccessToken(api_key, api_secret)
            .with_identity(participant_identity)
            .with_name(participant_name)
            .with_grants(
                api.VideoGrants(
                    room_join=True, room=room_name, can_publish=True, can_subscribe=True
                )
            )
        )

        if request.participant_metadata:
            token = token.with_metadata(request.participant_metadata)
        if request.participant_attributes:
            token = token.with_attributes(request.participant_attributes)
        if request.room_config:
            token = token.with_room_config(
                ParseDict(request.room_config, api.RoomConfiguration())
            )

        participant_token = token.to_jwt()
        return JSONResponse(
            status_code=201,
            content={"participant_token": participant_token, "server_url": server_url},
        )
    except Exception as e:
        print(f"Error in generating token: {e}")
        return JSONResponse(
            status_code=500, content={"detail": "Failed to generate token"}
        )
