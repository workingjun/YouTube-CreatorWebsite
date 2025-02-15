import argparse
from src import create_app
from src import start_collect_link_data
from src import start_collect_creator_data

def main():
    parser = argparse.ArgumentParser(description="YouTube Creator Data Collection & Web Application")
    
    # 실행 옵션 추가
    parser.add_argument("--collect-links", action="store_true", help="Collect link data")
    parser.add_argument("--collect-creators", action="store_true", help="Collect creator data")
    parser.add_argument("--run-local", action="store_true", help="Run the web application server")

    args = parser.parse_args()

    # 옵션에 따라 실행
    if args.collect_links:
        print("🔹 Collecting link data...")
        start_collect_link_data()

    if args.collect_creators:
        print("🔹 Collecting creator data...")
        start_collect_creator_data()

    if args.run_local:
        print("🚀 Starting web server...")
        application = create_app()
        application.run(debug=True)

if __name__ == "__main__":
    main()