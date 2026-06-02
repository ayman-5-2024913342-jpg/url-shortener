import base64
import hashlib
from database import add_url, check_collision_long_url, check_collision_short_url, get_long_url, get_short_url

def shortner(url: str):
    # প্রথমে চেক করি লং ইউআরএলটি অলরেডি ডাটাবেজে আছে কিনা
    # (ধরে নিচ্ছি check_collision_long_url এখন শুধু True/False রিটার্ন করে)
    is_existed = check_collision_long_url(url)
    
    if not is_existed:
        # ১. ইউআরএল হ্যাশ করা
        hashed = hashlib.sha256(url.encode('utf-8')).hexdigest()
        
        # ২. প্রথম ৪ ক্যারেক্টার নিয়ে Base64 এনকোড করা এবং স্ট্রিং-এ রূপান্তর
        data_bytes = hashed[:4].encode("utf-8")
        short_url = base64.urlsafe_b64encode(data_bytes).decode("utf-8")
        
        # ৩. শর্ট ইউআরএল-এর কলিশন চেক করা
        if not check_collision_short_url(short_url):

            add_url((url, short_url)) # ডাটাবেজে সেভ করার ফাংশন
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
        # যদি ইউআরএল আগেই থাকে, তবে ডাটাবেজ থেকে আগের শর্ট ইউআরএলটি তুলে আনা উচিত
        # এখানে উদাহরণ হিসেবে দেখানোর জন্য static_short_url বা fetch logic বসাতে পারেন
        # আপাতত বোঝার সুবিধার্থে ডাটাবেজ থেকে তুলে আনার লজিক না থাকলে None বা "Already Exists" দেওয়া হলো
        short_url = get_short_url(url)
        msg = {
            "long url" : url,
            "short url" : short_url, 
            "message" : "Url already existed in database!"
        }

    return msg
