import html
import time

from bs4 import BeautifulSoup
import requests
import os
import shutil

import json

from lib.coms import *
from lib.geektime_api import GeekTimeApi

HTML_TEMPLATE = open("./lib/template/page.html").read()


class PageDownloader(object):
    productId: int
    htmlPath: str
    productPath: str
    force: bool

    def __init__(self, productId: int, htmlPath, force=False):
        self.productId = productId
        self.htmlPath = htmlPath
        self.force = force

        self.api = GeekTimeApi()

    def download_jpg(self, image_url, image_localpath):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_localpath, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

    # 取得演讲图片
    def download_images(self, html_str):
        soup = BeautifulSoup(html_str, 'lxml')
        for pic_href in soup.find_all('p'):
            for pic in pic_href.find_all('img'):
                img_url = pic.get('src')
                rdir = 'images'
                img_dir = os.path.join(self.productPath, rdir)
                if not os.path.exists(img_dir):
                    os.makedirs(img_dir)
                filename = os.path.basename(img_url).split("?")[0]
                img_path = os.path.join(img_dir, filename)
                print_gray('\t\t开始下载 %s' % img_url)

                try:
                    self.download_jpg(img_url, img_path)
                except IOError as e:
                    print("图片下载失败1", e, img_url)

                pic['src'] = os.path.join(rdir, filename)
                pic['class'] = 'down_img'
                parentNode = pic.find_parent('p')
                if parentNode:
                    parentNode['class'] = 'img_container'
        return soup.prettify()

    def download_article(self, index, article_id):
        file_list = os.listdir(self.productPath)
        file_list.sort()
        for file_name in file_list:
            file_index = file_name.split('_')[0]
            if file_index and file_name.endswith(".html"):
                if int(file_index) == index:
                    return

        article = self.api.get_article(article_id)
        article_title = article.get('article_title')
        article_content = article.get('article_content')
        product_id = article.get('product_id')
        share_title = article.get('share', {}).get('title', '')

        article_title2 = article_title.replace('/', '').replace('?', '').replace('？', '').replace('<', '').replace('>',
                                                                                                                   '')
        html_path = f'{self.productPath}/{str(index).zfill(3)}_{article_title2}.html'
        if os.path.exists(html_path):
            return

        html_text = self.download_images(HTML_TEMPLATE
                                         .replace('{{courseName}}', share_title)
                                         .replace('{{title}}', html.escape(article_title))
                                         .replace('{{content}}', article_content))
        print_blue("\t保存文章", product_id, article_id, "《" + article_title + "》")

        f1 = open(html_path, 'w+',
                  encoding='utf-8',
                  newline='')
        f1.write(html_text)
        f1.close()

    def begin_download_article(self, article_list):
        for i in range(len(article_list)):
            article_id = article_list[i].get("id")
            print_yellow("\tDOWNLOAD_ARTICLE:", i, len(article_list), article_id)
            self.download_article(i, article_id)

    def download(self):
        product = self.api.get_product_info(self.productId)
        title = product.get('title')
        author_name = product.get('author').get("name")
        # article_id = product.get('article').get("id")

        self.productPath = os.path.join(self.htmlPath, author_name + "_" + title)

        if os.path.exists(self.productPath) and not self.force:
            print_yellow(title, author_name, '已经存在')
            return
        if os.path.exists(self.productPath):
            shutil.rmtree(self.productPath)

        os.makedirs(self.productPath)

        article_list = self.api.get_article_list(self.productId)
        print_yellow(title, author_name, len(article_list))
        self.begin_download_article(article_list)

        return self.productPath
