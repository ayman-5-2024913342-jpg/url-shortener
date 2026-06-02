import base64
import hashlib
from database import add_url, check_collision_long_url, check_collision_short_url, get_long_url, get_short_url

def shortner(url: str):
    is_existed = check_collision_long_url(url)
    
    if not is_existed:
        hashed = hashlib.sha256(url.encode('utf-8')).hexdigest()
        
        data_bytes = hashed[:4].encode("utf-8")
        short_url = base64.urlsafe_b64encode(data_bytes).decode("utf-8")
        
        if not check_collision_short_url(short_url):

            add_url((url, short_url)) 
            msg = {
                "long url" : url,
                "short url" : short_url,
                "message" : "Url has been added to database!"
            }
        else:
            msg = {
                "long url" : url,
                "short url" : None,
                "message" : "COLLISION! Url could not be added to database!"
            }   
    else:
        result = get_short_url(url)
        short_url = result[0]
        msg = {
            "long url" : url,
            "short url" : short_url, 
            "message" : "Url already existed in database!"
        }

    return msg
