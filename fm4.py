import json
import requests
import sys

import xbmc, xbmcgui

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
FM4_API_URL='http://audioapi.orf.at/fm4/json/2.0/broadcasts/'
DOWNLOAD_URL='http://loopstream01.apa.at/?channel=fm4&id='

class FM4(xbmcgui.Window):
    def __init__(self):
        self.strActionInfo = xbmcgui.ControlLabel(250, 80, 200, 200, '', 'font14', '0xFFBBBBFF')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel('Push BACK to quit')
        self.list = xbmcgui.ControlList(200, 150, 300, 400)
        self.addControl(self.list)

        self.days = self.get_broadcast_days()
        for d in self.days:
            self.list.addItem(str(d))
        self.setFocus(self.list)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.message('exit?')
            self.close()

    def onControl(self, control):
        if control == self.list:
            item = self.list.getSelectedItem()
            self.message('You selected : ' + item.getLabel())

    def message(self, message):
        dialog = xbmcgui.Dialog()
        dialog.ok("FM4", message)

    def get_broadcast_days(self):
        try:
            r = requests.get(FM4_API_URL)
        except:
            self.message('nargh')

        bcd = json.loads(r.content)
        days = []
        for item in bcd:
            days.append(item['day'])

        return days

fm4dis = FM4()
fm4dis.doModal()
del fm4dis
