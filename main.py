from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import databases
import config_core
from contextlib import asynccontextmanager
from src.models import blocks, programs, users
import sqlalchemy
from typing import List
import uuid
import minio_test

tags_metadata = [
    {
        "name": "Core",
        "description": "Основные функции, применимые на сервере",
    },
    {
        "name": "Users", 
        "description": "Функции работы с пользователем"
    },
    {
        "name": "Auth", 
        "description": "Функции работы при аутентификации пользователя"
    }
]

database = databases.Database(config_core.DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    title="GrowthApp",
    description="Здесь описан сервер приложения по передаче знаний между сотрудниками, для повышения осведомленности о текущих знаниях в компании",
    summary="Приложение для передачи знаний",
    version="0.1.1",
    contact={
        "name": "by Артем Макаров",
        "url": "https://t.me/theneoxs",
        "email": "tema.makarov2012@gmail.com",
    },
    license_info={"name": "Непубличная лицензия"},
    openapi_tags=tags_metadata,
    redoc_url=None,
    lifespan=lifespan,
)


@app.get("/", tags=["Core"])
async def start_screen():
    query = config_core.select_all_query.format(user_id='6b1d6361-ac2a-4a7c-a6af-0738057c2ed3')
    return await database.fetch_all(query)


@app.get("/get_all_schemes/{user_id}", tags=["Core"])
async def get_all_schemes(user_id):
    query = config_core.select_all_query.format(user_id=user_id)
    res = await database.fetch_all(query)
    mas = []
    for i in res:
        mas.append(i["id"])
    res2 = await get_admoder({"data" : mas})
    
    return {"data" : res, "users" : res2}


@app.get("/get_all_users/", tags=["Users"])
async def get_all_users():
    query = "select usr1.id user_id, concat(usr1.name, ' ', usr1.surname) user_name from public.user usr1"
    return await database.fetch_all(query)


@app.get("/get_user/{user_id}", tags=["Users"])
async def get_user_data(user_id):
    query = config_core.select_user_data.format(user_id=user_id)
    res = await database.fetch_all(query)
    res2 = await select_all_complete_scheme(user_id)
    return {"data" : res, "scheme" : res2}


@app.post("/get_admoder/", tags=["Users"])
async def get_admoder(program_ids: dict):
    prog_ids = ""
    for i in program_ids["data"]:
        prog_ids += str(i) + ","
    prog_ids = prog_ids[:-1]
    query = config_core.select_all_admoder_in_scheme.format(program_id=prog_ids)
    if prog_ids == "":
        return None
    res = await database.fetch_all(query)
    answer = {}
    for i in res:
        if i["program_id"] not in answer:
            answer[i["program_id"]] = {"admin": [], "moders": []}
        if i["role_id"] == 2:
            answer[i["program_id"]]["moders"].append(
                {"user_name": i["user_name"], "user_id": i["user_id"]}
            )
        if i["role_id"] == 3:
            answer[i["program_id"]]["admin"].append(
                {"user_name": i["user_name"], "user_id": i["user_id"]}
            )
    return answer


@app.post("/set_favorite_schema/", tags=["Users"])
async def set_fav_schema(data: dict):
    checked = await database.fetch_all(
        "select * from public.program_to_user WHERE program_id = {program_id} and user_id = '{user_id}';".format(
            program_id=data["data"]["prog_id"], user_id=data["data"]["user_id"]
        )
    )
    if checked == []:
        query = config_core.create_user_to_program.format(
            data="({program_id}, '{user_id}', {role_id})".format(
                program_id=data["data"]["prog_id"],
                user_id=data["data"]["user_id"],
                role_id=None,
            )
        )
        await database.fetch_all(query)
    query = config_core.set_favorite_schema.format(
        program_id=data["data"]["prog_id"],
        user_id=data["data"]["user_id"],
        is_favorite=data["data"]["is_favorite"],
    )
    res = await database.fetch_all(query)
    return res


