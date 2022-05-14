import os

from ebooklib import epub

from lib.coms import *

CSS_STYLE = open("./lib/template/epub.css").read()


class EpubMaker(object):
    def __init__(self, html_path: str, out_path: str):
        self.html_path = html_path
        self.out_path = out_path

    def make_epub(self):

        html_path = self.html_path
        out_path = self.out_path

        # 文件夹名称
        path_name = os.path.basename(html_path)
        path_names = path_name.split("_", maxsplit=2)
        # 作者
        book_author = path_names[0]
        # 标题
        book_title = path_names[1]
        # 唯一标识
        book_identifier = md5(book_title)

        # 新建电子书
        book = epub.EpubBook()

        # set metadata
        book.set_identifier(book_identifier)
        book.set_title(book_title)
        book.set_language('cn')

        book.add_author(book_author)

        # define CSS style
        print("通用样式文件")
        style_item = epub.EpubItem(uid="stylesheet", file_name="stylesheet.css", media_type="text/css",
                                   content=CSS_STYLE)
        book.add_item(style_item)

        # create chapter
        file_list = os.listdir(html_path)
        file_list.sort()

        # 章节列表
        html_list = []

        for file_name in file_list:
            if not file_name.endswith(".html"):
                continue
            # 章节标题
            title = file_name.split(".")[0].split("_", maxsplit=2)[1].strip().replace('\b', '')
            # 链接ID
            link_id = file_name.split("_", maxsplit=2)[0]
            # 链接地址
            link_name = link_id + ".html"

            html_item = epub.EpubHtml(title=title, file_name=link_name, lang='utf-8')
            html_item.content = open(os.path.join(html_path, file_name), "rb").read()
            html_item.add_item(style_item)
            html_item.id = link_id

            print("生成章节：", title)

            book.add_item(html_item)
            html_list.append(html_item)

        # 图片
        images_path = os.path.join(html_path, "images")
        images_list = ([], os.listdir(images_path))[os.path.isdir(images_path)]
        for image_name in images_list:
            if len(image_name.split(".")) < 2:
                continue
            # 图片绝对路径
            image_path = os.path.join(html_path, "images", image_name)

            # 创建图片
            image_item = epub.EpubImage()
            image_item.file_name = "images/" + image_name
            image_item.media_type = "image/jpeg"
            image_item.content = open(image_path, 'rb').read()

            book.add_item(image_item)

        print("添加图片：", len(images_list))

        # define Table Of Contents
        book.toc = [epub.Link(item.file_name, item.title, item.id) for item in html_list]

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        nav = epub.EpubNav()
        nav.add_item(style_item)
        book.add_item(nav)

        # basic spine
        book.spine = ['nav'] + [item.id for item in html_list]

        # write to the file
        book_file_name = path_name + '.epub'
        print("开始制作epub", book_file_name)

        if not os.path.isdir(out_path):
            os.makedirs(out_path)
        epub.write_epub(os.path.join(out_path, book_file_name), book, {})
        print("制作epub完成", book_file_name)
