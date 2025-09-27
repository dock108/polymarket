from sqlalchemy import Column, DateTime, Integer, String, JSON, Float, Index, func

from app.db.base import Base


class MarketSnapshot(Base):
    __tablename__ = "market_snapshot"

    id = Column(Integer, primary_key=True, index=True)
    captured_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    source = Column(String(50), nullable=False)  # polymarket, odds_api, datagolf
    sport = Column(String(50), nullable=True)
    event_id = Column(String(100), nullable=True)
    market = Column(String(100), nullable=True)  # market identifier/type

    snapshot = Column(JSON, nullable=False)  # full normalized snapshot

    __table_args__ = (
        Index("ix_market_snapshot_source_captured", "source", "captured_at"),
        Index("ix_market_snapshot_event_captured", "event_id", "captured_at"),
    )
