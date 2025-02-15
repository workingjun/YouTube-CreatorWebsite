api_key = [
    "AIzaSyDA38IZdJjA6BEgkUe_TKeQc2q9YPUf0xE", 
    "AIzaSyCqn7MaBwhHwSxBhj8HxfYaiHNVA33Xx74",
    "AIzaSyBkbCe8_hZVj2MKgoPDZyTmSew9yHCBEdE",
    "AIzaSyBah1gLE-kNJnrV_HZbVadAv-2ztjqNOT8",
    "AIzaSyC7mvnHXvy8MniPuc4pwAe9fKq2wAUJs1s",
    "AIzaSyB3oVEwa_XS6U0DMBPDh5L2Lqh6xTSzG0Q",
    "AIzaSyDmhjtFCxm_4BqcevulfJtGRqqkiAA1Bkc",
    "AIzaSyC89Z-buolVgFmDoH9Q74JIbO23q-IIPko"
]

def get_api_key(index):
    """1부터 시작하는 인덱스로 API 키를 반환"""
    if index < 1 or index > len(api_key):
        raise IndexError("Index out of range. Use 1 to {}".format(len(api_key)))
    return api_key[index - 1]