This is a modified python script using Pi My Life Up's simple GPIO LDR tutorial (https://pimylifeup.com/raspberry-pi-light-sensor/) in combination with Murry's sunrise/sunset code (https://blog.ligos.net/2016-04-18/Day-Night-Cycle-For-MotionEye.html) to change the MotionEyeOS camera configuration based upon time of day.

To use this, you need a photoresistor and 1uF capacitor. It should be noted that I used what I had laying around, in this case a 100uF capacitor. Therefore, if you use the 1uF capacitor, you'll need to adjust your thresshold accordingly.

I added a GPIO header to my Raspberry PI Zero for the aforemenitoned sensor.

Once you've added your sensor, log into your MotionEyeOS device, and cd to /data.

I created a directory, /data/ToD, to store the state file. Should you wish to use a different state directory, you'll need to modify the script to reflect that. Otherwise, this script will repeatedly update/restart the MotionEyeOS server.

The python script will set the initial state to "", which ensures the correct configuration will be copied on your first run.

Place the script in /data/ToD.py.

You also need to create the following files:

/data/etc/thread-1.conf.day
/data/etc/thread-1.conf.night

The easiest way to create these files is to copy thread-1.conf to each file, respectively. One during the day, once you have your desired settings, and the other at night, once you have your desired settings.

Once your files are created, it's a matter of adding a cron job:

EDITOR=nano crontab -e
02,07,12,17,22,27,32,37,42,47,52,57 * * * * /usr/bin/python /data/ToD.py >> /var/log/daynight.log

