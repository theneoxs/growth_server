import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "user",
    metadata,
    #sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique = True),
    sqlalchemy.Column("id", UUID(True), primary_key=True, default=uuid.uuid4),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("surname", sqlalchemy.String(100)),
    sqlalchemy.Column("position", sqlalchemy.String(100)),
    sqlalchemy.Column("role_id", sqlalchemy.ForeignKey("role.id", ondelete="SET NULL")),
    sqlalchemy.Column("branch_id", sqlalchemy.ForeignKey("branch.id", ondelete="SET NULL"))
)

login_user_table = sqlalchemy.Table(
    "auth_data",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("user.id", ondelete="CASCADE")),
    sqlalchemy.Column("login", sqlalchemy.String(100), unique = True),
    sqlalchemy.Column("password", sqlalchemy.String(100))
)

branch_table = sqlalchemy.Table(
    "branch",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100))
)

role_table = sqlalchemy.Table(
    "role",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100))
)
