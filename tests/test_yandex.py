import logging

from pages.yandex import YandexSearchPage, YandexImagesPage
from pages.basic.common_methods import Common


def test_yandex_search(driver):
    """Поиск в яндексе"""
    driver.get('http://www.yandex.ru/')
    yandex_page = YandexSearchPage(driver)
    common = Common(driver)
    logging.info('Нажимаем на кнопку вперед')
    common.check_presence(yandex_page.search_input)
    yandex_page.enter_search_text('Тензор')
    common.check_presence(yandex_page.suggest_popup)
    yandex_page.search()
    common.check_presence(yandex_page.search_results)
    yandex_page.check_link_href('https://tensor.ru/')


def test_yandex_images(driver):
    """Картинки на яндексе"""
    driver.get('http://www.yandex.ru/')
    yandex_page = YandexSearchPage(driver)
    common = Common(driver)
    common.check_presence(yandex_page.images_link)
    yandex_page.open_images()
    images = YandexImagesPage(driver)
    images.open_category()
    images.open_image()
    first_image_src = images.get_image_src()
    images.open_next_image()
    second_image_src = images.get_image_src()
    assert first_image_src != second_image_src, 'Картинка не изменилась'
    images.open_prev_image()
    assert images.get_image_src() == first_image_src, 'Не отобразилась первая картинка'
