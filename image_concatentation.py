import io

from PIL import Image
from selenium.webdriver.chrome import webdriver


def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


if __name__ == '__main__':
    driver = webdriver.WebDriver('resources/chromedriver.exe')
    driver.maximize_window()
    driver.get('https://chromedriver.chromium.org/capabilities')
    slices = []
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    size = driver.get_window_size()
    current_height = 0
    window_height = size['height']
    slices.append(driver.get_screenshot_as_png())
    current_height += window_height

    while current_height + window_height < scroll_height:
        driver.execute_script(f'window.scrollTo(0, {current_height + 1})')
        slices.append(driver.get_screenshot_as_png())
        current_height += window_height

    remaining_height = scroll_height - current_height

    if remaining_height > 0:
        driver.execute_script(f'window.scrollTo(0, '
                              f'{current_height + remaining_height + 1})')
        current_slice = driver.get_window_rect()
        slices.append(driver.get_screenshot_as_png())

    max_index = len(slices) - 2
    current_index = 0
    is_1 = io.BytesIO(slices[current_index])
    im_1 = Image.open(is_1)

    for current_index in range(max_index + 1):
        is_2 = io.BytesIO(slices[current_index + 1])
        im_2 = Image.open(is_2)

        im_1 = get_concat_v(im_1, im_2)

    im_1.save('output/test.png')