@app.post("/set_favorite_block/", tags=["Core"])
async def set_fav_block(data: dict):
    checked = await database.fetch_all(
        "select * from public.status_block WHERE block_id = {block_id} and user_id = '{user_id}';".format(
            block_id=data["data"]["block_id"], user_id=data["data"]["user_id"]
        )
    )
    if checked == []:
        query = config_core.create_connect_block_to_user.format(
            data="({block_id}, '{user_id}')".format(
                block_id=data["data"]["block_id"], user_id=data["data"]["user_id"]
            )
        )
        await database.fetch_all(query)
    query = config_core.set_favorite_block.format(
        block_id=data["data"]["block_id"],
        user_id=data["data"]["user_id"],
        is_favorite=data["data"]["is_favorite"],
    )
    res = await database.fetch_all(query)
    return res


@app.post("/set_block_status/", tags=["Core"])
async def set_block_status(data: dict):
    checked = await database.fetch_all(
        "select * from public.status_block WHERE block_id = {block_id} and user_id = '{user_id}';".format(
            block_id=data["data"]["block_id"], user_id=data["data"]["user_id"]
        )
    )
    if checked == []:
        query = config_core.create_connect_block_to_user.format(
            data="({block_id}, '{user_id}')".format(
                block_id=data["data"]["block_id"], user_id=data["data"]["user_id"]
            )
        )
        await database.fetch_all(query)
    query = config_core.set_block_status.format(
        block_id=data["data"]["block_id"],
        user_id=data["data"]["user_id"],
        block_status=data["data"]["block_status"],
    )
    res = await database.fetch_all(query)
    return res


@app.post("/select_all_block_in_schema/", tags=["Core"])
async def get_block_in_schema(data: dict):
    query = config_core.select_all_block_in_schemes.format(
        program_id=data["data"]["prog_id"], user_id=data["data"]["user_id"]
    )
    res = await database.fetch_all(query)
    return res


@app.post("/create_schema/", tags=["Core"])
async def create_schema(data: dict):
    new_schema_id = ""
    new_block_id = ""
    try:
        add_schema = await database.fetch_all(
            config_core.create_scheme.format(
                name=data["name"],
                tag=data["tag"],
                info=data["info"],
                is_public=True if data["status"] == 2 else False,
                status=data["status"],
            )
        )
        
        checked = await database.fetch_all(
            "select id from public.program WHERE name = '{name}';".format(
                name=data["name"]
            )
        )
        new_schema_id = checked[0]["id"]
        await add_new_admoders(data, new_schema_id)
        new_block_id = await create_new_blocks(data, checked)
        return {"new_id" : new_schema_id}
    except BaseException as e:
        print(e)
        if new_schema_id != "":
            drop_schema = await database.fetch_all(
                "DELETE FROM public.program WHERE id={id}};".format(id=new_schema_id)
            )

        if new_block_id != "":
            drop_blocks = await database.fetch_all(
                "DELETE FROM public.block WHERE name in ({id})};".format(
                    id=new_block_id
                )
            )
        return e

async def add_new_admoders(data, new_schema_id):
    admin_add = ""
    moder_add = ""
    user_pattern = "({program_id}, UUID('{user_id}'), {role_id}),"
    user_pattern_check = "({program_id}, UUID('{user_id}')),"
    user_check_admin = ""
    user_check_moder = ""
    for i in data["admin"]:
        user_check_admin += user_pattern_check.format(program_id=new_schema_id, user_id=i["user_id"])
    user_check_admin = user_check_admin[:-1]
    for i in data["moders"]:
        user_check_moder += user_pattern_check.format(program_id=new_schema_id, user_id=i["user_id"])
    user_check_moder = user_check_moder[:-1]
    if len(data["admin"]) != 0:
        queue = "select * from public.program_to_user where (program_id, user_id) in ({data})".format(data=user_check_admin)
        check_admin = await database.fetch_all(queue)
        non_create_admin = []
        update_admin = ""
        for i in check_admin:
            update_admin += user_pattern.format(
                program_id=new_schema_id, user_id=i["user_id"], role_id=3
            )
            non_create_admin.append(i["user_id"])
        update_admin = update_admin[:-1]
        if update_admin != "":
            update_data_admin = await database.fetch_all(
                    config_core.update_user.format(data=update_admin)
                )
        for i in data["admin"]:
            if uuid.UUID(i["user_id"]) not in non_create_admin:
                admin_add += user_pattern.format(
                        program_id=new_schema_id, user_id=i["user_id"], role_id=3
                    )
        admin_add = admin_add[:-1]
        if admin_add != "":
            add_data_admin = await database.fetch_all(
                    config_core.create_user_to_program.format(data=admin_add)
                )
    if len(data["moders"]) != 0:
        queue = "select * from public.program_to_user where (program_id, user_id) in ({data})".format(data=user_check_moder)
        check_moder = await database.fetch_all(queue)
        non_create_moder = []
        update_moder = ""
        for i in check_moder:
            update_moder += user_pattern.format(
                program_id=new_schema_id, user_id=i["user_id"], role_id=2
            )
            non_create_moder.append(i["user_id"])
        update_moder = update_moder[:-1]
        if update_moder != "":
            update_data_moder = await database.fetch_all(
                    config_core.update_user.format(data=update_moder)
                )
        for i in data["moders"]:
            if uuid.UUID(i["user_id"]) not in non_create_moder:
                moder_add += user_pattern.format(
                        program_id=new_schema_id, user_id=i["user_id"], role_id=2
                    )
        moder_add = moder_add[:-1]
        if moder_add != "":
            add_data_moder = await database.fetch_all(
                    config_core.create_user_to_program.format(data=moder_add)
                )

