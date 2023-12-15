from drivers.chromedriver import setDriver
from drivers.multilogindriver import setDriver as multiloginSetDriver, stop_profile as multiloginDestroyDriver
from src.game2048 import game_run
from src.foxnews import fox_news_run
from src.surfing_script import surfing_script_run
from src.surfing_jomashop import surfing_jomashop_run
from src.surfing_ebay import surfing_ebay_run
from src.surfing_macys import surfing_macys_run

import datetime
import sys


if __name__ == '__main__':
    func, profile_id, folder_id = sys.argv[1:]
    start = datetime.datetime.now()
    driver = multiloginSetDriver(profile_id, folder_id)
    driver.get('https://www.google.com')
    try:
        func = globals()[func]
        func(driver)
    except Exception as e:
        print("Error (stack):", e)
    multiloginDestroyDriver(profile_id)
    end = datetime.datetime.now()
    executionTime = end - start

    print("Start time - " + str(start))
    print("End time - " + str(end))
    print("Execution Time - " + str(executionTime))
