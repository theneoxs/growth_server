import sqlalchemy
from .users import user_table
from sqlalchemy.dialects.postgresql import UUID
import uuid

metadata = sqlalchemy.MetaData()

block_table = sqlalchemy.Table(
    "block",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100), unique = True),
    sqlalchemy.Column("type", sqlalchemy.Integer), #1 - главный блок, 2 - побочный блок. У одного главного родителя - один главный ребенок
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("level", sqlalchemy.String(3))
)

block_res_table = sqlalchemy.Table(
    "block_res",
    metadata,
    sqlalchemy.Column("block_id", sqlalchemy.ForeignKey("block.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("res_id", sqlalchemy.Integer),
    sqlalchemy.Column("source", sqlalchemy.Text)
)

tree_block_table = sqlalchemy.Table(
    "tree_block",
    metadata,
    sqlalchemy.Column("mother_id", sqlalchemy.ForeignKey("block.id", ondelete="CASCADE"), nullable=True),
    sqlalchemy.Column("child_id", sqlalchemy.ForeignKey("block.id", ondelete="CASCADE"))
)

status_block_table = sqlalchemy.Table(
    "status_block",
    metadata,
    sqlalchemy.Column("block_id", sqlalchemy.ForeignKey("block.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(user_table.c.id, ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("block_status", sqlalchemy.String(100), server_default = "0"),
    sqlalchemy.Column("is_favorite", sqlalchemy.Boolean(), server_default=sqlalchemy.sql.expression.false())
)
