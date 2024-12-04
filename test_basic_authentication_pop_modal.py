from playwright.sync_api import sync_playwright
import time


def test_pop_modal():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Embed username and password in the URL
        page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
        time.sleep(3)

        # Validate the result
        content = page.locator("body").inner_text()
        success_login = page.locator("//div[@id='content']/div/h3/following-sibling::p").text_content()
        print(content)  # Should confirm successful login
        print("success_login:\t",success_login)
        context.close()

        browser.close()
