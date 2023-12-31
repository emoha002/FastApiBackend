"""added the event table

Revision ID: c0b5f1a6999c
Revises: 4f7e641b6e55
Create Date: 2023-10-31 23:06:00.606424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0b5f1a6999c"
down_revision = "4f7e641b6e55"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "calendar_event",
        sa.Column("event_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("event_name", sa.String(length=200), nullable=False),
        sa.Column("course_number", sa.String(length=200), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_index(
        op.f("ix_calendar_event_event_id"), "calendar_event", ["event_id"], unique=True
    )
    op.create_table(
        "event_occurrence",
        sa.Column("occurrence_id", sa.UUID(), nullable=False),
        sa.Column("event_id", sa.UUID(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["calendar_event.event_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("occurrence_id"),
    )
    op.create_index(
        op.f("ix_event_occurrence_occurrence_id"),
        "event_occurrence",
        ["occurrence_id"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_event_occurrence_occurrence_id"), table_name="event_occurrence"
    )
    op.drop_table("event_occurrence")
    op.drop_index(op.f("ix_calendar_event_event_id"), table_name="calendar_event")
    op.drop_table("calendar_event")
    # ### end Alembic commands ###
