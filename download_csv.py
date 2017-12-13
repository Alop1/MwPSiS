import datetime
import re
import requests
from bs4 import BeautifulSoup
import string, os, math, time


# referal link http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/01.10.2017
#              http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/05.10.2017


# TODO wygenerowac tablice linkow dla kazdej stacji {staca : [tablica linkow]} done
# TODO dostac sie do  strony i kliknac export to csv
# TODO obsluzyc zapis

def get_link(start_date, end_date):

    start = datetime.datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.datetime.strptime(end_date, "%d.%m.%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    links_tab = []
    for date in date_generated:
        date = str(date)
        date = date.split(' ', 1)
        date = date[0]
        tem_date = date.split("-")
        date = tem_date[::-1]
        date = ".".join(date)
        # date = date.replace("-", ".")
        links_tab.append("http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/"+date)

    print links_tab
    return links_tab

def click_button(links_tab):
    pass
    ## https://stackoverflow.com/questions/33538600/how-to-automatically-download-the-files-that-have-a-download-button-on-a-webpage
    ## https://stackoverflow.com/questions/11588072/handle-a-file-download-triggered-by-the-click-of-a-button
    ##
    my_folder = 'D:\userdata\lacz\Desktop\temp'

    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from selenium import webdriver
    URL = "http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/05.10.2017"
    profile = FirefoxProfile ()
    profile.set_preference("browser.download.folderList",2)
    profile.set_preference("browser.download.manager.showWhenStarting",False)
    profile.set_preference("browser.download.dir", my_folder)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",'application/pdf')
    profile.set_preference('network.proxy.type',2)
    profile.set_preference('network.proxy.autoconfig_url', "http://proxyconf.glb.nsn-net.net/proxy.pac")
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(URL)
    submit3 = driver.find_element_by_id("table-export-to-csv")
    time.sleep(5)
    submit3.click()


def main():

    links_tab = get_link(start_date= "21.06.2017",end_date = "07.07.2017")
    click_button(links_tab)








if __name__ == "__main__":
    main()
