from azure_.blob_strage import upload_blob
from tools.gps import get_gps_coordinates
from datetime import datetime

task_dict = {
    "見回り": "patrol",
    "罠設置": "trap_set",
    "罠撤去": "trap_remove",
    "罠捕獲": "trap_cap",
    "銃捕獲": "gun_cap",
    "調査": "research",
    "他": "other",
}


def file_upload(uploaded_files, task_type):
    file_names = []
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    index = 0
    for uploaded_file in uploaded_files:
        gps_coordinates = get_gps_coordinates(uploaded_file.read())
        if gps_coordinates:
            lat, lon = gps_coordinates
            file_names.append(
                {"file_name": uploaded_file.name, "latitude": lat, "longitude": lon}
            )
        else:
            file_names.append(
                {
                    "file_name": uploaded_file.name,
                    "latitude": "位置情報なし",
                    "longitude": "位置情報なし",
                }
            )
        uploaded_file.seek(0)

        extension = uploaded_file.name.split(".")[-1]
        blob_name = f"{now}_{task_dict[task_type]}_{index}.{extension}"
        upload_blob(
            "",
            blob_name,
            uploaded_file,
        )
        index += 1
    return file_names


def file_upload_no_rename(uploaded_files, task_type):
    file_names = []
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    index = 0
    for uploaded_file in uploaded_files:
        gps_coordinates = get_gps_coordinates(uploaded_file.read())
        if gps_coordinates:
            lat, lon = gps_coordinates
            file_names.append(
                {"file_name": uploaded_file.name, "latitude": lat, "longitude": lon}
            )
        else:
            file_names.append(
                {
                    "file_name": uploaded_file.name,
                    "latitude": "位置情報なし",
                    "longitude": "位置情報なし",
                }
            )

        blob_name = uploaded_file.name
        upload_blob(
            "",
            blob_name,
            uploaded_file,
        )
        index += 1
    return file_names
