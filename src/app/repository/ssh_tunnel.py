import sshtunnel
from src.utils.yamL import load_yaml

FILE_NAME_DB = './config/db_config.dev.yaml'
DB_CONFIG = load_yaml(FILE_NAME_DB)["default"]

_tunnel = None

def start_ssh_tunnel():
    global _tunnel

    if _tunnel is None:
        _tunnel = sshtunnel.SSHTunnelForwarder(
            (DB_CONFIG['host'], 22),
            ssh_username=DB_CONFIG['user'],
            ssh_password=DB_CONFIG['password'],
            remote_bind_address=(DB_CONFIG['localhost'], 3306),
            local_bind_address=('127.0.0.1', 0)  # 동적 포트
        )
        _tunnel.start()
        print(f"[SUCCESS] SSH tunnel connection established: {_tunnel.local_bind_port}")
    return _tunnel
    
def stop_ssh_tunnel():
    global _tunnel
    
    if _tunnel is not None:
        _tunnel.stop()
        _tunnel = None
        print("[SUCCESS] SSH tunnel connection closed")