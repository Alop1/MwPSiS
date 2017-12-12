import datetime

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
        link_tabs.append("http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/parametr/pm10/stacje/1723/dzienny/"+date)

    print links_tab
    return links_tab


def main():

    # dateList = []
    # numdays = 100
    # base = datetime.datetime.today()
    # date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    # print "daty", date_list[0]
    # single_date = date_list[0]
    # print single_date

    links_tab = get_link(start_date= "21.06.2017",end_date = "07.07.2017")








if __name__ == "__main__":
    main()