async def create_new_blocks(data, checked):
    block_pattern = "('{name}', {type}, '{description}', '{level}'),"
    block_link_pattern = "({mother_id}, {child_id}),"
    block_program_pattern = "({program_id}, {block_id}),"
    block_list = ""
    block_link_list = ""
    block_to_find = {}
    later_id_block = {}
    for i in data["blocks"]:
        block_to_find[i["block_name"]] = i["block_rel"]
        later_id_block[i["block_id"]] = i["block_name"]
        block_list += block_pattern.format(
                name=i["block_name"],
                type=i["block_type"],
                description=i["block_data"],
                level=i["level"],
            )
    block_list = block_list[:-1]
    add_blocks = await database.fetch_all(
            config_core.create_blocks.format(data=block_list)
        )
        #TODO: Добавить обработчик ошибки на случай существования блока с таким названием
    block_to_program = ""
    block_checked = await database.fetch_all(
            "select id, name from public.block WHERE name in ({data});".format(
                data=",".join("'" + i + "'" for i in list(block_to_find.keys()))
            )
        )
    new_block_id = ",".join("'" + i + "'" for i in list(block_to_find.keys()))
    for i in block_checked:
        get_new_block_id = 0
        if block_to_find[i["name"]] != None and block_to_find[i["name"]] in later_id_block.keys():
            get_new_block_name = later_id_block[block_to_find[i["name"]]]
            for j in block_checked:
                if j["name"] == get_new_block_name:
                    get_new_block_id = j["id"]
                    break
        else:
            get_new_block_id = block_to_find[i["name"]]
        block_to_program += block_program_pattern.format(
                program_id=checked[0]["id"], block_id=i["id"]
            )
        block_link_list += block_link_pattern.format(
                mother_id=get_new_block_id
                if block_to_find[i["name"]] != None
                else "null",
                child_id=i["id"],
            )
    block_link_list = block_link_list[:-1]
    block_to_program = block_to_program[:-1]
    add_block_to_block = await database.fetch_all(
            config_core.create_connect_block_to_block.format(data=block_link_list)
        )
    add_block_to_program = await database.fetch_all(
            config_core.create_connect_blocks_to_program.format(data=block_to_program)
        )
    
    return new_block_id


@app.post("/select_all_favorite_block/", tags=["Core"])
async def select_all_favorite_block(data: dict):
    query = config_core.select_all_favorite_block.format(
        user_id=data["data"]["user_id"]
    )
    res = await database.fetch_all(query)
    return res

@app.post("/select_user_to_scheme/", tags=["Core"])
async def select_user_to_scheme(data: dict):
    query = config_core.select_all_user_complete_scheme.format(
        prog_id=data["data"]["prog_id"]
    )
    res = await database.fetch_all(query)
    return res

@app.get("/get_schema_from_block/{block_id}", tags=["Core"])
async def get_schema_from_block(block_id: int):
    query = "select program_id from public.program_list where block_id = {block_id};".format(
        block_id=block_id
    )
    res = await database.fetch_all(query)
    return res


@app.get("/select_all_complete_scheme/{user_id}", tags=["Core"])
async def select_all_complete_scheme(user_id):
    query = config_core.select_all_complete_scheme.format(user_id=user_id)
    res = await database.fetch_all(query)
    return res


