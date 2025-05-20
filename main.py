COMMUNITY_NAME = "asyabio"

import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Открываем страницу сообщества ВКонтакте
        await page.goto(f'https://vk.com/{COMMUNITY_NAME}')  # Замените на имя вашего сообщества

        # Ждем, пока страница загрузится
        await page.wait_for_load_state('networkidle')

        # Получаем все посты
        posts = await page.query_selector_all('.post')  # Замените селектор на актуальный для постов
        if posts:
            latest_post = posts[0]
            post_id = await latest_post.get_attribute('data-post-id')  # Замените на актуальный атрибут для ID поста

            # Читаем последний сохранённый ID поста
            last_post_id_file = 'last_post_id.txt'
            if os.path.exists(last_post_id_file):
                with open(last_post_id_file, 'r') as file:
                    last_post_id = file.read().strip()
            else:
                last_post_id = None

            # Сравниваем ID постов
            if post_id != last_post_id:
                # Сохраняем новый ID поста
                with open(last_post_id_file, 'w') as file:
                    file.write(post_id)

                # Проверяем наличие ключевого слова "отработка"
                post_text = await latest_post.inner_text()
                if "отработка" in post_text:
                    # Нажимаем кнопку комментировать
                    comment_button = await latest_post.query_selector('.reply')  # Замените селектор на актуальный для кнопки комментирования
                    await comment_button.click()

                    # Вводим текст комментария
                    await page.fill('textarea', 'Меркулова Анастасия')  # Замените селектор на актуальный для текстового поля комментария
                    await page.click('button[type="submit"]')  # Замените селектор на актуальный для кнопки отправки комментария
            else:
                print("Новых постов нет.")

        # Закрываем браузер
        await browser.close()

# Запускаем асинхронную функцию
asyncio.run(main())
