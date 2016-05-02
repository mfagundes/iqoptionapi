# -*- coding: utf-8 -*-
"""Module for IQ option api."""

import time
import json
import logging
import requests
import threading

from iqoption_api.login import Login
from iqoption_api.websocket import Websocket
from iqoption_api.ssid import Ssid
from iqoption_api.subscribe import Subscribe
from iqoption_api.unsubscribe import UnSubscribe
from iqoption_api.setactives import SetActives
from iqoption_api.buy import Buy

# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()


class IQOptionAPI(object):
    """Class for communication with IQ option api."""
    
    def __init__(self, ssid):
        """
        :param str host: The hostname or ip address of a IQ option server.
        :param str username: The username of a IQ option server.
        :param str password: The password of a IQ option server.
        """


        self.wss_url = "wss://iqoption.com/echo/websocket"
        self.websocket = None
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False
        self.myssid = ssid


    def send_wss_request(self, name, msg):
        """
        Send wss request to IQ option server.

        :param chanel: :class:`Chanel <iqoption_api.chanel.Chanel>`.
        :param dict data: The websocket request data.

        :returns: 
        """
        data = json.dumps(dict(name=name, 
                               msg=msg))
        self.websocket.send(data)

    @property
    def login(self):
        """
        Property for get IQ option login resource.

        :returns: :class:`Login
            <iqoption_api.login.Login>`.
        """
        return Login(self)

    @property
    def ssid(self):
        """
        Property for get IQ option websocket ssid chanel.

        :returns: :class:`Ssid
            <iqoption_api.ssid.Ssid>`.
        """
        return Ssid(self)

    @property
    def subscribe(self):
        """
        Property for get IQ option websocket subscribe chanel.

        :returns: :class:`Subscribe
            <iqoption_api.subscribe.Subscribe>`.
        """
        return Subscribe(self)

    @property
    def unsubscribe(self):
        """
        Property for get IQ option websocket unsubscribe chanel.

        :returns: :class:`unsubscribe
            <iqoption_api.unsubscribe.UnSubscribe>`.
        """
        return UnSubscribe(self)

    @property
    def setactives(self):
        """
        Property for get IQ option websocket setactives chanel.

        :returns: :class:`setactives
            <iqoption_api.setactives.SetActives>`.
        """
        return SetActives(self)

    @property
    def buy(self):
        """
        Property for get IQ option websocket buy chanel.

        :returns: :class:`buy
            <iqoption_api.buy.Buy>`.
        """
        return Buy(self)

    def _thread(self):
        """Method for websocket thread.""" 
        self.websocket.run_forever()

    def connect(self, active, strategy, period):
        """Method for connection to api."""


        websocket = Websocket(self.wss_url)
        websocket.connect()

        self.websocket = websocket
       
        websocket_thread = threading.Thread(target=self._thread)
        websocket_thread.daemon = True
        websocket_thread.start()

        self.ssid(self.myssid)

        self.subscribe("deposited")
        self.unsubscribe("deposited")
        self.unsubscribe("iqguard")
        self.unsubscribe("signal")
        self.unsubscribe("feedRecentBets")
        self.unsubscribe("feedRecentBets2")
        self.unsubscribe("feedTopTraders2")
        self.unsubscribe("feedRecentBetsMulti")
        self.unsubscribe("timeSync")
        self.setactives(active)



        # for i in range(60):
        #     time.sleep(1)
        #     self.buy(self.websocket.time, self.websocket.show_value)