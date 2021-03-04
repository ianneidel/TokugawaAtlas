'''
This script is used to copy the color pallet of 250 traditional Japanese colors
from nipponcolors.com.
Color data cited: “日本の伝統色 The Traditional Colors of Japan”. PIE BOOKS, 2007.
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from matplotlib import colors
import urllib3
import datetime as dt


class NipponColorScraper:
    '''
    Need to use chromium for scraping since nipponcolors.com loads a random color
    before altering the page with JS to fade to color selected in url params.
    '''
    def __init__(self, base_url, run=True):
        self.base_url = base_url
        self.run = run
        self.curr_color = None

        # Set up the headless chrome browser to handle js loading on db page
        driver_path = "/Users/rjc/Downloads/chromedriver 2"
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')

        if self.run:
            self.log("Launching headless chrome")
            self.driver = webdriver.Chrome(driver_path, options=options)
            self.wait = WebDriverWait(self.driver, timeout=15)
            self.log("Sucessfully loaded headless chrome driver")

    def not_busy(self, driver):
        '''
        Function to enforce waiting for the color page to load.
        '''
        try:
            element = self.driver.find_element_by_xpath(
                "//*[@id=\"colorRuby\"]")
        except NoSuchElementException:
            return False

        # Wait until the page loads to the actuall color we want
        self.log("Want: {}, At: {}".format(self.curr_color,
                                           element.text.lower()))
        return element.text.lower() == self.curr_color

    def get_colors(self, color_names, outfile):
        '''
        Function to scrape all the color hex values from the different
        pages.
        '''

        # Write all the player urls to a file. Save incrementally in case something breaks!
        out = open(outfile, "w")
        names = open(color_names, "r").readlines()

        for i, name in enumerate(names):
            self.log("Getting color {}/250: {}".format(i + 1, name))

            # Set the color we are searching for to reference later while waiting for page load
            self.curr_color = name.strip()

            self.driver.get(self.base_url + "#" + name)
            self.wait.until(self.not_busy)
            page_source = self.driver.page_source

            # Parse the page source with BeautifulSoup and get all player links
            soup = BeautifulSoup(page_source, 'xml')
            r = soup.find("dd", {"class": "r"}).text
            g = soup.find("dd", {"class": "g"}).text
            b = soup.find("dd", {"class": "b"}).text

            rgb = (int(r), int(g), int(b))
            hex_val = '#%02x%02x%02x' % rgb
            hex_val = hex_val.upper()

            self.log("Retreived Hex: {}".format(hex_val))
            out.write(hex_val + '\n')

        out.close()

    def order_colors(self, color_names, hex_file, outfile):
        '''
        On-off function since original list of colors was coppied in wrong order.
        '''
        http = urllib3.PoolManager()
        response = http.request('GET', self.base_url)
        soup = BeautifulSoup(response.data)

        colors = soup.find_all('a')
        colors = colors[3:253]
        assert (len(colors) == 250)
        colors = [color.text for color in colors]
        romaji = [color.split(',')[1].strip().lower() for color in colors]
        kanji = [color.split(',')[0].strip().lower() for color in colors]

        hex_map = dict()
        unordered_names = open(color_names, "r").readlines()
        hex_vals = open(hex_file, "r").readlines()
        assert (len(unordered_names) == len(hex_vals))

        for i, name in enumerate(unordered_names):
            hex_map[name.strip()] = hex_vals[i].strip()

        print(hex_map.keys())
        out = open(outfile, "w")
        for i, color in enumerate(romaji):
            line = kanji[i] + ',' + color + ',' + hex_map[color] + '\n'
            out.write(line)

    def log(self, message):
        print("[NipponColorScraper {}] : {}".format(dt.datetime.now(),
                                                    message))


if __name__ == "__main__":
    base_url = "https://nipponcolors.com/"
    spider = NipponColorScraper(base_url)

    # Uncomment to re-scrape all hex colro values
    # spider.get_colors(color_names="color_names.txt", outfile="colors.txt")

    # Uncomment to do the one-off color ordering and generate csv of kanji, romaji, hex
    # spider.order_colors("color_names.txt",
    #                     "colors_hex.txt",
    #                     outfile="colors.txt")
