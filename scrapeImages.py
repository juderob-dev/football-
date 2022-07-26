import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import io
import os
import time
import bs4
from PIL import Image
import hashlib
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageFile as I_mage
from time import sleep
import PIL



def fetch_image_urls(query:str,max_links_to_fetch,wd:webdriver,sleep_between_interactions:float=100):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)
    search_url="https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=query))
    image_urls=set()
    image_count = 0
    results_start=0
    while image_count<max_links_to_fetch:
        scroll_to_end(wd)
        # page_html = wd.page_source
        # pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        # thumbnail_results = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
        thumbnail_results=wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results=len(thumbnail_results)
        print(f"found:{number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:number_results]:
        #for i in range(results_start+1,number_results+1):
            #xPath = """//*[@id="islrg"]/div[1]/div[%s]""" % (i)
            #print(i)

            try:

                #wd.find_element_by_xpath(xPath).click()

                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue


            #previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img""" % (i)
            #previewImageElement= wd.find_element_by_xpath(previewImageXPath)




            #previewImageURL = previewImageElement.get_attribute("src")
           # page_html = wd.page_source
            #actual_images = wd.find_elements_by_css_selector('img.n3VNCB')

            #first_image = img.find_elements_by_xpath('//*[@data-noaft="1"]')[0]
            #magic_class = first_image.get_attribute('class')
            #image_finder_xp = f'//*[@class="{magic_class}"]'

            actual_images = wd.find_elements(by=By.CSS_SELECTOR, value="img.n3VNCb")
            #actual_images =wd.find_elements_by_xpath(image_finder_xp)
            #print(magic_class,"yes")
           # actual_images = wd.find_elements_by_xpath("//img[contains(@class,'Q4LuWd')]")
            #actual_images =  wd.find_element_by_xpath(".//div[@class='visual']/div[@class='col-sm-6']//img[@class='color-frame']")

            #actual_images = wd.find_element_by_class_name('n3VNCb')

            #timeStarted = time.time()

            # while True:
            #     print("yes")
            #
            #     actual_image = wd.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
            #     imageURL = actual_image.get_attribute('src')
            #
            #     if imageURL != previewImageURL:
            #         image_urls.add(imageURL)
            #
            #
            # #        print("actual URL", imageURL)
            #         break
            #
            #
            #     else:
            #         # making a timeout if the full res image can't be loaded
            #         currentTime = time.time()
            #
            #         if currentTime - timeStarted > 10:
            #             print("Timeout! Will download a lower resolution image and move onto the next one")
            #             break




            for actual_image in actual_images:


                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
            image_count = len(image_urls)
            if len(image_urls)>=max_links_to_fetch:
                print(f"Found:{len(image_urls)} image links, done!")
                break
        if len(image_urls)<max_links_to_fetch:
            print("Found:", len(image_urls),"image links, looking for more .. ")
            time.sleep(30)

            load_more_button = wd.find_elements_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        results_start = len(thumbnail_results)
    return image_urls




image_URL="https://www.arsenal.com/sites/default/files/styles/desktop_16x9/public/images/Odegaard%20WBA.png?itok=UQBbJdLt"
def download_image(folder_path,url):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download{url} - {e}")

    try:

        image_file=io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] +'.jpg')
        #file_path=downloadPath + fileName # this was teh orignial file path method
        with open(file_path, "wb") as f:
            image.save(f,"JPEG", quality=85)
        print("Success -saved {url} - as {file_path}")
    except Exception as e:
        print(f"Failed -could not save{url}-{e}")

def search_and_download(search_term:str,driver_path:str,target_path='./images',number_images=500):
    target_folder= os.path.join(target_path,'_'.join(search_term.lower().split(' ')))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    with webdriver.Chrome(chrome_options=Options(), executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term,number_images, wd=wd, sleep_between_interactions=0.5)

    for elem in res:
        download_image(target_folder,elem)

#download_image("C:\\Users\\Jude_\\OneDrive\\Documents\\University project\\university project\\images\\odegaard", image_URL,"test.jpg")

