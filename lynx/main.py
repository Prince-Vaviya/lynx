from .config import get_api_key

def main():
    API_KEY=get_api_key()
    print(API_KEY)