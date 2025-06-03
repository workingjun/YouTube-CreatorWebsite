from src.app.youtube.api_manager import YoutubeApiManager
from src.app.repository.database import (
    YoutubeChannel, YoutuberNameVIDEO, YoutuberNameLinks, YoutuberNameIDS, _session
    )
from src.utils.yamL import load_yaml

FILE_NAME_CH = './config/channelid.dev.yaml'
CHANNELID = load_yaml(FILE_NAME_CH)['CHANNELID']

class YouTubeManager:
    def __init__(self, api_key, clannel_id=None, channel_name=None):
        self.api_manager = YoutubeApiManager(
            api_key=api_key, 
            clannel_id=clannel_id, 
            channel_name=channel_name
        )

    def collect_videoData(self, video_ids, table_name):
        for video_id in video_ids:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            db_manager.videoDt.upsert_data(table_name, stats)
            for res in stats:
                existing = _session.query(YoutuberNameVIDEO).filter(YoutuberNameVIDEO.video_id==res['video_id']).first()
                if existing:
                    for key, value in res.items():
                        setattr(existing, key, value)
                else:
                    new_channel = YoutubeChannel(**res)
                    _session.add(new_channel)
            _session.commit()

    def collect_videoId(self, table_name, update_video_ids:bool=False):
        if update_video_ids:
            video_ids_list = self.api_manager.get_videoIds() 
            for res in video_ids_list:
                existing = _session.query(YoutuberNameIDS).filter(YoutuberNameIDS.video_id==res['video_id']).first()
                if existing:
                    for key, value in res.items():
                        setattr(existing, key, value)
                else:
                    new_channel = YoutubeChannel(**res)
                    _session.add(new_channel)
            _session.commit()
            video_ids = [row['video_id'] for row in video_ids_list]
        else:
            video_ids = [row['video_id'] for row in 
                _session.query(YoutuberNameIDS).filter(YoutuberNameIDS.channel_id == table_name).all()] 
        
        return video_ids

    def collect_channelInfo(self):
        results = self.api_manager.get_channel_information()
        for res in results:
            existing = _session.query(YoutubeChannel).filter_by(channel_id=res['channel_id']).first()
            if existing:
                for key, value in res.items():
                    setattr(existing, key, value)
            else:
                new_channel = YoutubeChannel(**res)
                _session.add(new_channel)
        _session.commit()
        
