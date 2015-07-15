import logging
from PyObjCTools import AppHelper
from Cocoa import NSObject
import objc
import AppKit

# Get objc references to the classes we need.
NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

# objc.setVerbose(1)

class MountainLionNotification(NSObject):
    # Based on http://stackoverflow.com/questions/12202983/working-with-mountain-lions-notification-center-using-pyobjc

    def init(self):
        self = super(MountainLionNotification, self).init()
        if self is None: return None

        self.logger = logging.getLogger('TeamspeakNotifcation')
        self.nc = NSUserNotificationCenter.defaultUserNotificationCenter()
        self.nc.setDelegate_(self)

        return self

    def clearNotifications(self):
        """Clear any displayed alerts we have posted. Requires Mavericks."""

        self.nc.removeAllDeliveredNotifications()

    def notify(self, title='', subtitle='', text='', playSound=False):
        """Create a user notification and display it."""
        self.clearNotifications()
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(str(title))
        notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(str(text))
        if playSound:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")
        notification.setHasActionButton_(True)
        notification.setActionButtonTitle_("View")
        # private (undocumented) functionality
        notification.setValue_forKey_(True, '_showsButtons')

        self.nc.setDelegate_(self)
        self.nc.scheduleNotification_(notification)

        # Note that the notification center saves a *copy* of our object.
        return notification

    def userNotificationCenter_applicationDidFinishLaunching_(self, center, notification):
        print "launched!"

    def userNotificationCenter_didActivateNotification_(self, center, notification):
        '''User clicked on our notification'''
        self.logger.debug('Got userNotificationCenter:didActivateNotification:')
        self.userActivatedNotification_(notification)

    def userNotificationCenter_shouldPresentNotification_(self, center, notification):
        '''Delegate method called when Notification Center has decided it doesn't
        need to present the notification -- returning True overrides that decision'''
        self.logger.debug('Got userNotificationCenter:shouldPresentNotification:')
        return True

    def userNotificationCenter_didDeliverNotification_(self, center, notification):
        '''Notification was delivered and we can exit'''
        self.logger.debug('Got userNotificationCenter:didDeliverNotification:')
        NSApp.terminate_(self)

    def userActivatedNotification_(self, notification):
        '''React to user clicking on notification by launching MSC.app and showing Updates page'''
        NSUserNotificationCenter.defaultUserNotificationCenter().removeDeliveredNotification_(
            notification)
        user_info = notification.userInfo()
        if user_info.get('action') == 'open_url':
            url = user_info.get('url')
            NSWorkspace.sharedWorkspace(
                ).openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                        [NSURL.URLWithString_(url)], MSCbundleIdentifier, 0, None, None)

    # # We'll get this if the user clicked on the notification.
    # def userNotificationCenter_didActivateNotification_(self, center, notification):
    #     """Handle a user clicking on one of our posted notifications."""

    #     print 'click'
    #     return AppKit.NSWorkspace.launchApplication("TeamSpeak 3")

