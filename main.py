import argparse
import asyncio


def main():
    # 定义命令
    parser = argparse.ArgumentParser(description="爬虫工具")
    # 如果没有cookie，获取cookie
    parser.add_argument(
        "-c", "--cookie", help="获取cookie", choices=["get_red_book_cookie"]
    )
    parser.add_argument("-t", "--type", help="爬虫类型", choices=["red_book"])
    parser.add_argument("-k", "--keyword", help="搜索关键字")

    args = parser.parse_args()

    if args.cookie == "get_red_book_cookie":
        from service.get_cookie import get_red_book_cookie

        print("开始获取cookie")
        asyncio.run(get_red_book_cookie())
        print("获取cookie结束")

    if args.type == "red_book":
        from service.red_book_crawler import RedBookCrawler

        if args.keyword is None:
            print("请输入搜索关键字")
            return
        RedBookCrawler().get_article_by_search(args.keyword)

        return


if __name__ == "__main__":
    main()
