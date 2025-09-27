"""core tables for logs and snapshots

Revision ID: 0002
Revises: 0001
Create Date: 2025-09-26

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "api_call_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("service", sa.String(length=50), nullable=False),
        sa.Column("endpoint", sa.String(length=255), nullable=False),
        sa.Column("request_method", sa.String(length=10), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
    )
    op.create_index(
        "ix_api_call_log_service_created", "api_call_log", ["service", "created_at"]
    )
    op.create_index(
        "ix_api_call_log_status_created", "api_call_log", ["status_code", "created_at"]
    )

    op.create_table(
        "odds_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("sport", sa.String(length=50), nullable=False),
        sa.Column("event_id", sa.String(length=100), nullable=False),
        sa.Column("bookmaker", sa.String(length=50), nullable=False),
        sa.Column("market_type", sa.String(length=50), nullable=False),
        sa.Column("side", sa.String(length=50), nullable=False),
        sa.Column("raw_odds", sa.JSON(), nullable=True),
        sa.Column("normalized", sa.JSON(), nullable=True),
    )
    op.create_index(
        "ix_odds_log_event_bookmaker_created",
        "odds_log",
        ["event_id", "bookmaker", "created_at"],
    )
    op.create_index("ix_odds_log_sport_created", "odds_log", ["sport", "created_at"])

    op.create_table(
        "market_snapshot",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "captured_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("sport", sa.String(length=50), nullable=True),
        sa.Column("event_id", sa.String(length=100), nullable=True),
        sa.Column("market", sa.String(length=100), nullable=True),
        sa.Column("snapshot", sa.JSON(), nullable=False),
    )
    op.create_index(
        "ix_market_snapshot_source_captured",
        "market_snapshot",
        ["source", "captured_at"],
    )
    op.create_index(
        "ix_market_snapshot_event_captured",
        "market_snapshot",
        ["event_id", "captured_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_market_snapshot_event_captured", table_name="market_snapshot")
    op.drop_index("ix_market_snapshot_source_captured", table_name="market_snapshot")
    op.drop_table("market_snapshot")

    op.drop_index("ix_odds_log_sport_created", table_name="odds_log")
    op.drop_index("ix_odds_log_event_bookmaker_created", table_name="odds_log")
    op.drop_table("odds_log")

    op.drop_index("ix_api_call_log_status_created", table_name="api_call_log")
    op.drop_index("ix_api_call_log_service_created", table_name="api_call_log")
    op.drop_table("api_call_log")
