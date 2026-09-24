from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file://' + os.path.abspath('carousel.html'))
    # wait for fonts to load
    page.wait_for_timeout(2000)
    page.pdf(path=r'C:\Users\tmalu\Desktop\Amana_Wrap_Carousel_22Sep.pdf', width='1080px', height='1080px', print_background=True)
    browser.close()
