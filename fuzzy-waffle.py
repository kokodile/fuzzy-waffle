#%%
import requests
from bs4 import BeautifulSoup

alphabet_num = 81
alphabet_index = 0
alphabet_hex = str(hex(int(f'{alphabet_num}',16)+alphabet_index)).upper()[-2:] # 81 -> AE
index = 1

page = requests.get(f"https://dictionary.sanook.com/search/dict-th-th-royal-institute/char/%E0%B8%{alphabet_hex}/{index}")
soup = BeautifulSoup(page.content, 'html.parser')

#%%
soup.find_all('ol')
word_dicts = {}
current_alphabet = 'ก'
word_dicts[alphabet_hex] = soup.find_all('ol')[1].get_text().strip().split('\n')
# %%
def get_last_page(soup):
    navs = soup.find_all('nav', class_="pager")
    for nav in navs:
        max_index = 0
        links = nav.find_all('a')
        for link in links:
            try:
                index = int(link.text)
                if index > max_index:
                    max_index = index
            except ValueError:
                pass
    return max_index
#%%
for alphabet_index in range(0, 45):
    max_index = get_last_page(soup)
    for i in range(2, max_index+1):
        page = requests.get(f"https://dictionary.sanook.com/search/dict-th-th-royal-institute/char/%E0%B8%{alphabet_hex}/{index}")
        soup = BeautifulSoup(page.content, 'html.parser')
        word_dicts[alphabet_hex] += soup.find_all('ol')[1].get_text().strip().split('\n')

    alphabet_index += 1
    alphabet_hex = str(hex(int(f'{alphabet_num}',16)+alphabet_index)).upper()[-2:] # 81 -> AE
    index = 1
    current_alphabet = chr(ord(current_alphabet)+alphabet_index)
    page = requests.get(f"https://dictionary.sanook.com/search/dict-th-th-royal-institute/char/%E0%B8%{alphabet_hex}/{index}")
    print(f"{alphabet_hex} : https://dictionary.sanook.com/search/dict-th-th-royal-institute/char/%E0%B8%{alphabet_hex}/{index}")
    soup = BeautifulSoup(page.content, 'html.parser')
    word_dicts[alphabet_hex] = soup.find_all('ol')[1].get_text().strip().split('\n')
# print(navs[0])
# navs = BeautifulSoup(navs, 'html.parser')
# a = navs.find_all('a')
# print(a)
# %%
dictionary = []
for key, vals in word_dicts.items():
    dictionary += [f'{val}\n' for val in vals]
    # dictionary += vals
# %%
with open('th_words', 'w', encoding='utf-8') as f:
    f.writelines(dictionary)
# import codecs

# with codecs.open("lol", "w", "utf-8") as file:
#     file.write()
# file.close()