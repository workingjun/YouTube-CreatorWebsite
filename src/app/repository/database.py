from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, BigInteger,
    TIMESTAMP, func, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

import time
from sqlalchemy import create_engine
from src.app.repository.ssh_tunnel import start_ssh_tunnel, stop_ssh_tunnel

Base = declarative_base()

class YoutuberNameIDS(Base):
    __tablename__ = 'YoutuberName_IDS'

    video_id = Column(String(255), nullable=False, primary_key=True)
    channel_id = Column(String(255))
    publish_time = Column(DateTime, nullable=False)


class YoutuberNameLinks(Base):
    __tablename__ = 'YoutuberName_Links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_name = Column(String(255))
    image_link = Column(Text)
    external_link = Column(Text)


class YoutubeChannel(Base):
    __tablename__ = 'youtube_channels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(255))
    thumbnail = Column(Text)
    description = Column(Text)
    subscriber_count = Column(Integer)
    video_count = Column(Integer)
    views_count = Column(BigInteger)

    videos = relationship("YoutubeVideo", back_populates="channel")

class YoutuberNameVIDEO(Base):
    __tablename__ = 'YoutuberName_VIDEO'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(255))
    video_id = Column(String(255), nullable=False)
    title = Column(Text, nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    publish_time = Column(DateTime, nullable=False)
    is_shorts = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    channel = relationship("YoutubeChannel", back_populates="videos")
    
_conn = None
_engine = None
_tunnel = None
_session = None 

def connect(DB_CONFIG, ssh_flags: bool = False, retries: int = 5, delay: int = 5):
    global _conn, _engine, _tunnel, _session
    if _engine is not None and _conn is not None:
        print("Using existing MySQL connection via SQLAlchemy engine.")
        return

    if ssh_flags:
        print("Starting SSH tunnel...")
        _tunnel = start_ssh_tunnel()
        DB_CONFIG["port"] = _tunnel.local_bind_port
        print("SSH tunnel started at local port %s", _tunnel.local_bind_port)

    db_url = (
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}"
    )

    attempt = 0
    while attempt < retries:
        try:
            print(f"Attempting MySQL connection, attempt {attempt + 1} of {retries}")
            _engine = create_engine(db_url, pool_pre_ping=True)
            Base.metadata.create_all(_engine)
            Session = sessionmaker(bind=_engine)
            _session = Session()
            ## 패턴 추가 해야 함 

            _conn = _engine.connect()
            print("MySQL connection established via SQLAlchemy engine.")
            return
        except Exception as e:
            print(f"MySQL connection failed: {str(e)}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed to connect to MySQL after {retries} attempts.")
        except KeyboardInterrupt:
            raise

def close():
    global _conn, _engine, _tunnel
    if _conn:
        print("Closing SQLAlchemy connection...")
        _conn.close()
        _conn = None

    if _engine:
        print("Disposing SQLAlchemy engine...")
        _engine.dispose()
        _engine = None

    if _tunnel is not None:
        print("Stopping SSH tunnel...")
        stop_ssh_tunnel()
        _tunnel = None

if __name__=='__main__':

    Session = sessionmaker(bind=_engine)
    session = Session()

    channel = YoutubeChannel(
        title="Example Channel",
        channel_id="UC1234567890",
        thumbnail="http://example.com/image.jpg",
        description="This is an example channel",
        subscriber_count=100000,
        video_count=50,
        views_count=5000000
    )

    session.add(channel)  # 세션에 추가
    session.commit()      # 실제 DB에 반영

    channels = session.query(YoutubeChannel).all()
    for ch in channels:
        print(ch.title, ch.subscriber_count)
        for vid in ch.videos:
            print(" -", vid.title, vid.view_count)
