from scripts.youtube import YouTubeManager
from scripts.DataBase import DatabaseManager
import math 
from datetime import datetime

class HtmlManager:

    PATH1 = "template/template.html"
    PATH2 = "transfer_files/index.html"
    
    def __init__(self, youtube_manager: YouTubeManager):
        self.youtube_manager = youtube_manager
        
    def load_template_video(self):
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

    def save_files(self, db_manager):
        self.save_index_to_file(db_manager=db_manager)
        self.save_comments_to_file(db_manager=db_manager)
    
    def save_index_to_file(self, db_manager: DatabaseManager):
        last_video_cards = self.make_video_card(db_manager=db_manager, hidden=False)
        video_cards = self.make_video_card(db_manager=db_manager, start=5, stop=-1)
        result = self.youtube_manager.ChannelInformation()
        subscriber_count = format(result['subscriber_count'], ",")
        video_count = format(int(result['video_count']), ",")
        views_count = format(int(result['views_count']), ",")
        self.template = self.load_template_video()
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

    def make_video_card(self, db_manager: DatabaseManager, start=0, stop=5, hidden=True):
        # Fetch video data
        df_videos = db_manager.fetch_all_videodata()
        video_Ids = self.youtube_manager.collect_data(db_manager=db_manager)
        video_cards_list = []  # HTML 조각을 저장할 리스트

        #for video_id in video_Ids:
        #    for row in df_videos:
        #        if df_videos["video_id"] == video_id:

        # Define card visibility class
        hidden_text = "video-card hidden" if hidden else "video-card-info"

        # Generate video cards
        for row in df_videos:
            # Calculate engagement metrics
            publish_time = row['publish_time']
            view_count = format(row['view_count'], ",")
            like_count = format(row['like_count'], ",")
            comment_count = format(row['comment_count'], ",")
            current_time = datetime.now()
            time_difference = current_time - publish_time
            elapsed_hours = time_difference.total_seconds() / 3600  # Convert seconds to hours
            Engagement_Rate = (row['comment_count'] + row['like_count']) / row['view_count']
            half_life = 24 * 30  # 30 days
            trand_point = Engagement_Rate * math.exp(-elapsed_hours / half_life)

            # Append HTML for the video card
            video_cards_list.append(f"""
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
                <h3><a href="#" class="open-modal-link" data-video-id="{row['video_id']}">{row['title']}</a></h3>
                <p><strong>조회수:</strong> {view_count}</p>
                <p><strong>좋아요 수:</strong> {like_count}</p>
                <p><strong>댓글 수:</strong> {comment_count}</p>
                <p><strong>게시 시간:</strong> {publish_time}</p>
                <a href="https://www.youtube.com/watch?v={row['video_id']}" target="_blank">동영상 보러가기</a>
            </div>
            """)

        # Combine all video cards into a single HTML string
        return "".join(video_cards_list)

    def save_comments_to_file(self, db_manager: DatabaseManager):
        # Fetch all comments from the database
        results = db_manager.fetch_all_comments()
        comments_dict = {}

        # Organize comments by video_id
        for row in results:
            video_id = row['video_id']
            if video_id not in comments_dict:
                comments_dict[video_id] = []
            comments_dict[video_id].append({
                "author": row["author"],
                "like_count": row["like_count"],
                "text": row["text"]
            })

        # Generate the modal HTML for each video
        for video_id, comments_list in comments_dict.items():
            if not comments_list:
                comments_html = "<p>댓글이 없습니다.</p>"
            else:
                comments_html = "<ul>" + "".join([f"""
    <li>
        <p><strong>{comment['author']}</strong></p>
        <p>{comment['text']}</p>
        <p>좋아요 수: {comment['like_count']}</p>
    </li>
    """ for comment in comments_list]) + "</ul>"

            comments_modal = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/styles.css"> 
</head>
    <body>
        <div id="loading-spinner" style="display: none;">
            <div class="spinner"></div>
            <div id="modal-{video_id}" class="comments-modal">
                <button class="close-modal-btn" onclick="closeCommentsModal()">×</button>
                {comments_html}
            </div>
        </div>
    </body>
</html>"""
            with open(f"transfer_files/html/cmnts{video_id}.html", "w", encoding="utf-8") as file:
                file.write(comments_modal)
        
    

