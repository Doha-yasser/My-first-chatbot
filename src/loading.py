import time

import requests
from bs4 import BeautifulSoup
import os 


# Without header, requests uses a default agent like python-requests/2.32.5. Many websites block or send a CAPTCHA to such obvious scripts
Header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


# --------------------------------------------------------------------


# get correct url 
def get_url(pdf_url):
    if pdf_url:
        # should start with http
        if not pdf_url.startswith('http'):
            if pdf_url.startswith('/'):
                pdf_url = "https://www.alarabimag.com" + pdf_url
            else:
                pdf_url = "https://www.alarabimag.com/" + pdf_url
        print(f"PDF URL (fixed): {pdf_url}")
    else:
        print("Not found") 
    return pdf_url



# --------------------------------------------------------------------


# Load page
def load(url):
    print('Fetching page .....')
    response = requests.get(url , headers=Header , timeout=15)
    # get status for response
    response.raise_for_status()
    print('Featched successfully')

    # html to tree obj 
    soup = BeautifulSoup(response.text , 'html.parser')
    # print(soup.prettify()[:600])


    #  load pdf book ----> middle page 
    pdf_url = None 
    book_title = None
    links = soup.find_all('a' , href=True)
    for link in links:
        if 'تحميل' in link.text or 'download' in link.text.lower():
            pdf_url = link['href']
            break


    final_url = get_url(pdf_url)

    
    # print('mmmmmmmmmmm')
    # get name of book
    for element in soup.find_all(['h1', 'h2', 'h3', 'div', 'p']):
        title = element.get_text()
        if 'تحميل رواية' in title:
            book_title = title.split('تحميل رواية')[-1].strip()
            print(f"Book title: {book_title}")
        
    
    print(final_url, book_title)
    return final_url , book_title





# --------------------------------------------------------------------



# download and save book as pdf 
def download_book(pdf_url ,book_title, save_dir = 'Books'):
    #  replace space 
    safe_title = book_title.replace(' ', '_')
    pdf_path = os.path.join(save_dir, f"{safe_title}.pdf")    # build correct path like Books/..


    # check if path exist
    if os.path.exists(pdf_path):
        print(f" Book already exists: {pdf_path}")
        print("Skipping download.")
        return pdf_path 
    


    #  Validate input  (debug)
    if not pdf_url:
        print("No PDF URL provided.")
        return None


    # the middle page 
    pdf_response = requests.get(pdf_url, headers=Header, timeout=15)
    pdf_response.raise_for_status()

    soup_middle = BeautifulSoup(pdf_response.text , 'html.parser')
    pdf_url = None
    links = soup_middle.find_all('a' , href=True)

    # for prepare link
    time.sleep(10)

    for link in links:
        if 'رابط التحميل' in link.text or 'download' in link.text.lower():
            pdf_url = link['href']
            break


    #  if link not found (for debug)
    if not pdf_url:
        print("Could not find the download link on the middle page.")
        return None
    
    final_pdf_url = get_url(pdf_url)



    print(f'Downloading {book_title} ...')
    # check response for the final pdf 
    pdf_response = requests.get(final_pdf_url , headers=Header , timeout=15)
    pdf_response.raise_for_status()

    # create folder if not exist 
    os.makedirs(save_dir, exist_ok=True)


    # save content 
    with open(pdf_path, 'wb') as f:
        f.write(pdf_response.content)

    
    print(f"PDF saved to: {pdf_path}")
    return pdf_path

