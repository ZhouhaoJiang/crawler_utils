import csv
import random
import re
import time

from DrissionPage import WebPage, ChromiumOptions
from config import is_headless, max_article_num, red_book_cookie_path
from config import red_book_url
from service.logger_config import logger


class RedBookCrawler:
    def __init__(self):
        self.url = red_book_url
        if is_headless:
            self.page = WebPage(chromium_options=ChromiumOptions().headless())
        else:
            self.page = WebPage()
        with open(red_book_cookie_path, "r") as f:
            cookie = f.read()
            self.page.get("http:/www.baidu.com")
            self.page.set.cookies(cookie)

    def get_article_by_search(self, key_word):
        try:
            self.page.get(self.url)
            search_input = self.page.ele("@class=search-input")
            search_input.input(key_word + "\n")
            self.page.wait.ele_displayed("xpath=//*[@id='search-type']/div/div/div[2]")
            self.page.ele("xpath=//*[@id='search-type']/div/div/div[2]").click()
            self.page.wait.ele_displayed("@class=feeds-container")

            processed_articles = 0

            # 创建csv便于存储数据
            # 获取项目根目录
            import os

            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            file_path = os.path.join(
                project_root, f"data/{now_time}_red_book_articles.csv"
            )

            with open(
                file_path,
                "w",
            ) as f:
                f.write(
                    "author_name,author_avatar_url,title,description,date,media_urls\n"
                )

            while processed_articles < max_article_num:
                article_list = self.page.ele("@class=feeds-container")
                article_section_list = article_list.eles("tag=section")

                article_redict_url_list = []
                for i, _ in enumerate(article_section_list):
                    if processed_articles >= max_article_num:
                        break

                    # 尝试获取每个section中的<a>标签的链接，如果找不到，则继续处理下一个section
                    try:
                        article_redict_url = (
                            article_section_list[i]
                            .ele("xpath=.//div/a", timeout=5)
                            .link
                        )
                        article_redict_url_list.append(article_redict_url)
                    except Exception as e:
                        print(f"An error occurred while processing article {i}: {e}")
                        continue  # 继续处理下一个文章section

                print(f"Article URLs: {article_redict_url_list}")
                logger.info(f"Article URLs: {article_redict_url_list}")

                for article_redict_url in article_redict_url_list:
                    new_tab = self.page.new_tab(url=article_redict_url)
                    # 开始提取文章数据
                    try:
                        article_data = self.extract_and_print_article_data(page=new_tab)
                        # 追加写入到csv
                        with open(file_path, "a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow(
                                [
                                    article_data["author_name"],
                                    article_data["author_avatar_url"],
                                    article_data["title"],
                                    article_data["description"],
                                    article_data["date"],
                                    article_data["media_urls"],
                                ]
                            )
                    except Exception as e:
                        print(f"An error occurred while extracting article data: {e}")
                    finally:
                        self.page.close_tabs(others=True)
                        processed_articles += 1
                if processed_articles < max_article_num:
                    self.page.run_js("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)
                    self.page.wait.ele_displayed("@class=feeds-container", timeout=10)

        except Exception as e:
            print(e)
        finally:
            self.page.close()

    @staticmethod
    def get_article_media(article_container):
        """
        获取文章中的图片链接
        :param article_container:
        :return:
        """
        article_media_url_list = []
        article_media_swiper = article_container.s_ele("@class=swiper-wrapper")
        article_media_list = article_media_swiper.s_eles("xpath=.//div")

        for article_media in article_media_list:
            article_media_url = article_media.style("background-image")
            match = re.search(r'url\("(http[^"]+)"\)', article_media_url)
            if match:
                article_media_url_list.append(match.group(1))

        return article_media_url_list

    @staticmethod
    def extract_and_print_article_data(page):
        """
        用于提取文章数据
        :return:
        """
        article_container = page.ele("xpath=//div[@id='noteContainer']")
        # 用户信息
        author_avatar_url = article_container.s_ele("@class=avatar-item").link
        author_name = article_container.s_ele("@class=username").text

        # 文章图片
        article_media_swiper = article_container.ele("@class=swiper-wrapper")
        article_media_list = article_media_swiper.eles("xpath=.//div")
        article_media_url_list = []
        for article_media in article_media_list:
            article_media_url = article_media.style("background-image")
            # 匹配出url
            match = re.search(r'url\("(http[^"]+)"\)', article_media_url)
            if match:
                article_media_url_list.append(match.group(1))

        # 文章信息
        article_title = (
            article_container.s_ele("@id=detail-title").text
            if article_container.s_ele("@id=detail-title")
            else ""
        )
        article_desc = (
            article_container.s_ele("@id=detail-desc").text
            if article_container.s_ele("@id=detail-desc")
            else ""
        )
        article_date = (
            article_container.s_ele("@class=date").text
            if article_container.s_ele("@class=date")
            else ""
        )

        # 打印文章信息
        print(
            f"Author: {author_name} ({author_avatar_url})\n"
            f"Title: {article_title}\n"
            f"Description: {article_desc}\n"
            f"Date: {article_date}\n"
            f"Media URLs: {article_media_url_list}\n"
        )

        return {
            "author_name": author_name,
            "author_avatar_url": author_avatar_url,
            "title": article_title,
            "description": article_desc,
            "date": article_date,
            "media_urls": article_media_url_list,
        }


if __name__ == "__main__":
    read_book_crawler = RedBookCrawler()
    read_book_crawler.get_article_by_search("python")
