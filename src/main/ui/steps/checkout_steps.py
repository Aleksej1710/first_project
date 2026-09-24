import allure
from playwright.sync_api import Page, expect
from src.main.ui.pages.checkout_information_page import CheckoutInformationPage


class CheckoutSteps:
    """Шаги оформления заказа: форма → обзор → завершение.

    Страница формы создаётся в __init__, а обзор и завершение приходят
    из возвратов методов-переходов (submit() → overview, finish() → complete).
    """

    def __init__(self, page: Page):
        self.page = page
        self.information = CheckoutInformationPage(page)
        self.overview = None
        self.complete = None

    # ---------- Форма ----------

    @allure.step("Проверяем, что открыта форма оформления")
    def check_information_opened(self):
        expect(self.information.continue_button).to_be_visible()
        return self

    @allure.step("Начинаем Checkout: {first_name} {last_name}, индекс '{postal_code}'")
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.information.fill_form(first_name, last_name, postal_code)
        expect(self.information.first_name_input).to_have_value(first_name)
        expect(self.information.last_name_input).to_have_value(last_name)
        expect(self.information.postal_code_input).to_have_value(postal_code)
        self.overview = self.information.submit()
        return self

    @allure.step("Проверяем текст ошибки: {expected}")
    def check_error(self, expected: str):
        expect(self.information.error_message).to_have_text(expected)
        return self

    # ---------- Обзор ----------

    @allure.step("Проверяем, что открыт обзор заказа")
    def check_overview_opened(self):
        expect(self.overview.total_label).to_be_visible()
        expect(self.overview.finish_button).to_be_visible()
        return self

    @allure.step("Проверяем Item total: {expected}")
    def check_subtotal(self, expected: float):
        subtotal = self.overview.get_subtotal()
        assert subtotal == expected, f"Item total {subtotal} != сумме корзины {expected}"
        return self

    @allure.step("Проверяем, что Total = Item total + Tax")
    def check_total(self):
        subtotal = self.overview.get_subtotal()
        tax = self.overview.get_tax()
        total = self.overview.get_total()
        assert total == round(subtotal + tax, 2), f"Total {total} != {subtotal} + {tax}"
        return self

    @allure.step("Завершаем Checkout")
    def finish_checkout(self):
        self.complete = self.overview.finish()
        return self

    # ---------- Завершение ----------

    @allure.step("Проверяем, что заказ оформлен")
    def check_complete_opened(self):
        expect(self.complete.title).to_have_text("Checkout: Complete!")
        expect(self.complete.complete_header).to_have_text("Thank you for your order!")
        expect(self.complete.back_home_button).to_be_visible()
        return self

    @allure.step("Скачиваем PDF заказа и проверяем файл")
    def check_pdf_downloaded(self):
        download = self.complete.generate_pdf()
        name = download.suggested_filename
        assert name.startswith("swag-labs-order-"), f"Неожиданное имя файла: {name}"
        assert name.endswith(".pdf"), f"Неожиданное расширение: {name}"
        with open(download.path(), "rb") as f:
            assert f.read(4) == b"%PDF", "Файл не является PDF"
        return self
