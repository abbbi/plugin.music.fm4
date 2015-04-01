import sys
import urllib
import urlparse
import requests
import xbmcgui
import xbmcplugin

FM4_API_URL='http://audioapi.orf.at/fm4/json/2.0/broadcasts/'
DOWNLOAD_URL='http://loopstream01.apa.at/?channel=fm4&id='
ADDON_NAME='FM4 On Demand'

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
dialog = xbmcgui.Dialog()

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def get_broadcast_days():
    try:
        r = requests.get(FM4_API_URL)
    except:
        dialog.ok(ADDON_NAME, 'Error getting FM API data, see kodi.log')

    try:
        bcd = r.json()
    except:
        dialog.ok(ADDON_NAME, 'Error parsing FM4 JSON API data')

    days = []
    for item in bcd:
        days.append(item['day'])

    return days

def get_broadcast_shows(day):
    try:
        r = requests.get(FM4_API_URL + day)
    except:
        dialog.ok(ADDON_NAME, 'Error getting FM API data for day %s ' % day)

    try:
        s = r.json()
    except:
        dialog.ok(ADDON_NAME, 'Error parsing FM4 JSON API data for day %s' % day)

    shows = []

    for show in s:
        s=dict()
        s['title'] = show['title'].encode('utf-8')
        s['programKey'] = show['programKey']
        shows.append(s)

    return shows
    
if mode is None:

    for day in get_broadcast_days():
        url = build_url({'mode': 'folder', 'foldername': str(day)})
        li = xbmcgui.ListItem(str(day), iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    day = args['foldername'][0]

    shows = get_broadcast_shows(day)

    if len(shows) <= 0:
        dialog.ok(ADDON_NAME, 'No shows found .. maybe somethings wrong with the FM4 API, exiting')
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")

    for show in shows:
        r = requests.get(FM4_API_URL + day + '/' + show['programKey'])
        data = r.json()
        try:
            if data['streams']:
                url = (DOWNLOAD_URL + data['streams'][0]['loopStreamId'] + '&offset=0')
                li = xbmcgui.ListItem(day + ": " + str(show['title']), iconImage='DefaultVideo.png')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        except KeyError:
            dialog.ok(ADDON_NAME,'Error: no streams found for this day')
            xbmc.executebuiltin("XBMC.Container.Update(path,replace)")

    xbmcplugin.endOfDirectory(addon_handle)
