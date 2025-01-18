import re
from modules.utiles.scripts.transform import transform_datetime
from modules.utiles.scripts.shorts import is_short_video

class YouTubeResponseHandler:
    @staticmethod
    def parse_response(api_name, response):
        """API 이름에 따라 응답 처리"""
        parsers = {
            "channels.list": YouTubeResponseHandler._parse_channel_information,
            "videos.list": YouTubeResponseHandler._parse_video_statistics,
            "commentThreads.list": YouTubeResponseHandler._parse_comments,
            "search.list": YouTubeResponseHandler._parse_channel_id_by_name,
            "search.Idlist": YouTubeResponseHandler._parse_video_Ids
        }
        parser = parsers.get(api_name)
        if not parser:
            raise ValueError(f"Unsupported API: {api_name}")
        return parser(response)
    
    @staticmethod
    def _parse_channel_id_by_name(response):
        """채널 이름으로 채널 ID를 가져오는 함수"""
        if response['items']:
            # 검색 결과에서 채널 ID와 이름 추출
            channel_info = response['items'][0]
            channel_id = channel_info['id']['channelId']
            return channel_id
        else:
            return None

    @staticmethod
    def _parse_channel_information(response):
        """채널 정보 응답 처리"""
        channel_info = response["items"][0]
        return {
            "title": channel_info["snippet"]["title"],
            "channel_id": channel_info["id"],
            "thumbnail": channel_info["snippet"]["thumbnails"]["high"]["url"],
            "description": channel_info["snippet"]["description"],
            "subscriber_count": int(channel_info["statistics"]["subscriberCount"]),
            "video_count": int(channel_info["statistics"]["videoCount"]),
            "views_count": int(channel_info["statistics"]["viewCount"]),
        }
        
    @staticmethod
    def _parse_comments(response):
        """댓글 응답 처리"""
        comments = []
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": snippet["authorDisplayName"],
                "text": re.sub(r'<.*?>', '', snippet["textDisplay"]),
                "like_count": snippet["likeCount"],
                "publish_time": snippet["publishedAt"],
            })
        return comments

        
    @staticmethod
    def _parse_video_statistics(response):
        """비디오 통계 응답 처리"""
        for item in response["items"]:
            duration = item["contentDetails"]["duration"]
            publish_time = transform_datetime(item['snippet']['publishedAt'])  # 업로드 날짜 추가
            is_short = is_short_video(duration)
            return {
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "view_count": int(item["statistics"].get("viewCount", 0)),
                "like_count": int(item["statistics"].get("likeCount", 0)),
                "comment_count": int(item["statistics"].get("commentCount", 0)),
                "publish_time": publish_time,
                "is_shorts": is_short
            }
    
    @staticmethod
    def _parse_video_Ids(response):
        # response 검증
        if response is None:
            print("[ERROR] Response is None.")
            return []

        if 'items' not in response:
            print("[ERROR] 'items' key is missing in the response.")
            return []

        video_data = []
        for item in response['items']:
            # 유효한 YouTube 비디오인지 확인
            if item.get('id', {}).get('kind') == "youtube#video":
                video_id = item['id'].get('videoId')
                published_time = transform_datetime(item['snippet'].get('publishedAt'))
                video_data.append({
                    "video_id": video_id,
                    "publish_time": published_time
                })

        if not video_data:
            print("[WARNING] No valid video IDs found in the response.")
        
        return video_data




