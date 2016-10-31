# __author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup


addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
mysettings = xbmcaddon.Addon(id='plugin.video.movihd')

homelink = 'http://movihd.net'
# logo = addon.getAddonInfo('icon')
logo = 'http://movihd.net/img/logo.png'


def GetContent(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-agent','Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    response = urllib2.urlopen(req).read()
    return response

def home():
    link = GetContent(homelink)
    soup = BeautifulSoup(link)
    catli = soup('li')
    for li in range(0,34):
        lisoup = BeautifulSoup(str(catli[li]))
        lititle = str(lisoup('a')[0].contents[0].encode('utf-8'))
        if lititle==' ':
            lititle = lisoup('a')[0].next.next.next.encode('utf-8')
        lilink = homelink+lisoup('a')[0]['href']
        if lititle.find('PHIM B')!=-1:
            addDir(lititle,lilink,1,logo,False,1)
        else:
            addDir(lititle,lilink,1,logo,False,None)

def index(url):
    link = GetContent(url)
    soup = BeautifulSoup(link)
    blockbase = soup('div',{'class':'block-base movie'})
    for b in blockbase:
        bsoup = BeautifulSoup(str(b))
        btitle = str(bsoup('a')[0]['title'].encode('utf-8'))
        blink = homelink+bsoup('a')[0]['href']
        bimage = homelink+bsoup('img')[0]['src']
        if inum==1:
            addDir(btitle,blink,4,bimage,False,None)
        else:
            addLink(btitle,blink,3,bimage)

    pagination = BeautifulSoup(str(soup('div',{'class':'action'})[0]))('a')
    for p in pagination:
        psoup = BeautifulSoup(str(p))
        plink = homelink+psoup('a')[0]['href']
        ptitle = psoup('a')[0].contents[0]

        addDir(ptitle,plink,1,iconimage,False,None)

def episodes(url):
    link = GetContent(url)
    soup = BeautifulSoup(link)
    episodes =BeautifulSoup(str(soup('div',{'class':'action left'})[0]))('a')
    for e in episodes:
        esoup = BeautifulSoup(str(e))
        elink =homelink+'/playlist/'+re.compile("javascript:PlayFilm\('(.+?)'\)").findall(esoup('a')[0]['href'])[0]+'_server-2.xml'
        etitle = str(esoup('a')[0].contents[0].encode('utf-8'))
        addLink(etitle,elink,3,iconimage)

def videolinks(url):
    if url.find('xml')!=-1:
        xml_link=url
    else:
        xml_link =homelink+'/playlist/'+re.compile('http://movihd.net/phim/(.+?)_').findall(url)[0]+'_server-2.xml'
    link = GetContent(xml_link)
    soup = BeautifulSoup(link)
    media = homelink+soup('item')[0].next.next.next.next['url']
    return media

def play(url):
    VideoUrl = videolinks(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=VideoUrl))

def addDir(name, url, mode, iconimage,edit,inum):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
edit=None
inum=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        edit = bool(params["edit"])
except:
        pass
try:
        inum=int(params["inum"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index(url)
elif mode==2:
    videolinks(url)
elif mode==3:
    play(url)
elif mode==4:
    episodes(url)

xbmcplugin.endOfDirectory(int(sysarg))