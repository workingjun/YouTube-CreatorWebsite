import math
from datetime import datetime
from src.utils.template import load_main
from src.utils.template import load_template
from src.app.repository.database import (
    YoutubeChannel, YoutuberNameVIDEO, YoutuberNameLinks, YoutuberNameIDS, _session
    )
from src.utils.yamL import load_yaml

FILE_NAME_CH = './config/channelid.dev.yaml'
CHANNELID = load_yaml(FILE_NAME_CH)['CHANNELID']

def save_channel_index_to_file(output_path, table_name):
    channel_info = make_channel_info(table_name)
    last_video_cards = make_video_card(table_name, info_flag=True)
    video_cards = make_video_card(table_name, info_flag=False)
    template = load_template()
    html_output = template.format(
        channel_info=channel_info,
        last_video_cards=last_video_cards,
        video_cards=video_cards
        )
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_output)
    
def make_channel_info(table_name):
    result_channelInfo = _session.query(YoutubeChannel).filter(YoutubeChannel.channel_id == CHANNELID[table_name]).first()
    # result_Links = _session.query(YoutuberNameLinks).filter(YoutuberNameLinks.name == table_name).first()
    subscriber_count = format(result_channelInfo.subscriber_count, ",")
    view_count = format(result_channelInfo.views_count, ",")
    video_count = format(result_channelInfo.video_count, ",")

    # Links_html = ""
    # for row in result_Links:
    #     Links_html += f"""
    #         <a class="link-item" href="{row["external_link"]}" target="_blank" rel="nofollow noopener noreferrer">
    #             <img src="{row["image_link"]}" loading="lazy">
    #             <span>"{row["name"]}"</span>
    #         </a>"""
        
    return f"""<!-- 채널 정보 섹션 -->
        <div class="channel-info" id="channel-info">
            <h2>채널 정보</h2>
            <p>
                <a id="channel-link" 
                href="https://www.youtube.com/channel/{result_channelInfo["channel_id"]}" 
                target="_blank">
                    <img src="{result_channelInfo["thumbnail"]}" alt="채널 썸네일" class="thumbnail">
                </a>
            </p>
            <p>채널 이름: {result_channelInfo["title"]}</p>
            <p>구독자 수: {subscriber_count}</p>
            <p>채널 설명: {result_channelInfo["description"]}</p>
            <p>전체 조회 수: {view_count}</p>
            <p>동영상 수: {video_count}</p>
        </div>"""

    # <div class="links-section">
    #     <div class="links-list">
    #         {Links_html}
    #     </div>
    # </div>

def make_video_card(table_name, info_flag=True):
    # Fetch video data
    dic_videos = _session.query(YoutuberNameVIDEO).filter(YoutuberNameVIDEO.channel_id == CHANNELID[table_name]).all()

    # 조회수가 0 이상인 데이터만 필터링
    dic_videos = [row for row in dic_videos if row.get('view_count', 0) > 0]

    video_cards_list = []  # HTML 조각을 저장할 리스트
    hidden_text = "video-card-info" if info_flag else "video-card hidden"

    # info_flag에 따라 상위 5개 또는 나머지를 선택
    filtered_videos = dic_videos[:5] if info_flag else dic_videos[5:]

    # Generate video cards
    for row in filtered_videos:
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
        video_cards_list.append(f"""<div class="{hidden_text}" 
            data-date="{publish_time}" 
            data-comments="{row['comment_count']}"
            data-views="{row['view_count']}"
            data-likes="{row['like_count']}"
            data-trand="{trand_point}"
            data-video-id="{row['video_id']}"
            data-is-shorts="{row['is_shorts']}"
            data-group="{table_name}">
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
    
def save_main_index_to_file():
    # 폴더 내 모든 JSON 파일 읽기
    data_list = []
    info_cards_list = []

    data_list = _session.query(YoutubeChannel).all()

    # 모든 JSON 데이터 출력
    for data in data_list:
        view_count = format(data['views_count'], ",")
        video_count = format(data['video_count'], ",")
        subscriber_count = format(data['subscriber_count'], ",")

        info_cards_list.append(f"""<div class="card">
        <img src="{data["thumbnail"]}" alt="{data["title"]}">
        <h3><a href="{data["title"]}">{data["title"]}</a></h3>
        <p>구독자 수: {subscriber_count}</p>
        <p>전체 조회 수: {view_count}</p>
        <p>등록된 영상 수: {video_count}</p>
    </div>
    """)
    main_templates = load_main()
    main_html_output = main_templates.format(
        container="".join(info_cards_list)
    )
    with open("templates/main.html", "w", encoding="utf-8") as file:
        file.write(main_html_output)