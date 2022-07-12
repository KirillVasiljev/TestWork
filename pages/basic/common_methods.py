import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.basic.elements import Elements


class Common(Elements):
    """Базовые методы"""

    def check_presence(self, element: dict) -> None:
        """Проверяем отображение элемента на странице

        :param element: элемент, которого ждем
        """

        logging.debug('Проверям отображение элемента')
        wait = WebDriverWait(self.driver, 10)
        element = self.find_element(element)
        wait.until(EC.visibility_of(element), 'Не отображается элемент')
