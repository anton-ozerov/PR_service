"""seeding users

Revision ID: f875b4b264da
Revises: 30cccf3bdeb7
Create Date: 2025-11-16 12:04:54.731490

"""
import uuid
from typing import Sequence, Union

from alembic import op
from sqlalchemy import column, table, String, Boolean

from app.core.config.config import ADMIN_AUTO_CREATED_PASSWORD
from app.core.security import PasswordUtils
from app.enums import UserRoleEnum

# revision identifiers, used by Alembic.
revision: str = 'f875b4b264da'
down_revision: Union[str, Sequence[str], None] = '30cccf3bdeb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Определение структуры таблицы для сидинга
users_table = table(
    'user',
    column('id', String),
    column('username', String),
    column('hashed_password', String),
    column('role', String),
    column("is_active", Boolean),
    column("team_id", String),
)
teams_table = table(
    "team",
    column("id", String),
    column("name", String),
)


def upgrade() -> None:
    """Upgrade schema."""
    teams = [
        {
            "id": uuid.uuid4(),
            'name': 'First',
        },
        {
            "id": uuid.uuid4(),
            'name': 'Second',
        },
        {
            "id": uuid.uuid4(),
            'name': 'Third',
        }
    ]
    op.bulk_insert(teams_table, teams)

    users = [
        {
            "id": uuid.uuid4(),
            'username': 'admin',
            'hashed_password': PasswordUtils.hash_password(ADMIN_AUTO_CREATED_PASSWORD)[0],
            'role': UserRoleEnum.ADMIN.value,
            "is_active": True,
            "team_id": teams[0]["id"],
        },
        {
            "id": uuid.uuid4(),
            'username': 'user1',
            'hashed_password': PasswordUtils.hash_password('userpass')[0],
            'role': UserRoleEnum.USER.value,
            "is_active": True,
            "team_id": teams[0]["id"],
        },
        {
            "id": uuid.uuid4(),
            'username': 'user2',
            'hashed_password': PasswordUtils.hash_password('userpass')[0],
            'role': UserRoleEnum.USER.value,
            "is_active": True,
            "team_id": teams[0]["id"],
        },
        {
            "id": uuid.uuid4(),
            'username': 'user3',
            'hashed_password': PasswordUtils.hash_password('userpass')[0],
            'role': UserRoleEnum.USER.value,
            "is_active": True,
            "team_id": teams[1]["id"],
        },
    ]
    op.bulk_insert(users_table, users)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM \"user\" WHERE username IN ('admin', 'user1', 'user2', 'user3')")
    op.execute("DELETE FROM \"team\" WHERE name IN ('First', 'Second', 'Third')")
