# TeamSpeak Notifier for Mac OS X

Using TeamSpeak as your office communication channel can be difficult -- especially
if you don't have your headphones on.

This application will watch for incoming messages in Teamspeak and, should you
be in a different window, display a notification to let you know that you
recieved a message. It will also alert to tell you who is speaking, which is
especially useful in large rooms.

This uses OS X's Notification Center to display notifications, so it requires 10.8+.
There may be bugs in OS X betas as Apple has been known to change the API.

## Requirements

 - teamspeak3
 - Enabled "Client Query" plugin in TeamSpeak.

## Setup

    python setup.py develop

## Use

You can run the program directly with:

    ./teamspeak-notifier

Add it to your automatically started applications. It will automatically connect
to TeamSpeak when it is available.

## Arguments

You can run it with any of the following arguments:

 - **--info** Allows you to see information about communication with Teamspeak.
 - **--debug** Allows you to see more information than the above.
 - **--logfile**  Allows you to specify a file to log errors to.


