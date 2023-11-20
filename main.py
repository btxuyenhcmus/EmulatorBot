from drivers.chromedriver import setDriver
from src.game2048 import game_run
from src.foxnews import fox_news_run
from src.surfing_script import surfing_script_run

import datetime

if __name__ == '__main__':
    start = datetime.datetime.now()
    driver = setDriver()
    driver.get('https://www.google.com')
    surfing_script_run(driver)
    end = datetime.datetime.now()
    executionTime = end - start

    print("Start time - " + str(start))
    print("End time - " + str(end))
    print("Execution Time - " + str(executionTime))
    driver.quit()