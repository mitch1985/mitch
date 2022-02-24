from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import timeit
#Timer Starts
start = timeit.default_timer()

chrome_options = Options()
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="D:\\Programmieren\\chromedriver.exe")
# go to Indeed.com

driver.get("https://www.indeed.com")
driver.maximize_window()


driver.find_element_by_xpath("//*[@id='text-input-what']").send_keys("Selenium")
#Timer Stops
stop = timeit.default_timer()
#Prints the Start and End Time to Console
print('Time: ', stop - start)