async def scrap(link):
    from bs4 import BeautifulSoup
    import requests
    import lxml

    res = requests.get(link)
    soup = BeautifulSoup(res.text, "lxml")

