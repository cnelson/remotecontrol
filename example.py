#!/usr/bin/env python3
"""An example of using the Roku External Control API to control the
roku app shipped with this script

https://sdkdocs.roku.com/display/sdkdoc/External+Control+API
"""

import atexit
import argparse
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from multiprocessing import Process


ECA_PORT = 8060
APP_NAME = 'remotecontrol'


def cleanup(p):
    """Deal with our child process on shutdown

    Args:
        p (Process): The process to reap
    """

    p.terminate()
    p.join()


def keep_app_running(roku_hostname, delay=1):
    """Continually tell the roku to start the dev app.  This will ensure the
    app is restarted if the roku crashes or reboots

    Args:
        roku_hostname (str): The hostname or ip of the device
        delay (float): The numberof seconds to sleep between start requests

    Returns:
        - This function blocks forever

    """

    while True:
        try:
            urllib.request.urlopen(
                'http://{}:{}/launch/dev'.format(roku_hostname, ECA_PORT),
                data=bytes()  # send POST method with empty body per api spec
            )
        except urllib.error.URLError as exc:
            if exc.code == 404:
                print("Dev app is not installed.  Did you sideload it?")
            else:
                print("Error launching app: {}".format(exc))

        time.sleep(delay)


def play_video(roku_hostname, video):
    """Instruct the remote control app to play a video

    Args:
        roku_hostname (str): The hostname or ip of the device
        video (str): The name of the video to be played

    Returns:
        True: The request was made (video might not play for other reasons)

    Raises:
        Exception: Something went wrong (exception will have more info)

    """

    urllib.request.urlopen(
        'http://{}:{}/input?video={}'.format(roku_hostname, ECA_PORT, video),
        data=bytes()  # send POST method with empty body per api spec
    )

    return True


def query_app(roku_hostname):
    """Check if roku api can be reached

    Args:
        roku_hostname (str): The hostname or ip of the device

    Returns:
        str: The name of the currently running app.
        True: Roku is reachable

    Raises:
        Exception: Something went wrong (exception will have more info)

    """
    resp = urllib.request.urlopen(
        'http://{}:{}/query/active-app'.format(roku_hostname, ECA_PORT)
    )

    info = ET.fromstring(resp.read())

    return info[0].text.strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play a video on a Roku via Remote Control app"
    )

    parser.add_argument(
        'roku_hostname',
        help="The ip or hostname of the roku."
    )

    parser.add_argument(
        'video',
        help="The name of the video to play."
    )

    args = parser.parse_args()

    try:
        app = query_app(args.roku_hostname)
    except Exception as exc:
        parser.error(
            "Unable to connect to roku at {}: {}".format(
                args.roku_hostname,
                exc
            )
        )

    # start a background process to keep our app running
    # not really useful for this example, but in a more robust
    # implementation we'd want a process continually monitoring this state
    # to ensure the roku is always in our app, and not displaying it's own
    # ui
    p = Process(target=keep_app_running, args=(args.roku_hostname,))
    p.start()
    atexit.register(cleanup, p)

    # wait for our app to be running on the roku
    tries = 5
    while tries > 0:
        if app == APP_NAME:
            break

        tries = tries - 1
        app = query_app(args.roku_hostname)
        time.sleep(1)

    if app != APP_NAME:
        parser.error("Gave up waiting for app to start. Is it installed?")

    # play the requested video
    try:
        play_video(args.roku_hostname, args.video)
    except Exception as exc:
        parser.error(
            "Unable to play video on {}: {}".format(
                args.roku_hostname,
                exc
            )
        )
