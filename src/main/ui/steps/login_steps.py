import allure
from playwright.sync_api import Page, expect
from src.main.ui.pages.login_page import LoginPage


class LoginSteps:
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)

    @allure.step("Открываем страницу логина")
    def open_login_page(self):
        self.login_page.open()
        return self

    @allure.step("Логинимся пользователем {username}")
    def login(self, username: str, password: str):
        self.login_page.login(username, password)
        return self

    @allure.step("Проверяем, что открыта страница логина")
    def check_login_page_opened(self):
        expect(self.page).to_have_url(LoginPage.URL)
        expect(self.login_page.login_button).to_be_visible()
        return self

    @allure.step("Проверяем текст ошибки: {expected}")
    def check_error(self, expected: str):
        expect(self.login_page.error_message).to_have_text(expected)
        return self
