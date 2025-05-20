import asyncio
from playwright.sync_api import sync_playwright
import os

COMMUNITY_NAME = "asyabio"



playwright = sync_playwright().start()
browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
# browser = playwright.chromium.launch(headless=False)
page = browser.new_page()

# Открываем страницу сообщества ВКонтакте
page.goto(f'https://vk.com/{COMMUNITY_NAME}')  # Замените на имя вашего сообщества

# Ждем, пока страница загрузится
page.wait_for_load_state('networkidle')

# Получаем все посты
posts =  page.query_selector_all("//div[contains(@class, 'post') and starts-with(@id, 'post-216822404_')]")  # Замените селектор на актуальный для постов
if posts:
    latest_post = posts[0]

    comment_button =  latest_post.query_selector("//div[contains(@class, 'post') and starts-with(@id, 'post-216822404_')]//div[contains(@class, 'comment')]")
    comment_button.click()

    # Вводим текст комментария
    page.fill('textarea', 'Меркулова Анастасия')  # Замените селектор на актуальный для текстового поля комментария
    page.click('button[type="submit"]')  # Замените селектор на актуальный для кнопки отправки комментария