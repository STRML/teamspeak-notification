import logging
import re
import time
from notification import MountainLionNotification
import AppKit

import teamspeak3

class TeamspeakNotifier(object):
    CHECK_INTERVAL = 0.25
    RECONNECT_INTERVAL = 1
    TEAMSPEAK_TITLE = "TeamSpeak 3"
    DEFAULT_NAME = "Somebody"
    TARGETMODE_CLIENT = '1'
    TARGETMODE_CHANNEL = '2'
    TARGETMODE_SERVER = '3'

    def __init__(self):
        super(TeamspeakNotifier, self).__init__()
        self.logger = logging.getLogger('TeamspeakNotifier')

        self.notification = MountainLionNotification.alloc().init()
        self.notification.notify(
            title="TeamSpeak 3",
            subtitle="Starting",
            text="TeamspeakNotifier is finding Teamspeak."
        )
        self.connect()

        self.clients = {}
        self.identity = None

    def get_active_window_title(self):
        return AppKit.NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

    def _update_notification(self, title, message = ''):
        self.logger.debug("Posting Notification: [%s]%s" % (
                    title,
                    message,
                )
            )
        self.notification.notify(title=title, text=message)

    def notify(self, message):
        if message.ultimate_origination == 'notifytextmessage':
            if not self.teamspeak_is_active() and not self.message_is_mine(message):
                if message['targetmode'] == self.TARGETMODE_CLIENT:
                    title = "%s said (via private message)" % (
                            self.get_name_for_message(message),
                        )
                else:
                    title = "%s said" % (
                            self.get_name_for_message(message),
                        )
                self._update_notification(title, message['msg'])
        elif message.ultimate_origination == 'notifytalkstatuschange':
            if not self.teamspeak_is_active() and not self.message_is_mine(message):
                if message['status'] == '1':
                    self._update_notification(
                                    "%s is talking..." % (
                                    self.get_name_for_message(message),
                                )
                            )
        elif message.ultimate_origination in ('notifyclientmoved', 'notifyclientleftview', 'notifycliententerview', ):
            self.send_client_update_commands()
        elif message.ultimate_origination == 'clientlist':
            self.update_client_list(message)
        elif message.ultimate_origination == 'whoami':
            self.update_identity(message)
        elif message.ultimate_origination == 'notifyconnectstatuschange':
            self._update_notification(
                                message['status'].title(),
                                "Your connection to Teamspeak is now %s." % message['status']
                            )

    def send_client_update_commands(self):
        self.api.send_command(
                    teamspeak3.Command('clientlist')
                )
        self.api.send_command(
                    teamspeak3.Command('whoami')
                )

    def update_identity(self, message):
        self.identity = message['clid']
        self.logger.info("Updated identity: %s" % self.identity)

    def update_client_list(self, message):
        self.clients = {}
        if not hasattr(message, 'responses'):
            responses = [message]
        else:
            responses = message.responses
        for client_info in responses:
            self.clients[client_info['clid']] = client_info['client_nickname']
        self.logger.info("Updated client list: %s" % self.clients)

    def message_is_mine(self, message):
        try:
            if 'clid' in message.keys():
                return message['clid'] == self.identity
            elif 'invokername' in message.keys():
                return self.clients[self.identity] == message['invokername']
            elif 'invokerid' in message.keys():
                return message['invokerid'] == self.identity
        except KeyError:
            pass
        return False

    def get_name_for_message(self, message):
        try:
            if 'clid' in message.keys():
                return self.clients[message['clid']]
            elif 'invokername' in message.keys():
                return message['invokername']
            elif 'invokerid' in message.keys():
                return self.clients[message['invokerid']]
        except KeyError:
            pass
        return self.DEFAULT_NAME

    def teamspeak_is_active(self):
        return self.get_active_window_title() == self.TEAMSPEAK_TITLE

    def main(self):
        while True:
            try:
                messages = self.api.get_messages()
                for message in messages:
                    self.notify(message)
            except teamspeak3.TeamspeakConnectionError:
                self._update_notification(
                        "Teamspeak is Unavailable", "Teamspeak does not appear to be running."
                    )
                self.logger.warning("Connection lost.")
                self.connect()
            time.sleep(self.CHECK_INTERVAL)

    def connect(self):
        while True:
            try:
                self.logger.info("Attempting to connect.")
                self.api = teamspeak3.Client()
                self.api.subscribe()
                self.logger.info("Connection established.")
                self._update_notification(
                        "Ready",
                        "Teamspeak is now listening for messages."
                    )
                self.send_client_update_commands()
                return True
            except teamspeak3.exceptions.TeamspeakConnectionLost as e:
                self.logger.exception(e)
                pass
            except Exception as e:
                self.logger.exception(e)
                pass
            time.sleep(self.RECONNECT_INTERVAL)


