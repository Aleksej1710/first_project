import allure
from playwright.sync_api import Page, expect
from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    # ---------- Действия ----------

    @allure.step("Удаляем товар из корзины: {product_name}")
    def remove_item(self, product_name: str):
        card = self.basket.remove_item(product_name)
        expect(card).not_to_be_visible()
        return self

    @allure.step("Переходим к оформлению заказа")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Считаем сумму товаров в корзине")
    def get_items_total_price(self) -> float:
        # вызывать ПОСЛЕ expect_items_in_cart: all_text_contents() — снимок, он не ждёт
        return round(sum(self.basket.get_item_prices()), 2)

    @allure.step("Проверяем, что открыта корзина")
    def check_basket_opened(self):
        expect(self.page).to_have_url(BasketPage.URL)
        expect(self.basket.checkout_button).to_be_visible()
        return self

    @allure.step("Проверяем товары в корзине: {names}")
    def expect_items_in_cart(self, names: list[str]):
        expect(self.basket.item_names).to_have_text(names)
        return self

    @allure.step("Проверяем счётчик корзины: {expected}")
    def check_cart_count(self, expected: int):
        if expected == 0:
            expect(self.basket.cart_badge).not_to_be_visible()
        else:
            expect(self.basket.cart_badge).to_have_text(str(expected))
        return self
