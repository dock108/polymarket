from sqlalchemy import Column, DateTime, Integer, String, JSON, Float, Text, Index, func

from app.db.base import Base


class APICallLog(Base):
    __tablename__ = "api_call_log"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    service = Column(String(50), nullable=False)  # e.g., polymarket, odds_api, datagolf
    endpoint = Column(String(255), nullable=False)
    request_method = Column(String(10), nullable=False)

    status_code = Column(Integer, nullable=True)
    duration_ms = Column(Float, nullable=True)

    error = Column(Text, nullable=True)
    meta = Column(JSON, nullable=True)

    __table_args__ = (
        Index("ix_api_call_log_service_created", "service", "created_at"),
        Index("ix_api_call_log_status_created", "status_code", "created_at"),
    )
