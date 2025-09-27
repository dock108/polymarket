from sqlalchemy import Column, DateTime, Integer, String, JSON, Float, Index, func

from app.db.base import Base


class OddsLog(Base):
    __tablename__ = "odds_log"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    sport = Column(String(50), nullable=False)
    event_id = Column(String(100), nullable=False)
    bookmaker = Column(String(50), nullable=False)

    market_type = Column(String(50), nullable=False)  # h2h, spreads, totals, outrights
    side = Column(String(50), nullable=False)  # team/player/yes/no identifier

    raw_odds = Column(JSON, nullable=True)  # original payload fragment
    normalized = Column(JSON, nullable=True)  # fair odds/probs after processing

    __table_args__ = (
        Index(
            "ix_odds_log_event_bookmaker_created", "event_id", "bookmaker", "created_at"
        ),
        Index("ix_odds_log_sport_created", "sport", "created_at"),
    )
