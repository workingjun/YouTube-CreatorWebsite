from modules.youtube import YouTubeManager

class HtmlManager:
    
    BODY="""
        <h2>채널이름</h2>
        <p>채널 이름: <a href="https://www.youtube.com/channel/{channelID}" target="_blank"> {channel_name}</a></p>
        
        <h3>구독자 수</h3>
        <p>구독자 수: {subscriber_count}</a></p>
        
        <h3>상위 10개의 동영상 통계 정보</h3>
        <table>
            <thead>
                <tr>
                    <th>제목</th>
                    <th>조회수</th>
                    <th>좋아요 수</th>
                    <th>댓글 수</th>
                    <th>게시 시간</th>
                    <th>좋아요 대비 조회수 비율</th>
                </tr>
            </thead>
            <tbody>
                {video_rows}
            </tbody>
        </table>
        
        <h3>상위 10개의 댓글 정보</h3>
        <table>
            <thead>
                <tr>
                    <th>동영상 ID</th>
                    <th>댓글</th>
                </tr>
            </thead>
            <tbody>
                {comment_rows}
            </tbody>
        </table>
        """

    def __init__(self, youtube_manager: YouTubeManager):
        self.youtube_manager = youtube_manager
        
    def load_template(self):
        with open("templates/Template.html", "r", encoding="utf-8") as file:
            template = file.read()
            template = template.replace("{", "{{").replace("}", "}}").replace("{{body}}", "{body}")
            return template

    def htmlrun(self):
        # 데이터 수집
        df_videos, df_comments = self.youtube_manager.collect_data()
        # 좋아요 대비 조회수 비율 계산
        df_videos['like_view_ratio'] = df_videos['like_count'] / df_videos['view_count']

        # 데이터 HTML에 삽입
        video_rows = ""
        for _, row in df_videos.iterrows():
            publish_time = row['publish_time'].replace("T", "\n").replace("Z", "")
            view_count = format(row['view_count'], ",")
            like_count = format(row['like_count'], ",")
            comment_count = format(row['comment_count'], ",")
            video_rows += f"""
                <tr>
                    <td><a href="https://www.youtube.com/watch?v={row['video_id']}" target="_blank"> {row['title']}</a></td>
                    <td>{view_count}</td>
                    <td>{like_count}</td>
                    <td>{comment_count}</td>
                    <td>{publish_time}</td>
                    <td>{row['like_view_ratio']:.2f}</td>
                </tr>
            """

        comment_rows = ""
        for _,row in df_comments.iterrows():
            comment_rows += f"""
            <tr>
                <td style="width: 20%;"><a href="https://www.youtube.com/watch?v={row['video_id']}" target="_blank">{row['title']}</a></td>
                <td>
                    <ul>{''.join(f'<li>{comment}</li>' for comment in row["comments"])}</ul>
                </td>
            </tr>
            """
        subscriber_count = format(self.youtube_manager.ChannelInformation()[2], ",")
        Body_output = self.BODY.format(
            channel_name=self.youtube_manager.ChannelInformation()[0],
            channelID=self.youtube_manager.ChannelInformation()[1],
            subscriber_count=subscriber_count,
            video_rows=video_rows,
            comment_rows=comment_rows
            )

        return Body_output