import datetime
import string, os, math, time
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
import os
import glob


# referal link http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/01.10.2017
#              http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/05.10.2017


# TODO wygenerowac tablice linkow dla PM10 PM2.5 done
# TODO dostac sie do  strony i kliknac export to csv - done
# TODO obsluzyc zapis - dane

def get_link(start_date, end_date, PM10='', PM25='' ):
    ##46-1747-1921-1914-1752-148-1723-57 - stacje PM10 KRakow
    ##..parametr/pm2.5/stacje/202-242-211-1911/.../10.2017 -  stacje PM2.5 krakow
    print "PM10 -> ", PM10
    print "PM25 -> ", PM25


    ## dusts = (PM10 if PM10 else PM25)
    ## print dusts


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
        if PM10:
            links_tab.append("http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/"+PM10+"/dzienny/"+date)
        else:
            links_tab.append("http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm2.5/stacje/"+PM25+"/dzienny/"+date)

    print links_tab
    return links_tab

def click_button(links_tab):
    pass
    ## https://stackoverflow.com/questions/33538600/how-to-automatically-download-the-files-that-have-a-download-button-on-a-webpage
    ## https://stackoverflow.com/questions/11588072/handle-a-file-download-triggered-by-the-click-of-a-button
    ##
    my_folder = 'D:\userdata\lacz\Desktop\\temp\WIOS\\'  # wybrac folder !!!!!
    URL = "http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/05.10.2017"
    profile = FirefoxProfile()
    profile.set_preference("browser.download.folderList",2)
    profile.set_preference("browser.download.manager.showWhenStarting",False)
    profile.set_preference("browser.download.dir", my_folder)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",'text/csv')
    profile.set_preference('network.proxy.type',2)
    profile.set_preference('network.proxy.autoconfig_url', "http://proxyconf.glb.nsn-net.net/proxy.pac")
    driver = webdriver.Firefox(firefox_profile=profile)

    for link in links_tab:
        driver.get(link)
        submit3 = driver.find_element_by_id("table-export-to-csv")
        time.sleep(2)
        submit3.click()
        time.sleep(1)
        assign_name(my_folder, link)


def assign_name(my_folder, link):
    date = link[-10:]
    date = date.replace(".", "-")
    date = date + ".csv"
    date = str(date)
    os.chdir(my_folder)
    files = glob.glob('*.csv')
    latest_file = max(files, key=os.path.getctime)
    os.rename(latest_file, date)




def main():
    PM10_stations = "46-1747-1921-1914-1752-148-1723-57"
    PM25_stations = "202-242-211-1911"

    # links_tab = get_link(start_date="21.06.2016", end_date="07.07.2017", PM10=PM10_stations)
    links_tab = get_link(start_date="22.06.2017", end_date="07.07.2017", PM25=PM25_stations)
    click_button(links_tab)


if __name__ == "__main__":
    main()
