import sshtunnel
from config.db_config import MYSQL_HOST
from config.db_config import SSH_USER
from config.db_config import SSH_PASSWORD
from config.db_config import SSH_HOST

_tunnel = None

def start_ssh_tunnel():
    global _tunnel

    if _tunnel is None:
        _tunnel = sshtunnel.SSHTunnelForwarder(
            (SSH_HOST, 22),
            ssh_username=SSH_USER,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=(MYSQL_HOST, 3306),
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