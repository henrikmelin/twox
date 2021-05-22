# twox


## Install HDR Homebridge camera



```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install screen vim imagemagick git ffmpeg enfuse

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


