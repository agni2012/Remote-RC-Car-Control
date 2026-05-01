from pybricks.hubs import PrimeHub;
from pybricks.pupdevices import Motor;
from pybricks.parameters import Port;
from pybricks.tools import wait;
from usys import stdin;
from uselect import poll;

hub = PrimeHub();
motor = Motor(Port.C);
left_motor = Motor(Port.A);
right_motor = Motor(Port.E);
s = 300;
t = 200;

keyboard = poll();
keyboard.register(stdin);

left_turn = 0;
right_turn = 0;
left_straight = 0;
right_straight = 0;

while True:
    #read stdin:
    if keyboard.poll(0):
        cmd = stdin.read(1);
        print(cmd);
        
        if cmd == "r":
            motor.run(50);
        elif cmd == "g":
            motor.run(-50);
        elif cmd == "j" or cmd == "x":
            motor.stop();

        if cmd == "w":
            left_straight = -s;
            right_straight = s;
        elif cmd == "s":
            left_straight = s;
            right_straight = -s;
        elif cmd == "f" or cmd == "x":
            left_straight = 0;
            right_straight = 0;

        if cmd == "a":
            left_turn = t;
            right_turn = t;
        elif cmd == "d":
            left_turn = -t;
            right_turn = -t;
        elif cmd == "h" or cmd == "x":
            left_turn = 0;
            right_turn = 0;

    left_motor.run(left_straight + left_turn);
    right_motor.run(right_straight + right_turn);
    
    if left_straight + left_turn == 0: 
        left_motor.stop();
    if right_straight + right_turn == 0: 
        right_motor.stop();
        
    wait(10);