@app.get("/select_all_favorite_scheme/{user_id}", tags=["Core"])
async def select_all_favorite_scheme(user_id):
    query = config_core.select_all_favorite_scheme.format(user_id=user_id)
    res = await database.fetch_all(query)
    mas = []
    for i in res:
        mas.append(i["id"])
    res2 = await get_admoder({"data" : mas})
    
    return {"data" : res, "users" : res2}


@app.post("/auth/", tags=["Auth"])
async def auth_user(data: dict):
    query = config_core.get_user_by_login.format(login=data["login"])
    res = await database.fetch_one(query)
    if res == None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if res["password"] == data["password"]:
        return {"detail": res["user_id"]}

    raise HTTPException(status_code=400, detail="Неверные данные, попробуйте еще раз")


@app.get("/select_all_branch/", tags=["Auth"])
async def select_all_branch():
    query = "SELECT * FROM public.branch"
    res = await database.fetch_all(query)
    return res


@app.post("/registration/", tags=["Auth"])
async def registration_user(data: dict):
    query = config_core.get_user_by_login.format(login=data["login"])
    res = await database.fetch_one(query)
    if res != None:
        raise HTTPException(status_code=406, detail="Такой логин уже занят")
    
    while True:
        new_guid = uuid.uuid4()
        query = "SELECT * FROM public.user where id = '{id}'".format(id=new_guid)
        res = await database.fetch_one(query)
        if res == None:
            query = config_core.create_user.format(
                id=new_guid,
                name=data["name"],
                surname=data["surname"],
                position=data["position"],
                role_id=data["role_id"],
                branch_id=data["branch_id"])
            res = await database.fetch_one(query)
            query = config_core.create_account.format(
                user_id=new_guid,
                login=data["login"],
                password=data["password"])
            res = await database.fetch_one(query)
            return {"new_login" : data["login"]}

@app.post("/select_scheme/", tags=["Core"])
async def select_scheme(data : dict):
    query = config_core.select_scheme.format(id=data["id"])
    res1 = await database.fetch_all(query)
    res2 = await get_admoder({"data": [data["id"]]})
    res3 = await get_block_in_schema({"data" : {"prog_id" : data["id"], "user_id" : data["user_id"]}})
    res1 = dict(res1[0])
    res1["admin"] = res2[data["id"]]["admin"]
    res1["moders"] = res2[data["id"]]["moders"]
    res1["role"] = 0
    res1["is_favourite"] = True
    res1["blocks"] = []
    for i in res3:
        res1["blocks"].append(dict(i))
    return res1

@app.post("/update_scheme/", tags=["Core"])
async def update_scheme(data : dict):
    queue = config_core.update_scheme.format(
        id=data["id"],
        name=data["name"],
        tag=data["tag"],
        image=data["image"] if data["image"] != "null" else "",
        description=data["info"],
        is_public=True if data["status"] == 2 else False,
        status=data["status"],
        )
    update_scheme = await database.fetch_all(queue)
    queue = "update public.program_to_user set role_id = 1 where program_id = {prog_id}".format(prog_id = data["id"])
    delete_role_scheme = await database.fetch_all(queue)
    add_new_adm = await add_new_admoders(data, data["id"])
    if len(data["updates"]["delete"]) != 0 or len(data["updates"]["create"]) != 0 or len(data["updates"]["update"]) != 0:
        if len(data["updates"]["delete"]) != 0:
            delete_ids = ",".join(list(map(str, data["updates"]["delete"])))
            query = "delete from public.block where id in ({id})".format(id=delete_ids)
            res1 = await database.fetch_all(query)

        create_data = []
        update_data = []

        block_pattern_upd = "({id}, '{name}', {type}, '{description}', '{level}'),"
        block_list_upd = ""

        update_rel_list = {}
        old_data = {}
        for i in data["blocks"]:
            if i["block_id"] in data["updates"]["create"]:
                create_data.append(i)
                update_rel_list[i["block_id"]] = i["block_name"]
            elif i["block_id"] in data["updates"]["update"]:
                update_data.append(i)
        
        if len(create_data) != 0:
            new_block_id = await create_new_blocks({"blocks" : create_data}, [{"id" : data["id"]}])
        
        for i in update_data:
            block_list_upd += block_pattern_upd.format(
                        id=i["block_id"],
                        name=i["block_name"],
                        type=i["block_type"],
                        description=i["block_data"],
                        level=i["level"],
                    )
            if i["block_rel"] in data["updates"]["create"]:
                for j in create_data:
                    if j["block_id"] == i["block_rel"]:
                        update_rel_list[j["block_id"]] = j["block_name"]
                        break
        
        if len(update_data) != 0:
            block_list_upd = block_list_upd[:-1]
            queue = config_core.update_blocks.format(data=block_list_upd)
            update_blocks = await database.fetch_all(queue)

        block_checked = []
        if len(update_rel_list.keys()) != 0:
            block_checked = await database.fetch_all(
                "select id, name from public.block WHERE name in ({data});".format(
                    data=",".join("'" + i + "'" for i in list(update_rel_list.values()))
                )
            )
        queue = config_core.delete_connect_blocks.format(prog_id=data["id"])
        res2 = await database.fetch_all(queue)
        block_link_pattern = "({mother_id}, {child_id}),"
        for i in update_rel_list:
            for j in block_checked:
                if update_rel_list[i] == j["name"]:
                    update_rel_list[i] = j["id"]
                    break
        for i in block_checked:
            for j in data["blocks"]:
                if j["block_name"] == i["name"]:
                    j["block_id"] = i["id"]
                    break
        block_link_list = ""
        for i in data["blocks"]:
            if i["block_rel"] in update_rel_list.keys():
                i["block_rel"] = update_rel_list[i["block_rel"]]
            block_link_list += block_link_pattern.format(
                    mother_id=i["block_rel"] 
                    if i["block_rel"] != None
                    else "null",
                    child_id=i["block_id"],
                )
        block_link_list = block_link_list[:-1]
        add_block_to_block = await database.fetch_all(
                config_core.create_connect_block_to_block.format(data=block_link_list)
            )
    
    return {"new_id" : data["id"]}

