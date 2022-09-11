from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import spacy
import icu 
import pandas as pd


def get_words():
    options = Options()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument("window-size=1400,600")
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
    driver.get("https://meduza.io")
    driver.set_window_size(1920,1080)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.Link-root.Link-isInBlockTitle"))).click()

    #search = driver.find_element(By.CLASS_NAME,"Link-isInBlockTitle").accessible_name
    #search.click()

    #article = driver.find_element(By.CSS_SELECTOR, "GeneralMaterial-root.GeneralMaterial-simple.GeneralMaterial-default")
    current_url = driver.current_url

    html_text = requests.get(current_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.select_one('div.GeneralMaterial-article').get_text(' ', strip=True)

    article = news
    driver.quit()

    nlp = spacy.load('ru_core_news_lg')

    regex = re.compile('[^a-zA-Z\ЁёА-я\-ÀàÂâÆæÇçÈèÉéÊêËëÎîÏïÔôŒœÙùÛûÜü]')
    articles = re.sub(regex, ' ', article)

    article = nlp(articles)

    #ADD WORDS TO LIST IF PART OF SPEECH IS A VERB/NOUN/ADJ
    verbs = [token.lemma_ for token in article if token.pos_ == 'VERB']
    nouns = [token.lemma_ for token in article if token.pos_ == 'NOUN']
    adjs = [token.lemma_ for token in article if token.pos_ == 'ADJ']


    #ADD LOCALE TO SORT UNICODE ALPHABETICALLY
    collator = icu.Collator.createInstance(icu.Locale('ru_RU.UTF-8'))
    sorted_verbs = sorted(verbs,key=collator.getSortKey)
    sorted_nouns = sorted(nouns,key=collator.getSortKey)
    sorted_adjs = sorted(adjs,key=collator.getSortKey)

    #REMOVE ANY DUPLICATES FROM SORTED LIST
    final_verbs = list(dict.fromkeys(sorted_verbs))
    final_nouns = list(dict.fromkeys(sorted_nouns))
    final_adjs = list(dict.fromkeys(sorted_adjs))
    final_words = final_adjs + final_nouns + final_verbs

    final_words = list(dict.fromkeys(final_words))


    final_words = pd.DataFrame(final_words, columns=['words'])

    final_words.to_json('words.json', force_ascii=False, orient='records')

if __name__ == "__main__":
    get_words()

  