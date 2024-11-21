from modules.youtube import YouTubeManager
import math 
import json

class HtmlManager:
    PATH1 = "youtube_data/templates/template.html"
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
        df_videos, df_comments = self.youtube_manager.collect_data()
        self.save_comments_to_file(df_comments)
        last_video_cards = self.make_video_card(df_videos, 5)
        video_cards = self.make_video_card(df_videos)

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
    
    def make_video_card(self, df_videos, count=-1):
        # 좋아요 대비 조회수 비율 계산    
        df_videos['like_view_ratio'] = df_videos['like_count'] / df_videos['view_count']

        video_cards = ""
        for _, row in df_videos[:count].iterrows():
            publish_time = row['publish_time'].replace("T", " ").replace("Z", "")
            view_count = format(row['view_count'], ",")
            like_count = format(row['like_count'], ",")
            comment_count = format(row['comment_count'], ",")
            like_view_ratio = f"{(row['like_count'] / row['view_count']) * 100:.2f}%"
            like_view_var = math.sqrt(row['view_count'] * row['like_count'])

            video_cards += f"""
            <div class="video-card" data-date="{publish_time}" data-comments="{row['comment_count']} "data-views="{row['view_count']}" data-likes="{row['like_count']}" data-popular="{like_view_var}">
                <img src="https://i.ytimg.com/vi/{row['video_id']}/hqdefault.jpg" alt="{row['title']} 썸네일" class="thumbnail">
                <h3><a href="comments.html?videoId={row['video_id']}">{row['title']}</a></h3>
                <p><strong>조회수:</strong> {view_count}</p>
                <p><strong>좋아요 수:</strong> {like_count}</p>
                <p><strong>댓글 수:</strong> {comment_count}</p>
                <p><strong>좋아요 대비 비율:</strong> {like_view_ratio}</p>
                <p><strong>게시 시간:</strong> {publish_time}</p>
                <a href="https://www.youtube.com/watch?v={row['video_id']}" target="_blank">동영상 보러가기</a>
            </div>
            """
        return video_cards
    
    def save_comments_to_file(self, df_comments):
        comments_data={}
        for _, row in df_comments.iterrows():
            comments_html = ""
            for comment, like_count in zip(row["comments"], row["like_count"]):  # 상위 5개 댓글
                comments_html += f"""
                <div class="comment-card">
                    <p class="comment-text">{comment}</p>
                    <span class="comment-likes">👍 {like_count} likes</span>
                </div>
                """
            comments_data[row["video_id"]] = f"""
            <div class="comment-container">
                <h4 class="video-title">{row['title']}</h4>
                <div class="comment-list">{comments_html}</div>    
            </div>
            """
        # JSON 파일로 저장
        with open(self.PATH3, "w", encoding="utf-8") as f:
            json.dump(comments_data, f, ensure_ascii=False, indent=4)

        
