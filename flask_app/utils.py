from datetime import datetime
import io 
import base64
from .models import User


def current_time() -> datetime:
    return datetime.now()


def get_b64_img(username):     
    user = User.objects(username=username).first()     
    bytes_im = io.BytesIO(user.profile_pic.read())     
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

