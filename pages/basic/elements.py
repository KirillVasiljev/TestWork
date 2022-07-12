import logging
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Elements:
    """Поиск элементов"""
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, element: dict) -> WebElement:
        """Обертка для поиска элементов

        :param element: Словарь с локатором элемента
        """

        start_time = time.time()
        while True:

            try:
                elements = self.driver.find_element(element['how'], element['locator'])
                return elements
            except NoSuchElementException:
                logging.warning(f"Не найден элемент '{element['locator']}'")
            time.sleep(1)

            if time.time() - start_time >= 10:
                break

        raise NoSuchElementException()

    def find_elements(self, element: dict) -> list:
        """Обертка для поиска элементов

        :param element: Словарь с локатором элемента
        """

        try:
            elements = self.driver.find_elements(element['how'], element['locator'])
            return elements
        except NoSuchElementException:
            raise NoSuchElementException(logging.warning(f"Не найден элемент" 
                                                         f" '{element['locator'], element['rus_name']}'"))

    @staticmethod
    def get_element_from_element(parent: WebElement, element_to_find: dict) -> WebElement:
        """
        Найти дочерний элемент от другого элемента
        :param parent: родительский элемент
        :param element_to_find: дочерний элемент
        :return: дочерний элемент
        """
        element = parent.find_element(By.CLASS_NAME, element_to_find['locator'])
        return element

    @staticmethod
    def element(how=By.CSS_SELECTOR, locator: str = '') -> dict:
        """Создание словоря с данными для поиска элементов

        :param how: стратегия поиска
        :param locator: локатор
        """
        element = {'how': how, 'locator': locator}
        return element
