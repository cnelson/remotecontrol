# remotecontrol

A simple roku application which plays video off a USB storage and is controlled by the [Remote Control API](https://sdkdocs.roku.com/display/sdkdoc/External+Control+API)

## Install the app on the roku

Ensure [development mode](https://sdkdocs.roku.com/display/sdkdoc/Loading+and+Running+Your+Application#LoadingandRunningYourApplication-EnablingDevelopmentModeonyourbox) is enabled on the roku

Sideload the app:
```bash

pushd roku/remotecontrol
ROKU_DEV_TARGET=ip_or_host_of_the_roku DEVPASSWORD=roku_dev_password make install
popd
```

## Prepare USB drive and insert into roku

Video files should be in an [mp4 container](https://sdkdocs.roku.com/display/sdkdoc/Audio+and+Video+Support#AudioandVideoSupport-SupportedVideoFormats), have a `.mp4` extention, and be in a folder named `roku`.

For example:

```bash 
$ find /mnt/usb-drive
/mnt/usb-drive
/mnt/usb-drive/roku
/mnt/usb-drive/roku/bar.mp4
/mnt/usb-drive/roku/foo.mp4
```

If your roku has more than one port for USB storage, the drive should be placed into the first port.

## Run the example control script

Assuming your USB drive contains the file `roku/foo.mp4`:

```bash
./example.py ip_or_host_of_the_roku foo
```