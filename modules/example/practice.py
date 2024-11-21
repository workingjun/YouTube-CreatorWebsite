class Practice:
    def get_all_playlists(self):
        next_page_token = None
        playlists = []
        while True:
            request = self.youtube.playlists().list(
                part="snippet",
                channelId=self.channelID,
                maxResults=50,  # 한 번에 최대 50개
                pageToken=next_page_token
            )
            response = request.execute()
            # 재생목록 정보를 리스트에 추가
            for item in response['items']:
                playlists.append(item["id"])
            # 다음 페이지 토큰
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        return playlists

    def save_videoId_from_playlist(self):
        playlist_ids = self.get_all_playlists()  # 업로드 재생목록 ID 가져오기
        next_page_token = None
        video_ids = []
        for playlist_id in playlist_ids:
            while True:
                request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                for item in response['items']:
                    video_ids.append(item['snippet']['resourceId']['videoId'])
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
        # JSON 파일로 저장
        with open("data/videoId.json", "w", encoding="utf-8") as f:
            json.dump(video_ids, f, ensure_ascii=False, indent=4)
            print("json 파일 저장 완료")

    def append_videoId(self):
        with open("data/videoId.json", "w", encoding="utf-8") as file:
            video_ids = json.load(file)
        while True:
            request = self.youtube.search().list(
                part="snippet",
                channelId=self.channelID,
                maxResults=1,
                order="date",
                pageToken=next_page_token
            )
            response = request.execute()
            for item in response['items']:
                if item['id']['kind'] == "youtube#video":
                    video_id = item['id']['videoId']
            next_page_token = response.get("nextPageToken")

            if video_id==video_ids[-1]:
                break
            else:
                video_ids.append(video_id)
        # JSON 파일로 저장
        with open("data/videoId.json", "w", encoding="utf-8") as f:
            json.dump(video_ids, f, ensure_ascii=False, indent=4)
            print("json 파일 저장 완료")