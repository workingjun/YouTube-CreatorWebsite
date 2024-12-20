from modules.youtube import YouTubeManager
import math 
from datetime import datetime

class HtmlManager:
    PATH1 = "youtube_data/template.html"
    PATH2 = "youtube_data/transfer_files/index.html"
    PATH3 = "youtube_data/transfer_files/comments_data.json"
    
    def __init__(self, youtube_manager: YouTubeManager):
        self.youtube_manager = youtube_manager
        
    def load_template(self):
        with open(self.PATH1, "r", encoding="utf-8") as file:
            template = file.read()
            template = template.replace("{", "{{").replace("}", "}}")
            template = template.replace("{{channel_name}}", "{channel_name}")
            template = template.replace("{{channelID}}", "{channelID}")
            template = template.replace("{{subscriber_count}}", "{subscriber_count}")
            template = template.replace("{{video_cards}}", "{video_cards}")
            template = template.replace("{{last_video_cards}}", "{last_video_cards}")
            template = template.replace("{{thumbnail}}", "{thumbnail}")
            template = template.replace("{{subscriber_count}}", "{subscriber_count}")
            template = template.replace("{{description}}", "{description}")
            template = template.replace("{{video_count}}", "{video_count}")
            template = template.replace("{{views_count}}", "{views_count}")
            return template

    def save_index_to_file(self):
        # 데이터 수집
        df_videos = self.youtube_manager.collect_data()
        last_video_cards = self.make_video_card(df_videos, hidden=False)
        video_cards = self.make_video_card(df_videos, start=5, stop=-1)
        result = self.youtube_manager.ChannelInformation()
        subscriber_count = format(result['subscriber_count'], ",")
        video_count = format(int(result['video_count']), ",")
        views_count = format(int(result['views_count']), ",")

        self.template = self.load_template()
        html_output = self.template.format(
            channel_name=result['title'],
            channelID=result['channelID'],
            thumbnail=result['thumbnail'],
            description=result['description'],
            video_count=video_count,
            views_count=views_count,
            subscriber_count=subscriber_count,
            last_video_cards=last_video_cards,
            video_cards=video_cards
            )
        with open(self.PATH2, "w", encoding="utf-8") as file:
            file.write(html_output)
    
    def make_video_card(self, df_videos, start=0, stop=5, hidden=True):
        # 좋아요 대비 조회수 비율 계산    
        df_videos['like_view_ratio'] = df_videos['like_count'] / df_videos['view_count']

        video_cards = ""
        for _, row in df_videos[start:stop].iterrows():
            publish_time = row['publish_time'].replace("T", " ").replace("Z", "")
            publish_time_list=list(publish_time)
            previous_time = ''.join(publish_time_list[11:13])
            plus_time = int(previous_time) + 9
            publish_time_list[11:13] = str(plus_time)
            publish_time = "".join(publish_time_list)
            view_count = format(row['view_count'], ",")
            like_count = format(row['like_count'], ",")
            comment_count = format(row['comment_count'], ",")

            given_time = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            time_difference = current_time - given_time
            elapsed_hours = time_difference.total_seconds() / 3600  # 초를 시간으로 변환
            Engagement_Rate = (row['comment_count'] + row['like_count']) / row['view_count']
            half_life = 24*30  # 7일(168시간)을 반감기로 설정
            trand_point = Engagement_Rate * math.exp(-elapsed_hours / half_life)

            hidden_text = ""
            if hidden:
                hidden_text = "video-card hidden"
            else:
                hidden_text = "video-card-info"

            video_cards += f"""
            <div class="{hidden_text}" 
                data-date="{publish_time}" 
                data-comments="{row['comment_count']}"
                data-views="{row['view_count']}"
                data-likes="{row['like_count']}"
                data-trand="{trand_point}"
                data-video-id="{row['video_id']}"
                data-is-shorts="{row['is_shorts']}">
                <div class="thumbnail-container">
                    <img src="https://i.ytimg.com/vi/{row['video_id']}/hqdefault.jpg" 
                        alt="썸네일" 
                        class="thumbnail">
                    <div class="play-button">▶</div>
                    <iframe style="display: none;" frameborder="0" allowfullscreen></iframe>
                </div>
                <h3><a href="javascript:void(0)">{row['title']}</a></h3>
                <p><strong>조회수:</strong> {view_count}</p>
                <p><strong>좋아요 수:</strong> {like_count}</p>
                <p><strong>댓글 수:</strong> {comment_count}</p>
                <p><strong>게시 시간:</strong> {publish_time}</p>
                <a href="https://www.youtube.com/watch?v={row['video_id']}" target="_blank">동영상 보러가기</a>
            </div>
            """
        return video_cards