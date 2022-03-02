from  pycreate2 import Create2
import time
import random

# Create a Create2.
port = "/dev/tty.usbserial-DN025ZAZ"  # where is your serial port?
bot = Create2(port)

# Start the Create 2
bot.start()

# Put the Create2 into 'safe' mode so we can drive it
# This will still provide some protection
bot.safe()

# You are responsible for handling issues, no protection/safety in
# this mode ... becareful
bot.full()


def turnRight(speed):
    angle = 0
    bot.drive_direct(-1 * speed,speed)
    notTrue = True
    somethingHappened = False
    counter = 0
    while notTrue:
        time.sleep(.01)
        sensor = bot.get_sensors()
        angle += sensor.angle #sensor.angle
        #print(angle)
        bump = sensor.light_bumper
        if not bump.left and not bump.front_left and not bump.center_left and not somethingHappened:
            somethingHappened = True
            counter = 0

        if somethingHappened:
            if not bump.left and not bump.front_left and not bump.center_left:
                counter += 1
            if counter == 5:
                notTrue = False
                bot.drive_stop()
        print("L {} CL {} FL {}".format(bump.left, bump.center_left, bump.front_left))
    return angle

def turnLeft(speed):
    angle = 0
    bot.drive_direct(speed,-1 * speed)
    notTrue = True
    somethingHappened = False
    counter = 0
    while notTrue:
        time.sleep(.01)
        sensor = bot.get_sensors()
        angle += sensor.angle #sensor.angle
        #print(angle)
        bump = sensor.light_bumper
        if not bump.right and not bump.front_right and not bump.center_right and not somethingHappened:
            somethingHappened = True
            counter = 0

        if somethingHappened:
            if not bump.left and not bump.front_left and not bump.center_left:
                counter += 1
            if counter == 5:
                notTrue = False
                bot.drive_stop()
        print("R {} CR {} FR {}".format(bump.right, bump.center_right, bump.front_right))
    return -1 * angle
        #isHitting = sensor.light_bumper.front_right or sensor.light_bumper.front_left
        #print(isHitting)


def driveUntilYouHitAWall(speed):
    bot.drive_direct(speed, speed)
    notTrue = True
    while notTrue:
        sensors = bot.get_sensors()
        bump = sensors.light_bumper
        if bump.front_left or bump.front_right:
            bot.drive_stop()
            notTrue = False

def printSensors(bot):
   cnt = 0
   while True:
       # Packet 100 contains all sensor data.
       sensor = bot.get_sensors()

       if cnt % 20 == 0:
           print("[L ] [LF] [LC] [CR] [RF] [ R]")

       print(
           f"{sensor.light_bumper_left:4} {sensor.light_bumper_front_left:4} {sensor.light_bumper_center_left:4} {sensor.light_bumper_center_right:4} {sensor.light_bumper_front_right:4} {sensor.light_bumper_right:4}")
       time.sleep(.01)

       cnt += 1


# TODO: Implement rotation up to 180 of left, up to 270 of right

angle = 0
while True:
    driveUntilYouHitAWall(200)
    turn = random.choice([turnLeft, turnRight])
    angle += turn(200)
    print(angle)
    if(angle <= -360):
        break
bot.drive_stop()





song = [72, 12, 20, 24, 67, 12, 20, 24, 64, 24, 69, 16, 71, 16, 69, 16, 68, 24, 70, 24, 68, 24, 67, 12, 65, 12, 67, 48]
song_num = 3
bot.createSong(song_num, song)
time.sleep(0.1)
bot.playSong(song_num)
time.sleep(10)

# Close the connection
# bot.close()
