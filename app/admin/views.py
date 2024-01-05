from sqladmin import ModelView
from app.models.camera import Camera
from app.models.zone import Zone


class CameraAdmin(ModelView, model=Camera):
    column_list = [Camera.id, 
                   Camera.address,
                   Camera.cam_url,
                   Camera.registered_at,
                   Camera.zones
                   ]
    name = "Камера"
    name_plural = "Камеры"
    icon = "fa-solid fa-camera"

    

class ZoneAdmin(ModelView, model=Zone):
    # column_list = [Zone.id, 
    #                Zone.internal_id,
    #                Zone.camera_id,
    #                Zone.long,
    #                Zone.lat,
    #                Zone.status,
    #                Zone.camera
    #                ]
    column_list = "__all__"
    name = "Зона"
    name_plural = "Зоны"
    icon = "fa-solid fa-parking"