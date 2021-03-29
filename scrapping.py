import os
import re
import sys
import time
import datetime
import requests

from bs4 import BeautifulSoup
from os.path import basename
from sys import exit
from video import Joinvideo, Joinsong

'''
    Ex: url='https://www.boredpanda.com/black-and-white-celebrity-photos-colorized-machine-learning-deepai-hidreley'
'''

base_dir = os.path.dirname(__file__)
os_sep = os.sep

input_dir = f'''{base_dir}{os.sep}input{os.sep}'''
output_dir = f'''{base_dir}{os.sep}output{os.sep}'''

urls = []

def txt():
    with open('lists.txt', 'r') as txt:
        for lines in txt:
            urls.append(lines)
    return urls

def scrapping(url):
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
    except Exception as e:
        return f'''We have an error: {e}'''

    soup = BeautifulSoup(page.content, 'html.parser')
    
    title_folder = soup.select('h1.post-title')[0].text.strip()
    title_folder_cleaned = re.sub('[^A-Za-z0-9 ]+',' ', title_folder)
    title_folder_cleaned_ = title_folder_cleaned.replace(' ','_')
    _filename = f'''{input_dir}{title_folder_cleaned_}{os_sep}'''

    if not os.path.exists(_filename):
        os.makedirs(_filename, exist_ok=True)
    else:
        pass

    if not [files for files in os.listdir(_filename)]:
        n = 0

        results_1 = soup.find('div', class_='post-content')
        results_2 = soup.find('div', class_='open-list-items')
        
        if results_1:
            results_1_ = results_1.find('div', class_='open-list-items')
            if results_1_:
                imgs = results_1_.find_all('img',class_='image-size-full',src=True)
                for img in imgs:
                    n += 1
                    i = img.get('src')
                    title = img.get('alt')
                    # t = re.sub('[^A-Za-z0-9 \.\()\-]+',' ',str(title))
                    title = title.replace("'","’")
                    title = title.replace('"',"“")
                    # t = re.sub('''[/\?:*<>"|]+''',' ',str(title))
                    
                    if title:
                        with open(_filename + str(n) +'.jpg', "wb") as s:
                            try:
                                with open(f'{_filename}titles.txt', 'a') as _f:
                                    _f.write(f'''{n}. {title}\n''')
                                s.write(requests.get(i).content)
                            except Exception as e:
                                print("We have an error: ", e)
                                pass
                    else:
                        with open(_filename + str(n) +'.jpg', "wb") as s:
                            try:
                                with open(f'{_filename}titles.txt', 'a') as _f:
                                    _f.write(f'{n}.「 No title 」\n')
                                s.write(requests.get(i).content)
                            except Exception as e:
                                print("We have an error: ", e)
                                pass
            else:
                return f"We can't find class 'open-list-item'"
        elif results_2:
            imgs = results_2.find_all('img', class_='image-size-full',src=True)
            
            for img in imgs:
                i = img.get('src')
                title = img.get('alt')
                t = re.sub('[^A-Za-z0-9 ]+',' ', title)
                t = t.replace(' ','_')
                
                if (os.path.exists(_filename + t + '.jpg')):
                    n += 1
                    with open(_filename + t + ' %d.jpg' % n, "wb") as s:
                        try:
                            s.write(requests.get(i).content)
                        except Exception as e:
                            print("We have an error: ", e)
                            pass
                else:
                    with open(_filename + t + '.jpg', "wb") as s:
                        try:
                            s.write(requests.get(i).content)
                        except Exception as e:
                            print("We have an error: ", e)
                            pass   
        else:
            print(f"Can't find class 'open-list-items' or 'post-content'. \
                    Please re-check the link: ")
            print(url)
    else:
        pass

    
if __name__ == "__main__":
    # scrapping(sys.argv[1])
    txt()

    for url in urls:
        scrapping(url)
    




