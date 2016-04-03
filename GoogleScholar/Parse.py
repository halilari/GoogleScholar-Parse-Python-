from bs4 import BeautifulSoup
import requests
import html5lib
import lxml
import webbrowser
import urllib3
import time
import random
from Author import Author
import hashlib
import os
import urllib


_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_SCHOLARHOST="https://scholar.google.com.tr"
_AUTHSEARCH = '/citations?view_op=search_authors&hl=en&mauthors='
_NEXTLINK="&cstart="
_PAGESIZE=20
pagelink=""
alintiliste=[]
yilliste=[]
_PUBSTART=0


def authorSearch(Author):
    time.sleep(5+random.uniform(0, 5))
    url=requests.get(_SCHOLARHOST+_AUTHSEARCH+Author.getAdiSoyadi(),headers=_HEADERS, cookies=_COOKIES)
    print(url.url)
    if url.status_code==200:
       print("Bağlantı Sağlandı!!!")
       soup=BeautifulSoup(url.content, "html.parser")
       if(soup.find("div","gs_med")):
            print("Böyle Bir Kullanıcı Yoktur...")
            return
       a=soup.find("h3","gsc_1usr_name")
       link=a.find("a").get("href")
       print(link)
    else:
       print("Siteye Erişim Sağlanamadı...")
       return
    return link

yazar=Author("ecir")
pagelink=authorSearch(yazar)

yil=2009

def authorArticle(pagelink,yil):
    global _PUBSTART
    global _PAGESIZE
    url=requests.get(_SCHOLARHOST+pagelink+_NEXTLINK+str(_PUBSTART)+"&pagesize="+str(_PAGESIZE),headers=_HEADERS, cookies=_COOKIES)
    print(url.url)
    if url.status_code==200:
        soup=BeautifulSoup(url.content,"html.parser")
        for i in soup.find_all("tr", class_="gsc_a_tr"):
            for j in i.find("td",class_="gsc_a_c"):
                 for k in i.find("td", class_="gsc_a_y"):
                      if k.text is not "":
                          if int(k.text)>yil:
                             yazar.Makaleleri.append(i.find("a").text)
                             yilliste.append(k.text)
                             alintiliste.append(j.text)

        if 'disabled' not in soup.find('button', id='gsc_bpf_next').attrs:
            _PUBSTART+=_PAGESIZE
            authorArticle(pagelink,yil)



def authorPage(pagelink):
    url=requests.get(_SCHOLARHOST+pagelink,headers=_HEADERS, cookies=_COOKIES)
    print(url.url)
    if url.status_code==200:
        print("Yazar Sayfasına Ulaşıldı")
        soup=BeautifulSoup(url.content, "html.parser")
        yazar=Author
        ad=soup.find("div", id="gsc_prf_in").text.upper()
        yazar.setAdiSoyadi(ad)
        print(soup.find("div", id="gsc_prf_in").text.upper())
        yazar.CalismaYeri=soup.find("div", class_="gsc_prf_il").text
        yazar.ToplamAlintilanma=soup.find("td", class_="gsc_rsb_std").text
        a=soup.find("div", class_="gsc_prf_il").next_sibling
        for i in soup.find_all("a",class_="gsc_rsb_aa"):
            yazar.Katki.append(i.text)
        for i in a.find_all("a",class_="gsc_prf_ila"):
            yazar.ilgiAlanlari.append(i.text)
        authorArticle(pagelink,yil)


authorPage(pagelink)

print("Yazar Adı Soyadı:"+yazar.AdiSoyadi)
print("Çalışma Yeri:"+yazar.CalismaYeri)
print("Toplam Alıntılanma:"+yazar.ToplamAlintilanma)
print("İlgi Alanları:"+"\t")
for i in yazar.ilgiAlanlari:
    print(i)

for i in range(0,len(yazar.Makaleleri)):
    print("Makale Adı:"+yazar.Makaleleri[i]+"\t\tYayınlanma Yılı:"+yilliste[i]+"\t\tAlıntılanma:"+alintiliste[i])
for i in range(0,len(yazar.Katki)):
    print("Katkı yapan:"+yazar.Katki[i])

