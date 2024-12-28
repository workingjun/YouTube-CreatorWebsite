from scripts.utils.utils import load_template
from DB.database import MySQLYouTubeDB
from datetime import datetime
import math 

class HTMLGenerator:
    def __init__(self, db_manager: MySQLYouTubeDB):
        self.output_path = "transfer_files/index.html"
        self.db_manager = db_manager
        
    def save_index_to_file(self):
        last_video_cards = self.make_video_card(hidden=False)
        video_cards = self.make_video_card(start=5, stop=-1)
        self.template = load_template()
        html_output = self.template.format(
            last_video_cards=last_video_cards,
            video_cards=video_cards
            )
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(html_output)

    def make_video_card(self, start=0, stop=5, hidden=True):
        # Fetch video data
        df_videos = self.db_manager.fetch_all_videoData()
        video_cards_list = []  # HTML 조각을 저장할 리스트
        hidden_text = "video-card hidden" if hidden else "video-card-info"

        # Generate video cards
        for row in df_videos[start:stop]:
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
    

