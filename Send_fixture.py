#import the webdriver from selenium package
from selenium import webdriver
#import the keys class from selenium package
from selenium.webdriver.common.keys import Keys
import time

# msg = {'dictionary':1, 'test': 2}
contact = input('enter persons name: ')
#initialize the web driver variable
driver = webdriver.Chrome(executable_path = r"C:/Users/Dave/Webdrivers/chromedriver.exe") #give the path of the web driver in the string
time.sleep(2)
#browse to a whatsapp web
driver.get(r"https://web.whatsapp.com") 
time.sleep(2)
#control the contact search textbox
user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(contact))
user.click()

#Now the contact opens and a new textbox is created, so we need to execute this line once again to read the new textbox
search=driver.find_elements_by_class_name(r"_2Evw0")
time.sleep(2)

attach = driver.find_element_by_xpath(r'//*[@title = "Attach"]')
attach.click()

dialog=driver.find_element_by_tag_name(r"input")

#send a file to open dialog
dialog.send_keys(r"C:/Users/Dave/Python/Python Scripts/Halo/Fixtures.xlsx") #this string contains the path of the file to be uploaded
#NOTE: if the file is large, then upload time will be high. If it takes some time to upload, then the preview window also takes some time to load
#so, its better to ask the program to wait
#this is done by the following code

time.sleep(2) #wait for 2 secs
#this step is not required when you execute the code step by step

#after the upload is completed, a preview window is opened
#in the preview window, there is a send button
#the below code controls the send button
but=driver.find_element_by_class_name(r"_3Git-")

#click the send button
but.click()