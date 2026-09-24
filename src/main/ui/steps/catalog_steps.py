import allure
from src.main.ui.pages.catalog_page import CatalogPage
from playwright.sync_api import Page, expect


class CatalogSteps:
    INVENTORY_URL = "https://www.saucedemo.com/inventory.html"  # потом → Urls

    def __init__(self, page: Page):
        self.page = page
        self.catalog = CatalogPage(page)

    # ---------- Действия ----------

    @allure.step("Добавляем товар в корзину: {product_name}")
    def add_to_cart(self, product_name: str):
        button = self.catalog.add_to_cart(product_name)
        expect(button).to_have_text("Remove")
        return self

    @allure.step("Удаляем товар из корзины: {product_name}")
    def remove_from_cart(self, product_name: str):
        button = self.catalog.remove_from_cart(product_name)
        expect(button).to_have_text("Add to cart")
        return self

    @allure.step("Сортируем товары: {option}")
    def sort_items(self, option: str):
        self.catalog.sort_items(option)
        return self

    @allure.step("Выполняем логаут")
    def logout(self):
        self.catalog.logout()
        return self

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.catalog.open_basket()
        return self

    # ---------- Проверки ----------

    @allure.step("Проверяем, что открыт каталог")
    def check_catalog_opened(self):
        expect(self.page).to_have_url(self.INVENTORY_URL)
        expect(self.catalog.product_cards).to_have_count(6)
        return self

    @allure.step("Проверяем счётчик корзины: {expected}")
    def check_cart_count(self, expected: int):
        if expected == 0:
            expect(self.catalog.cart_badge).not_to_be_visible()
        else:
            expect(self.catalog.cart_badge).to_have_text(str(expected))
        return self

    @allure.step("Проверяем сортировку по имени (обратная: {reverse})")
    def check_names_sorted(self, reverse: bool = False):
        expect(self.catalog.product_names.first).to_be_visible()
        names = self.catalog.get_product_names()
        expect(self.catalog.product_names).to_have_text(sorted(names, reverse=reverse))
        return self

    @allure.step("Проверяем сортировку по цене (обратная: {reverse})")
    def check_prices_sorted(self, reverse: bool = False):
        expect(self.catalog.product_prices.first).to_be_visible()
        prices = sorted(self.catalog.get_product_prices(), reverse=reverse)
        expect(self.catalog.product_prices).to_have_text([f"${p:.2f}" for p in prices])
        return self

    @allure.step("Проверяем, что название и цена совпадают на странице деталей: {product_name}")
    def check_product_details(self, product_name: str):
        name, price, detail_name, detail_price = self.catalog.open_product_details(product_name)
        assert name == detail_name, f"Название не совпадает: {name} != {detail_name}"
        assert price == detail_price, f"Цена не совпадает: {price} != {detail_price}"
        return self
