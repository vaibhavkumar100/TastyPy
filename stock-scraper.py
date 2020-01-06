from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep

# headless Chrome 
opt = Options()
opt.headless = True
opt.add_argument('--log-level=3')
browser = webdriver.Chrome(options=opt)
# browser = webdriver.Chrome()

url = "https://www.investing.com/equities/trending-stocks"
browser.get(url)
sleep(2)

# Close Sign Up Pop Up if appears
try:
    pop_up = browser.find_element_by_css_selector('div#PromoteSignUpPopUp')
    close = pop_up.find_element_by_css_selector('i.popupCloseIcon').click()
except Exception as e:
    pass

# Remove right column from DOM
java_script = "document.getElementById('rightColumn').remove()"
browser.execute_script(java_script)
sleep(2)

link = browser.find_element_by_css_selector("a#timeFrame_local").click()
print()
sleep(3)

# printing trending stocks 
soup = BeautifulSoup(browser.page_source, 'lxml')
trending_stocks = soup.find('div', class_='smallChartsWrapper')
stocks = soup.find_all('div', id="microChartData")
stock_data = []
for stock in stocks:
    company = stock.find('a').text
    last = stock.find('div', class_='bold').text
    change = stock.find('span', class_='bold').text
    change_per = stock.find('span', class_='widthBorder').text
    stock_data.append([company, last, change, change_per])

for data in stock_data:
    print(data)
print()

# printing stocks chart
charts = browser.find_elements_by_class_name('trendingStocksChart')
charts_by = ['by Popularity', 'by Sector']
for chart, by in zip(charts, charts_by):
    print('Trending Stocks', by)
    print()
    series_group = chart.find_element_by_class_name('highcharts-series-group').find_elements_by_class_name('highcharts-series')[0]
    rects = series_group.find_elements_by_tag_name('rect')
    for rect in rects:
        hover = ActionChains(browser)
        hover.move_to_element(rect)
        hover.perform()
        details = chart.find_elements_by_class_name('highcharts-tooltip')[1].text
        print(details)
        print()
        sleep(1)

# printing stocks quotes
btn_list = browser.find_element_by_css_selector('div.js-stock-filter-buttons').find_elements_by_tag_name('a')
for btn in btn_list:
    if btn.text != 'Performance':
        print('\n\n')
        print('Trending Stocks Quotes: ', btn.text)
        btn.click()
        sleep(2)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        table = soup.find('div', id='trendingInnerContent').find('table')
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            print()
            for i in range(len(cells)):
                print(cells[i].text, end='\t')

