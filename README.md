# twox


## Install HDR Homebridge camera

By taking a range of images with a range of exposure times, the Raspberry Pi can generate a [High Dynamic Range](https://en.wikipedia.org/wiki/High_dynamic_range) images. These provide much better contrast than the automatic exposure provided by the cameras, in particurlar where the lighting conditions are stark (e.g. sunlight and shadows). 

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install screen vim imagemagick git ffmpeg enfuse python3-pip

```

Enable the camera in `sudo raspi-config`

Get the latest node.js install for Raspberry Pi Zero from [here](https://github.com/sdesalas/node-pi-zero).

Install homebridge and the ffmepg plugin, and the ui-x component that provides the service:
```bash
sudo npm install -g homebridge homebridge-config-ui-x homebridge-camera-ffmpeg
```
Update the `.bashrc`:
```bash
PATH=/opt/nodejs/bin:$PATH
```
Edit the `.homebridge/config.json` to look something like:

```json
{
  "bridge": {
    "name": "Homebridge Pi Zero",
    "username": "CD:2D:AA:E3:CE:33",
    "port": 51826,
    "pin": "123-45-678"
  },
  "description": "Homebridge HDR Camera",
  "accessories": [
  ],
  "platforms": [
    {
      "platform": "Camera-ffmpeg",
      "cameras": [
        {
          "name": "HDR Camera",
          "videoConfig": {
            "source": "-i /home/pi/hdr_latest.jpg",
            "stillImageSource": "-i /home/pi/hdr_latest.jpg",
            "maxStreams": 2,
            "maxWidth": 1296,
            "maxHeight": 972,
            "maxFPS": 1
          }
        }
      ]
    }
  ]
}    

```
Install the Homebridge service:

```bash
sudo /opt/nodejs/bin/hb-service install --user pi
```

Dowload the script and set up the HDR capture:
```bash
cd
wget https://raw.githubusercontent.com/henrikmelin/twox/master/homebridge-hdr-camera/capture.sh
mkdir images
```
Load it at startup by adding this line to `/etc/rc.local`:
```bash
runuser -l pi -c 'sh /home/pi/capture.sh'
```
Go to `http://<IP of pi>.local:8581` and log in using admin/admin and then add this to HomeKit using hte QR code and pin (as set in the config.json file)

### Add Dropbox upload support

Since this script will generate lots of images that are overwritten, it may be good to store them somewhere to build time-lapses etc. Storing them on Dropbox also provides off-site storage if you wann use this for monitoring. 

Add a new app using the Dropbox API, and set the app to have write permissions, then generate the Access Key. Then add this to the `.bashrc`:

```bash
export DROPBOX_ACCESS_TOKEN="**TheAccessKey**"
export CAMERA_LOCATION="name-of-room"

```
And then uncomment the line in `capture.sh` that starts with `python3 upload2dropbox.py`. This requires:
```
pip3 install dropbox
```
The files will upload to the folder called `picameras` but that can be changed in `capture.sh`.