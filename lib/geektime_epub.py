import os
import shutil

from lib.page_downloader import PageDownloader
from lib.epub_maker import EpubMaker

__current_path__ = os.path.dirname(__file__)
TEMP_PATH = os.path.abspath(os.path.join(__current_path__, '../temp'))


class GeekTime2Epub(object):
    def __init__(self, productId: int):
        self.htmlPath = os.path.join(TEMP_PATH, "html")
        self.epubPath = os.path.join(TEMP_PATH, "epub")
        self.productId = productId

    def start(self):
        productPath = PageDownloader(self.productId, self.htmlPath, True).download()
        EpubMaker(productPath, self.epubPath).make_epub()
        shutil.rmtree(productPath)
