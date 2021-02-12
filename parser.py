import requests
from bs4 import BeautifulSoup, Tag
from typing import Optional, List
import lxml


class parse_html:
    """
    Get and parse https://play.google.com/store/apps/category/GAME
    page in html format and get categories links
    """
    def __init__(self, link: str = "https://play.google.com/store/apps/category/GAME"):
        """
        Get page at initialization
        :param link: link to google play market games
        """
        self.link = link
        self.html = None

    def _save_html(self):
        """
        Get html representation of the page
        """
        response = requests.get(self.link)
        if response.ok:
            self.html = response.content

    def get_categories_links(self) -> List[str]:
        """
        Get list of categories links from html page
        :return List[str]: categories
        """
        self._save_html()
        soup = BeautifulSoup(self.html, 'lxml')
        selector = soup.body.div.select(
            "div:last-child > c-wiz > div :nth-child(2) > c-wiz > div > c-wiz"
            " c-wiz > c-wiz > div > div > div:nth-of-type(2) a"
        )
        categories_link_tags = selector
        links = []
        for tag in categories_link_tags:
            link = tag.get("href")
            if link:
                links.append(
                    "https://play.google.com" +
                    tag["href"]
                )
        return links


class get_games_app_category:
    """Parse category from link,
    get name and """
    def __init__(self, link: str):
        """
        Parse category page
        :param link: links of categories to parse
        """
        self.link: Optional[str] = link
        self.name: Optional[str] = ""
        self.html: Optional[str] = None
        self.games_soup: List = []

    def _save_html(self):
        """Download html"""
        response = requests.get(self.link)
        if response.ok:
            self.html = response.content

    def parse_page(self):
        """Parse name and game categories"""
        self._save_html()
        soup = BeautifulSoup(self.html, 'lxml')
        if soup.h2:
            self.name = soup.h2.string
            selector = soup.body.div.select(
                ":nth-child(6) > c-wiz > div > c-wiz > div > c-wiz > c-wiz > c-wiz > div > :nth-child(2) div"
            )
            self.games_soup = selector

    def get_name(self) -> Optional[str]:
        """Get current state of category name"""
        return self.name


class get_games_app_names:
    """Get app names from pages soup"""
    def __init__(self, game_soup: Tag):
        self.game_soup = game_soup

    def get_name(self):
        a = self.game_soup.find('a')
        if a:
            name = a.get("href").split('=')[-1]
            return name
        return None


class parser_print:
    """Print games in special format"""
    def print_games(self):
        parser = parse_html('https://play.google.com/store/apps/category/GAME')
        categories = [get_games_app_category(link) for link in parser.get_categories_links()]
        for category in categories:
            if category:
                category.parse_page()
                games = [get_games_app_names(game_soup) for game_soup in category.games_soup]
                for game in games:
                    name = game.get_name()
                    if name:
                        if name.split('com.'):
                            print(f'/{category.name}/{name}')
