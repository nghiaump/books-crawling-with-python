import re
import requests
from bs4 import BeautifulSoup

def create_tracks(keyword, page):
    url = 'http://libgen.rs/search.php?&res=100&req={k}&phrase=1&view=simple&column=def&sort=year&sortmode=DESC&page={p}'.format(k=keyword, p=page)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    attrs = {'href':re.compile("http://library.lol/main/")}
    tracks = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))
    return tracks

def get_link(mirror):
    html_text = requests.get(mirror).text
    soup = BeautifulSoup(html_text, 'html.parser')
    attrs = {'href':re.compile("http://31.42.184.140/main/")}
    track = soup.find('a', attrs=attrs)
    link = track.attrs['href']
    filename = soup.find('h1').text
    return (filename, link)

def create_links(tracks):
    links = []
    for track in tracks:
        try:
            if type(track) == 'NoneType':
                continue
            elif 'href' in track.attrs:
                links.append(track.attrs['href'])
        except:
            continue
    return links
                

def download(path,info,count):
    # info is a tupple(filename, link)
    link = info[1]
    filename = info[0]

    # standardize filename
    invalid = '<>:"/\|?*'
    for char in invalid:
        filename = filename.replace(char, '_')        
    filename = path + filename + ' _' + str(count) + '.' + link.split('.')[-1]

    # Download file
    print("Downloading " + filename)
    r = requests.get(link, allow_redirects=True)
    with open(filename, 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    count = 0
    k = str(input('input keyword: '))
    num = int(input('number of books x 100: '))
    skip = int(input('number of downloaded book(s): '))
    path = str(input('input path: '))
    for i in range(1, num+1):
        print("Page ", i)
        tracks = create_tracks(k, i)
        links = create_links(tracks)
        for link in links:
            count += 1
            if count <= skip:
                continue
            info = get_link(link)
            download(path, info, count)
            


