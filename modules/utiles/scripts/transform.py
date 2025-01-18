from datetime import datetime
from datetime import timedelta

def get_url(text):
    if "우정잉" in text:
        return "/friendshiping"
    elif "유수현" in text:
        return "/suhyeon"
    elif "보겸" in text:
        return "/bokyem"
    elif "럽미" in text:
        return "/loveme"
    elif "지식줄고양" in text:
        return "/cat"
        
def transform_datetime(publish_time):
    publish_time = datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
    publish_time += timedelta(hours=9)
    return publish_time