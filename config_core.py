from dotenv import load_dotenv
from minio import Minio

import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

DATABASE_URL = os.environ["DATABASE_URL"]

BUCKET_ACCESS_TOKEN = os.environ["BUCKET_ACCESS_TOKEN"]
BUCKET_SECRET_KEY = os.environ["BUCKET_SECRET_KEY"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
MINIO_HOST = os.environ["MINIO_HOST"]
MINIO_HOST_SECURE = os.environ["MINIO_HOST_SECURE"]

minio_client = Minio(
    endpoint = os.environ["MINIO_HOST"],
    access_key = os.environ["BUCKET_ACCESS_TOKEN"],
    secret_key = os.environ["BUCKET_SECRET_KEY"],
    secure = os.environ["MINIO_HOST_SECURE"],
)

bucket_name = os.environ["BUCKET_NAME"]

select_all_query = ""
with open("queue/select_all_schemes.sql", 'r') as command_data:
        select_all_query = command_data.read()

select_user_data = ""
with open("queue/select_user_data.sql", 'r') as command_data:
        select_user_data = command_data.read()

select_all_people_with_role_in_program = ""
with open("queue/select_all_people_with_role_in_program.sql", 'r') as command_data:
        select_all_people_with_role_in_program = command_data.read()

select_all_block_in_schemes = ""
with open("queue/select_all_block_in_schemes.sql", 'r') as command_data:
        select_all_block_in_schemes = command_data.read()

select_all_admoder_in_scheme = ""
with open("queue/select_all_admoder_in_scheme.sql", 'r') as command_data:
        select_all_admoder_in_scheme = command_data.read()

set_favorite_schema = ""
with open("queue/set_favorite_schema.sql", 'r') as command_data:
        set_favorite_schema = command_data.read()

set_favorite_block = ""
with open("queue/set_favorite_block.sql", 'r') as command_data:
        set_favorite_block = command_data.read()

set_block_status = ""
with open("queue/set_block_status.sql", 'r') as command_data:
        set_block_status = command_data.read()

create_user_to_program = ""
with open("queue/create_user_to_program.sql", 'r') as command_data:
        create_user_to_program = command_data.read()

create_connect_block_to_user = ""
with open("queue/create_connect_block_to_user.sql", 'r') as command_data:
        create_connect_block_to_user = command_data.read()

create_scheme = ""
with open("queue/create_scheme.sql", 'r') as command_data:
        create_scheme = command_data.read()

create_blocks = ""
with open("queue/create_blocks.sql", 'r') as command_data:
        create_blocks = command_data.read()

create_connect_block_to_block = ""
with open("queue/create_connect_block_to_block.sql", 'r') as command_data:
        create_connect_block_to_block = command_data.read()

create_connect_blocks_to_program = ""
with open("queue/create_connect_blocks_to_program.sql", 'r') as command_data:
        create_connect_blocks_to_program = command_data.read()

select_all_favorite_block = ""
with open("queue/select_all_favorite_block.sql", 'r') as command_data:
        select_all_favorite_block = command_data.read()

select_all_favorite_scheme = ""
with open("queue/select_all_favorite_scheme.sql", 'r') as command_data:
        select_all_favorite_scheme = command_data.read()

select_all_complete_scheme = ""
with open("queue/select_all_complete_scheme.sql", 'r') as command_data:
        select_all_complete_scheme = command_data.read()

get_user_by_login = ""
with open("queue/get_user_by_login.sql", 'r') as command_data:
        get_user_by_login = command_data.read()

create_user = ""
with open("queue/create_user.sql", 'r') as command_data:
        create_user = command_data.read()

create_account = ""
with open("queue/create_account.sql", 'r') as command_data:
        create_account = command_data.read()

select_all_user_complete_scheme = ""
with open("queue/select_all_user_complete_scheme.sql", 'r') as command_data:
        select_all_user_complete_scheme = command_data.read()

select_scheme = ""
with open("queue/select_scheme.sql", 'r') as command_data:
        select_scheme = command_data.read()

update_blocks = ""
with open("queue/update_blocks.sql", 'r') as command_data:
        update_blocks = command_data.read()

delete_connect_blocks = ""
with open("queue/delete_connect_blocks.sql", 'r') as command_data:
        delete_connect_blocks = command_data.read()

update_scheme = ""
with open("queue/update_scheme.sql", 'r') as command_data:
        update_scheme = command_data.read()

update_user = ""
with open("queue/update_user.sql", 'r') as command_data:
        update_user = command_data.read()