@app.post("/select_all_user_data/", tags=["Users"])
async def select_all_user_data(data : dict):
    query = "SELECT * FROM public.user usr1 left join public.auth_data usr2 on usr1.id = usr2.user_id"
    res = await database.fetch_all(query)
    res2 = await select_all_branch()
    query = "select * from public.role"
    res3 = await database.fetch_all(query)
    result = {"user" : [], "branch" : [], "role" : []}
    if data["is_user"] == True:
        result["user"] = res
    if data["is_branch"] == True:
        result["branch"] = res2
    if data["is_role"] == True:
        result["role"] = res3
    return result

@app.post("/change_user/", tags=["Users"])
async def change_user(data : dict):
    query = "update public.user set name='{name}', surname='{surname}', position='{position}', role_id={role_id}, branch_id={branch_id} where id='{id}'".format(
        id=data["id"],
        name=data["name"],
        surname=data["surname"],
        position=data["position"],
        role_id=data["role_id"],
        branch_id=data["branch_id"]
    )
    res = await database.fetch_all(query)
    query = "update public.auth_data set login='{login}', password='{password}' where user_id='{id}'".format(
        id=data["id"],
        login=data["login"],
        password=data["password"]
    )
    res = await database.fetch_all(query)
    return True

@app.post("/check_create_blocks/", tags=["Core"])
async def check_create_blocks(data : dict):
    pattern_queue = "'{name}',"
    new_blocks = ""
    for i in data["name"]:
        new_blocks += pattern_queue.format(name = i)
    new_blocks = new_blocks[:-1]
    query = "select * from public.block where name in ({data})".format(
        data = new_blocks
    )
    print(query)
    res = await database.fetch_all(query)
    if len(res) != 0:
        print("Есть такие")
        err_pattern = """- {name}
"""
        err_text = """Измените названия следующих блоков: 
"""
        for i in res:
            err_text += err_pattern.format(name=i["name"])
        raise HTTPException(status_code=418, detail=err_text)
    return True

@app.post("/load_picture/", tags=["Core"])
async def load_picture(data : dict):
    new_name = str(uuid.uuid4()) + ".png"
    print(new_name)
    res = minio_test.save_file_to_minio(new_name, bytes(data["data"]))
    if res == 0:
        return {"type" : "save", "new_name" : new_name}
    return False

@app.post("/download_picture/", tags=["Core"])
async def download_picture(data : dict):
    res = minio_test.load_file_from_minio(data["name"])
    #print(str(res))
    return StreamingResponse(content=res, status_code=206, media_type="image/png")