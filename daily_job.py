import os
from dotenv import load_dotenv
from db import DB
import requests
import datetime
from bs4 import BeautifulSoup
import threading
import time
start = time.time()
load_dotenv()
# get db
imdb = DB(os.getenv('HOST'), os.getenv('UUID'), os.getenv('DBNAME'), os.getenv('PASSWORD'))
# http request session
s = requests.Session()

# due day
start_date = datetime.date(2016, 1, 1)
end_date = datetime.date(2016, 1, 2)
# end_date = datetime.date(2022, 1, 25)
delta = datetime.timedelta(days=1)



def getlink(s, date):
    # print('scarping: ' + str(date))
    data = {
        'title_type': 'feature',
        'release_date': date,
        'count': 250
    }

	#Get IMDB Path
    # https://www.imdb.com/search/title/?title_type=feature&release_date=2022-06-01&count=250
    # lister-item.mode-advanced

    response = s.post('https://www.imdb.com/search/title/?', data=data)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    formalist = soup.select('div.lister-item-content')
    mvlist = []
    for mv in formalist:
        header = mv.select_one('h3.lister-item-header a').getText()
        link = mv.select_one('h3.lister-item-header a').get("href")
        runtime = mv.select_one('span.runtime')
        if runtime != None:
            runtime = runtime.getText()
        else:
            runtime = 'Null'
        mvtype = mv.select_one('span.genre')
        if mvtype != None:
            mvtype = mvtype.getText().strip('\n').strip(' ')
        else:
            mvtype = 'Null'

        mvlist.append({'header': header, 'link': link, 'runtime': runtime, 'type': mvtype})
        
    return mvlist

# def scrapToDatabase(movie):
#     print(scrapToDatabase)

# movie list
movieList = []

# Main progress
def getLinkJob(s, date):
    global movieList
    print('Getting ' + str(date) + ' IMDB movie data')
    movieList.extend(getlink(s, date))
    print(str(date) + ' done!')

# Get movie data in detail page and merge data
def getDetailJob(s, mv):
    global imdb
    mvinfo = {}
    mvdetail = s.post('https://www.imdb.com' + mv['link'])
    res = mvdetail.text
    mvsoup = BeautifulSoup(res, "html.parser")
    actorlist = mvsoup.select('a.sc-36c36dd0-1')
    characterlist = mvsoup.select('span.sc-36c36dd0-4')
    information = mvsoup.select('div.sc-388740f9-0')
    actors = ''
    characters = ''
    for name in actorlist:
        actors+=(name.getText() + ', ')
    for name2 in characterlist:
        characters+=(name2.getText() + ', ')
    mvinfo['title'] = mv['header']
    mvinfo['id'] = mv['link']
    mvinfo['poster'] = mvsoup.select_one('div.ipc-media img').get('src')
    mvinfo['trailer'] = 'https://www.imdb.com' + mvsoup.select_one('div.ipc-slate a').get('href')
    if not mvinfo['trailer'].__contains__('https://www.imdb.com/video'):
        mvinfo['trailer'] = 'Null'
    mvinfo['runtime'] = mv['runtime']
    mvinfo['actors'] = actors
    mvinfo['characters'] = characters
    mvinfo['storyline'] = mvsoup.select_one('span.sc-16ede01-2').getText()
    #mvinfo['storyline2'] = information.select_one('div.ipc-html-content-inner-div').getText()
    # mvinfo['releaseDate'] = str(date)
    # ...

    #print(mvinfo['characters'])
    imdb.cur.execute("INSERT INTO movies (title, link, runtime, type, imdb_id, poster, trailer, actors, characters, storyline) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
    (mvinfo['title'], mv['link'], mv['runtime'], mv['type'], mvinfo['id'], mvinfo['poster'], mvinfo['trailer'], mvinfo['actors'], mvinfo['characters'], mvinfo['storyline']))
    # print(mvinfo.keys())

threads = []
while start_date <= end_date:
  threads.append(threading.Thread(target = getLinkJob, args = (s, start_date)))
  threads[-1].start()
  start_date += delta
  time.sleep(1)

# 等待所有子執行緒結束
for t in threads:
  t.join()

detailThreads = []
for movie in movieList:
    detailThreads.append(threading.Thread(target = getDetailJob, args = (s, movie)))
    detailThreads[-1].start()
    time.sleep(1)

# 等待所有子執行緒結束
for t in detailThreads:
  t.join()


imdb.close()

# print(len(threads), " days")
# print(len(detailThreads), " movies")
end = time.time()
print('time count ', end - start)