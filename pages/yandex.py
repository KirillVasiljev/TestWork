import logging
from pages.basic.elements import Elements
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages.basic.common_methods import Common


class YandexSearchPage(Elements):
    """Главная страница поиска"""

    search_input = Elements.element(By.CSS_SELECTOR, '[id="text"]')
    suggest_popup = Elements.element(By.CSS_SELECTOR, '.mini-suggest__popup')
    search_suggestions = Elements.element(By.CSS_SELECTOR, '.mini-suggest__item')
    search_results = Elements.element(By.CSS_SELECTOR, '[id="search-result"]')
    link_results = Elements.element(By.CSS_SELECTOR, '.Path-Item')
    images_link = Elements.element(By.CSS_SELECTOR, '[data-id="images"]')

    def enter_search_text(self, text: str, do_search: bool = False) -> None:
        """Ввод текста в поле ввода

        :param text: Вводимый тескст
        :param do_search: Нужно ли искать текст
        """

        logging.info(f'Вводим текст: {text}')
        search_input = self.find_element(self.search_input)
        search_input.send_keys(text)
        if do_search:
            self.search()

    def search(self) -> None:
        """Выполнение поиска"""

        logging.info(f'Ищем результаты ввода')
        self.find_element(self.search_input).click()
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def check_link_href(self, expected: str) -> None:
        """
        Проверка ссылки в первом результате поиска
        :param expected: ожидаемая ссылка
        """
        actual_link = self.find_element(self.link_results).get_attribute('href')
        assert expected == actual_link, f'Неожиданный результат: \nожидали {expected}, получили {actual_link}'

    def open_images(self) -> None:
        """
        Переход на вкладку 'Яндекс.Картинки'
        """
        self.find_element(self.images_link).click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        Common(self.driver).check_presence(YandexImagesPage(self.driver).categories)
        assert 'https://yandex.ru/images/' in self.driver.current_url, 'Открыта неверная ссылка'


class YandexImagesPage(Elements):
    """Главная страница поиска"""
    categories = Elements.element(By.CSS_SELECTOR, '.PopularRequestList-Item')
    category_text = Elements.element(By.CSS_SELECTOR, 'PopularRequestList-SearchText')
    category_image = Elements.element(By.CSS_SELECTOR, '.serp-item__preview')
    image_window = Elements.element(By.CSS_SELECTOR, '.MediaViewer-View')
    image = Elements.element(By.CSS_SELECTOR, '.MMImage-Origin')
    button_forward = Elements.element(By.CSS_SELECTOR, '.MediaViewer-ButtonNext')
    button_prev = Elements.element(By.CSS_SELECTOR, '.MediaViewer-ButtonPrev')

    def open_category(self, index: int = 0) -> None:
        """
        Открытие заданной категории
        :param index: Номер категории картинок
        """
        category = self.find_elements(self.categories)[index]
        category_text = self.get_element_from_element(category, self.category_text).text
        category.click()
        Common(self.driver).check_presence(self.category_image)
        search_text = self.find_element(YandexSearchPage(self.driver).search_suggestions).get_attribute('data-text')
        assert category_text.lower() in search_text.lower(), 'Текст в строке поиска не соответствует ожиданиям'

    def open_image(self, index: int = 0) -> None:
        """
        Открытие заданной картинки
        :param index: Номер картинки
        """
        common = Common(self.driver)
        common.check_presence(self.category_image)
        self.find_elements(self.category_image)[index].click()
        common.check_presence(self.image_window)

    def get_image_src(self) -> str:
        """
        Сохранение параметра картинки src в памяти
        :return: Возвращает src картинки
        """
        return self.find_element(self.image).get_attribute('src')

    def open_next_image(self) -> None:
        """Переход к следующей картинке"""
        logging.info('Нажимаем на кнопку вперед')
        self.find_element(self.button_forward).click()

    def open_prev_image(self) -> None:
        """Переход к предыдущей картинке"""
        logging.info('Нажимаем на кнопку назад')
        self.find_element(self.button_prev).click()
