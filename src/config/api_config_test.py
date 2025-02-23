api_key = [
    "api_key1",
    "api_key2",
    "api_key3",
    "api_key4",
    "api_key5",
    "api_key6"
]

def get_api_key(index):
    """1부터 시작하는 인덱스로 API 키를 반환"""
    if index < 1 or index > len(api_key):
        raise IndexError("Index out of range. Use 1 to {}".format(len(api_key)))
    return api_key[index - 1]