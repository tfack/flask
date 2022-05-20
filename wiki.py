import requests

def find_titles(movieTitle):
    url = f"https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/{movieTitle}"
    response = requests.get(url)

    data = response.json()
    results = data['results']

    return results

# def srchIMDB(srch_str): 
#     url = "https://imdb-api.com/en/API/SearchMovie/k_z7g2vpw7/" + srch_str
    
#     payload = {}
#     headers= {}
    
#     response = requests.request("GET", url, headers=headers, data = payload)
#     data=response.json()

#     # print(data)
#     print(response.text.encode('utf8'))    

# def findBirths(monthDay,year,size=10):
#     #monthDay is in form "mm/dd"
#     #year is in form "yyyy"
#     #returns a list of names, birth years and thumbnails 
#     #sortedbyClosestYear[i]['text'] has name of ith match
#     #sortedbyClosestYear[i]['year'] has year of ith match's birthdate
#     #sortedbyClosestYear[i]['thumbnail'] has url of ith match's thumbnail picture or localhost if there is none
#     size=int(size)
#     year=int(year)
#     path="https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"
#     response=requests.get(path+"/births/"+monthDay)
#     data=response.json()
#     sortedbyClosestYear=sorted(data["births"], key=lambda i: abs(int(i['year'])-year))
#     if len(sortedbyClosestYear) > size:
#         sortedbyClosestYear=sortedbyClosestYear[0:size]
#     for item in sortedbyClosestYear:
#         item['thumbnail']="localhost"
#         if "thumbnail" in item['pages'][0]:
#             item['thumbnail']=item['pages'][0]["thumbnail"]["source"]
#     return sortedbyClosestYear

if __name__ == "__main__":

    tmp = find_titles("Stranger")    
    
    # for key, value in tmp.items():
    #     print(key)
    #     print(value)
  
    # tmp = findBirths("07/16","1973",10)

    # for i in range(len(tmp)):
    #     print(tmp[i]["text"], tmp[i]["year"])

    # text, pages [type, title, displaytitle, namespace [id, text], wikibase_item, titles [canonical, normalized, display],
    # pageid, thumbnail [source, width, height], originalimage [source, width, height, lange, dir, revision, tid, timestamp,
    # description, description_source, content_urls [desktop [page, revisions, edit, talk], mobile [page, revisions, edit,
    # talk]], extract, year, thumbnail

