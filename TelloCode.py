from djitellopy import tello
import time
import cv2
import keyControl as kc

kc.init()
me = tello.Tello()
 me.connect()
print(me.get_battery())

me.takeoff()

### left-right, forward-backward, up-down, yaw
me.send_rc_control(0, 50, 0, 0)   ### forward
sleep(2)
me.send_rc_control(30, 0, 0, 0)   ### right
sleep(2)
me.send_rc_control(0, 0, 0, 90)   ### Yaw
sleep(2)
me.send_rc_control(0, 0, 0, 0)
me.land()

### Image
me.streamon()
global img


### Keyboard Input
def getkeyboardInput():
    lr, fb, ud, yv = 0,  0, 0, 0
    spd = 50
    if kc.getKey("LEFT"):
        lr = -spd
    elif kc.getKey("RIGHT"):
        lr = spd

    if kc.getKey("UP"):
        fb = spd
    elif kc.getKey("DOWN"):
        fb = -spd

    if kc.getKey("w"):
        ud = spd
    elif kc.getKey("s"):
        ud = -spd

    if kc.getKey("a"):
        yv = -spd
    elif kc.getKey("d"):
        yv = spd

    if kc.getKey("l"): me.land(); time.sleep(3)
    if kc.getKey("t"): me.takeoff()

    if kc.getKey("c"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3)
    return [lr, fb, ud, yv]


while True:
    val = getkeyboardInput()
    me.send_rc_control(val[0], val[1], val[2], val[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360,240))
    cv2.imshow("Image", img)
    print(val)
    time.sleep(0.5)
