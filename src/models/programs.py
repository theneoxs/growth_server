import sqlalchemy
from .users import user_table, role_table
from .blocks import block_table
from sqlalchemy.dialects.postgresql import UUID
import uuid

metadata = sqlalchemy.MetaData()

program_table = sqlalchemy.Table(
    "program",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(200), unique = True),
    sqlalchemy.Column("image", sqlalchemy.Text),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("tag", sqlalchemy.String(100)),
    sqlalchemy.Column("is_public", sqlalchemy.Boolean(), server_default=sqlalchemy.sql.expression.true()),
    sqlalchemy.Column("status", sqlalchemy.String(100))
)

program_list_table = sqlalchemy.Table(
    "program_list",
    metadata,
    sqlalchemy.Column("program_id", sqlalchemy.ForeignKey("program.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("block_id", sqlalchemy.ForeignKey(block_table.c.id, ondelete="CASCADE"), primary_key=True)
)

program_to_user_table = sqlalchemy.Table(
    "program_to_user",
    metadata,
    sqlalchemy.Column("program_id", sqlalchemy.ForeignKey("program.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(user_table.c.id, ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("role_id", sqlalchemy.ForeignKey(role_table.c.id, ondelete="SET NULL")),
    sqlalchemy.Column("is_favorite", sqlalchemy.Boolean(), server_default=sqlalchemy.sql.expression.false())
)
