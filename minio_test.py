from minio import Minio
from minio.error import S3Error
from config_core import minio_client

import io
import os
client = Minio(
        "127.0.0.1:9000",
        access_key="test_user",
        secret_key="qweqwe123123",
        secure=False
    )
bucket_name = "cachephoto"
def save_file_to_minio(name_file : str, path_to_file : bytes):
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print("Bucket '{bucket}' already exists".format(bucket = bucket_name))
    iodata = io.BytesIO(path_to_file)
    #client.fput_object("asiatrip", name_file, path_to_file)
    client.put_object(bucket_name, name_file, iodata, len(path_to_file))
    print("Photo is successfully uploaded as object '{name}' to bucket '{bucket}'.".format(bucket = bucket_name, name=name_file))
    return 0

def load_file_from_minio(name_file : str):

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print("Bucket '{bucket}' already exists".format(bucket = bucket_name))
    print("start search")
    obj = client.get_object(bucket_name, name_file)

    return io.BytesIO(obj.data)

if __name__ == "__main__":
    try:
        #save_file_to_minio("rect354.png", "C:\\Users\\Lulz\\Desktop\\rect354.png")
        load_file_from_minio("6a034c7e-4383-4d95-8dc6-37bb8c0abc01.png")
        print(os.getenv("DB_USER"))
    except S3Error as exc:
        print("error occurred.", exc)