def scrapeImage(searchTerm):
    downloadPath = "C:\\Users\\Jude_\\Documents\\University_Project\\images"
    PATH = "C:\\Users\\Jude_\\OneDrive\\Documents\\University project\\chromedriver_win32\\chromedriver.exe"
    wd = webdriver.Chrome(PATH)

    search_and_download(searchTerm, PATH, downloadPath)

if __name__ =="__main__":
    wholeteam={'1': {'NO.': '1', 'pos.': 'GK', 'Nation': 'GER', 'Player': 'Bernd Leno'}, '3': {'NO.': '3', 'pos.': 'DF', 'Nation': 'SCO', 'Player': 'Kieran Tierney (vice-captain)'}, '4': {'NO.': '4', 'pos.': 'DF', 'Nation': 'ENG', 'Player': 'Benjamin White'}, '5': {'NO.': '5', 'pos.': 'MF', 'Nation': 'GHA', 'Player': 'Thomas Partey'}, '6': {'NO.': '6', 'pos.': 'DF', 'Nation': 'BRA', 'Player': 'Gabriel Magalhaes'}, '7': {'NO.': '7', 'pos.': 'MF', 'Nation': 'ENG', 'Player': 'Bukayo Saka'}, '8': {'NO.': '8', 'pos.': 'MF', 'Nation': 'NOR', 'Player': 'Martin Ødegaard (3rd captain)'}, '9': {'NO.': '9', 'pos.': 'FW', 'Nation': 'FRA', 'Player': 'Alexandre Lacazette (captain)'}, '10': {'NO.': '10', 'pos.': 'MF', 'Nation': 'ENG', 'Player': 'Emile Smith Rowe'}, '16': {'NO.': '16', 'pos.': 'DF', 'Nation': 'ENG', 'Player': 'Rob Holding (4th captain)'}, '17': {'NO.': '17', 'pos.': 'DF', 'Nation': 'POR', 'Player': 'Cédric Soares'}, '18': {'NO.': '18', 'pos.': 'DF', 'Nation': 'JPN', 'Player': 'Takehiro Tomiyasu'}, '19': {'NO.': '19', 'pos.': 'FW', 'Nation': 'CIV', 'Player': 'Nicolas Pepe'},
               '20': {'NO.': '20', 'pos.': 'DF', 'Nation': 'POR', 'Player': 'Nuno Tavares'}, '23': {'NO.': '23', 'pos.': 'MF', 'Nation': 'BEL', 'Player': 'Albert Sambi Lokonga'}, '25': {'NO.': '25', 'pos.': 'MF', 'Nation': 'EGY', 'Player': 'Mohamed Elneny'}, '30': {'NO.': '30', 'pos.': 'FW', 'Nation': 'ENG', 'Player': 'Eddie Nketiah'}, '32': {'NO.': '32', 'pos.': 'GK', 'Nation': 'ENG', 'Player': 'Aaron Ramsdale'}, '33': {'NO.': '33', 'pos.': 'GK', 'Nation': 'ENG', 'Player': 'Arthur Okonkwo'}, '34': {'NO.': '34', 'pos.': 'MF', 'Nation': 'SUI', 'Player': 'Granit Xhaka'}, '35': {'NO.': '35', 'pos.': 'FW', 'Nation': 'BRA', 'Player': 'Gabriel Martinelli'}}


    downloadPath = "C:\\Users\\Jude_\\Documents\\University_Project\\images"
    PATH = "C:\\Users\\Jude_\\OneDrive\\Documents\\University project\\chromedriver_win32\\chromedriver.exe"
    #wd = webdriver.Chrome(PATH)
    # searchTerm="Leno_arsenal"
    # search_and_download(searchTerm, PATH, downloadPath)
    for key,val in wholeteam.items():
       print(key,val['Player'])
       name=val['Player'].split("(")
       searchTerm=name[0]+" Arsenal"
       scrapeImage(searchTerm)




