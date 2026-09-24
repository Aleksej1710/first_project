from playwright.sync_api import Page

from src.main.ui.pages.catalog_page import CatalogPage


class CheckoutCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator("[data-test='complete-text']")
        self.back_home_button = page.locator("[data-test='back-to-products']")
        self.generate_pdf_button = page.locator("[data-test='generate-pdf-order']")

    def back_home(self):
        self.back_home_button.click()
        return CatalogPage(self.page)

    def generate_pdf(self):
        with self.page.expect_download() as download_info:
            self.generate_pdf_button.click()
        return download_info.value