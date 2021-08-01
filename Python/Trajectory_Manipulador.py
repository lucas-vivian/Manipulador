#!/usr/bin/python
# coding: utf8
'''
Point Positioning Program for ARM 5E Manipulator through Invese Kinematics

@author: Lucas Vivian
'''

import serial
import struct
from math import *
from struct import *
from scipy.optimize import least_squares
from math import *

# byte de inicio da mensagem
Start_byte = 0xE7

# 3 bytes de aquisicao dos sensores
Master_T = 0x00
Master_V = 0x00
Master_C = 0x00
# não é preenchido para o envio

# 9 bytes por motor para motor data
# Exemplo para motor 1

demand_prefix = 0x00  # Motor data: demand, PID or sensors
pid_prefix = 0x01
sensor_prefix = 0x01

demand_stop = 0x00
demand_pos = 0x05

msb_voltage = 0x7F
lsb_voltage = 0xFF  # demanda de 4095 de 65535

msb_zero = 0x00
lsb_zero = 0x00

msb_speed_lim = 0x03
lsb_speed_lim = 0xFF  # velocidade limitada a 1/4 da limitação máxima

msb_cur_lim = 0x07  # testar com 0x0F
lsb_cur_lim = 0xFF  # corrente limitada a 1/4 da limitação máxima

motor_data = 0x00

# byte de checksum
# fazer com overflow ja que o checksum so possui 8 bits
# chksum = 0x00

# byte de end of message
End_byte = 0xE5


def read_msg(Obj_porta):  # recebe a mensagem da serial e, através do protocolo conhecido, transforma-a em uma lista
    # Obj_porta = msg_serial()
    # align='>' #trocando de volta para big-endian, seguindo o protocolo
    align = '<'  # seguindo o documento Erros do Protocolo
    start = 'B'
    master_values = '3B'
    # motor='1B3H1Bx' #seguindo o protocolo
    motor = '1B2H3Bx'  # formato atual
    check = 'B'
    end = 'B'
    byte = Obj_porta.read()
    # print "Antes:", byte.encode('hex')
    if byte == '\xe7':  # start byte
        # print "Depois:", byte.encode('hex')
        # print Obj_porta.inWaiting()
        msg_raw = Obj_porta.read(50)  # começa a partir do byte seguinte ao byte start
        # print "Depois:", byte.encode('hex')
        # print("\n")
        # print " ".join(c.encode('hex') for c in msg_raw)
        if msg_raw[49] != '\xe5':  # byte final inválido
            return None
        chksum = 0xe7
        for i in range(0, 47):
            chksum += ord(msg_raw[i])
        chksum = chksum % 256
        # print 'cheksum: ', chksum, '=', ord(msg_raw[48])
        if chksum != ord(msg_raw[48]):
            # print("Pacote corrompido")
            return None
        else:
            # print("Pacote OK")
            msg = list(struct.unpack(align + master_values + 5 * motor + check + end, msg_raw))
            msg.insert(0, 0xe7)
            # print " ".join('{:02x}'.format(x) for x in msg)
            # print "e7", " ".join(c.encode('hex') for c in msg_raw)
            # print msg
            return msg


def open_serial():
    porta = '/dev/ttyUSB0'
    baud_rate = 115200
    Obj_porta = serial.Serial(porta, baud_rate)
    return Obj_porta


def create_msg():
    msg = [Start_byte,
           Master_T,
           Master_V,
           Master_C,
           demand_prefix,  # inicio do bloco SHOULDER
           demand_pos,
           msb_zero,
           lsb_zero,
           # demand_stop, #byte 5
           # msb_zero,
           # lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix,  # SLEW
           # demand_volt_CW,
           # msb_voltage,
           # lsb_voltage,
           demand_pos,  # byte 14
           msb_zero,
           lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix,  # ELBOW
           demand_pos,  # byte 23
           msb_zero,
           lsb_zero,
           # demand_volt_CW,
           # msb_voltage,
           # lsb_voltage,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix,  # JAW ROTATE
           # demand_volt_CW,
           # msb_voltage,
           # lsb_voltage,
           demand_stop,
           msb_zero,
           lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix,  # JAW OPENING/CLOSE
           # demand_volt_CW, #(opening)
           # demand_volt_CCW,
           # msb_voltage,
           # lsb_voltage,
           demand_stop,
           msb_zero,
           lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data]
    # final_msg = complete_msg(msg)
    return msg


def checksum(msg):
    # Add check_sum byte at the end of message
    chksum = 0x00
    for i in range(0, 48):
        chksum += msg[i]
    chksum = chksum % 256
    msg.append(chksum)
    msg.append(End_byte)
    return msg


def send_msg(msg_final, Obj_porta):
    msg_pack = pack('<{}B'.format(len(msg_final)), *msg_final)
    # print " ".join(c.encode('hex') for c in msg_pack)
    Obj_porta.write(msg_pack)


def send_target_pos(Obj_porta, target_pos):
    # Send desired joint positions for manipulator
    # print "Send target joint position: "
    new_msg = create_msg()

    for motor_num in range(3):
        motor_change = 9 * motor_num + 5  # byte to change in the new message
        pos = target_pos[motor_num]
        lsb = pos & 0xFF
        msb = (pos >> 8) & 0xFF
        new_msg[motor_change + 1] = msb
        new_msg[motor_change + 2] = lsb
        # print motor_num + 1, pos

    final_msg = checksum(new_msg)

    send_msg(final_msg, Obj_porta)


def get_actual_pos(msg):
    # Get actual joint angle positions from received message
    pos = [0, 0, 0]

    # print "Read actual joint position: "

    for motor_num in range(3):
        pos[motor_num] = msg[motor_num * 6 + 5]
    # print motor_num + 1, pos[motor_num]

    return pos


def get_actual_speed(msg):
    # Get actual joint speed from received message
    spd = [0, 0, 0]
    for motor_num in range(3):
        spd[motor_num] = msg[motor_num * 6 + 6]
    # print "Joints' speed: ", spd
    return spd


def get_ee_pos_from_file():
    # Get target end-effector position or trajectory from file
    file = open('ponto.txt', 'r')

    ee_pos = []
    data = file.readline()

    # Resolver problema da linha extra no final do arquivo!!!
    while data:
        data = data.strip()
        new_data = data.split(',')
        ee_pos.append(map(float, new_data))
        data = file.readline()

    file.close()

    # print ee_pos, len(ee_pos)

    return ee_pos


def arm_eq(p, x, y, z):
    # Define kinematic equation for the manipulador
    a1 = 115.8;
    a2 = 315;
    a3 = 92;
    d4 = 407;

    t1, t2, t3 = p
    t1 = t1 - pi / 2
    t2 = t2 - pi / 2
    t3 = t3 - 75 * pi / 180

    return (cos(t1) * (a1 + a3 * cos(t2 - t3) - d4 * sin(t2 - t3) + a2 * cos(t2)) - x,
            sin(t1) * (a1 + a3 * cos(t2 - t3) - d4 * sin(t2 - t3) + a2 * cos(t2)) - y,
            - d4 * cos(t2 - t3) - a3 * sin(t2 - t3) - a2 * sin(t2) - z)


def ik_solver(ee_pos):
    slew = radians(120);
    shoulder = radians(90);
    elbow = radians(145);

    x = ee_pos[0]
    y = ee_pos[1]
    z = ee_pos[2]

    lb = (0, 0, 0)
    ub = (slew, shoulder, elbow)

    res = least_squares(arm_eq, (0.1, 0.1, 0.1), bounds=(lb, ub), args=(x, y, z))

    # Check if the optimization was successfull
    opt_result_pos = arm_eq(res.x, 0, 0,
                            0)  # returns theoretical end effector position from provided optimization result angles

    dist = sqrt((ee_pos[0] - opt_result_pos[0]) ** 2 + (ee_pos[1] - opt_result_pos[1]) ** 2 + (
                ee_pos[2] - opt_result_pos[2]) ** 2)  # calculates distance

    # print "Computado: ", opt_result_pos
    # print "Desejado: ", ee_pos
    # print dist

    tolerance = 10  # tolerance distance of 1 cm
    if dist > tolerance or res.success is not True:
        print "Error! Coordinate outside manipulator's workspace!"
        exit()

    # print "IK solution (rad):", res.x[1], res.x[0], res.x[2]
    # print "IK solution (deg):", degrees(res.x[1]), degrees(res.x[0]), degrees(res.x[2])

    return res


def convert_rad_to_ad(pos_rad):
    pos = [0, 0, 0]

    pos[0] = int((20320 * degrees(pos_rad[0])) / 90)
    pos[1] = int((20320 * degrees(pos_rad[1])) / 120)
    pos[2] = int((20320 * degrees(pos_rad[2])) / 145)

    return pos


# NOT USED!!
def verify_opt(opt_result, ee_pos):  # Receives optimization result and original position from file
    opt_result_pos = arm_eq(opt_result.x, 0, 0,
                            0)  # returns theoretical end effector position from provided optimization result angles
    print "Optimization result position", opt_result_pos
    dist = sqrt((ee_pos[0] - opt_result_pos[0]) ** 2 + (ee_pos[1] - opt_result_pos[1]) ** 2 + (
                ee_pos[2] - opt_result_pos[2]) ** 2)  # calculates distance
    # between desired EE position and optimization found position
    tolerance = 10  # tolerance distance of 1 cm
    if dist > tolerance or opt_result.success is not True:
        print "Error! Coordinate outside manipulator's workspace!"
        exit()


def evaluate_speed(spd):
    tolerance = 1  # defines 10 rpm of tolerance
    joints = 0
    # print "Joint Speeds: ", spd
    for i in range(3):
        if spd[i] < tolerance:  # evaluate if speed of each joint is less than tolerance
            joints += 1
            if joints == 3:  # all joints stopped
                print "Manipulator arrived at current point"
                return True


def main():
    # open serial port
    Obj_porta = open_serial()

    # Send the robot to initial position
    target_pos = [0, 0, 0]  # unidade: AD
    send_target_pos(Obj_porta, target_pos)  # enviar posição desejada
    received_msg = read_msg(Obj_porta)
    if received_msg is not None:
        pos_before = get_actual_pos(received_msg)

    # Get target end-effector position (x, y, z) or trajectory matrix from file
    ee_pos = get_ee_pos_from_file()
    num_points = len(ee_pos)
    # print "\nTrajectory: ", ee_pos, "\n"

    # Check if Trajectory is empty!! --> MISSING

    # Start at first point of trajectory
    pt = 0
    point_reached = False
    moving = False
    count = 0

    while (1):
        # print "Point: ", pt

        # Compute joint angles from target EE pos (using IK)
        # print "Trajectory Point: ", ee_pos[pt]
        # print "Matrix Index: ", pt
        opt_result = ik_solver(ee_pos[pt])

        # Retrieve only angle values from the optimization result
        target_pos_rad = [opt_result.x[1], opt_result.x[0], opt_result.x[2]]

        # Convert target joint angles from degrees to "pulses"
        target_pos = convert_rad_to_ad(target_pos_rad)
        # print  "Target joint position (ad):", target_pos

        # Send target position (joint angles)
        target_pos = [0, 0, 0]
        # target_pos = [6773, 5080, 4204]  # unidade: AD
        send_target_pos(Obj_porta, target_pos)

        # Read data from manipulator
        received_msg = read_msg(Obj_porta)

        if received_msg is not None:
            pos_now = get_actual_pos(received_msg)

            # Check if the arm has started to move
            for i in range(3):
                if abs(pos_now[i] - pos_before[i]) > 10:
                    moving = True

        count += 1;

        # If it is moving, check the speed
        if moving == True:
            spd = get_actual_speed(received_msg)
            # print pos_before, pos_now, spd

            if (spd[0] == 0) and (spd[1] == 0) and (spd[2] == 0):  # ver um jeito melhor de fazer isso...
                point_reached = True
                moving = False

                print "Point reached: ", point_reached
                print "Trajectory Point: ", ee_pos[pt]
                print "Point: ", pt
                print  "Target joint position (ad):", target_pos
                print "Actual joint position (ad):", pos_now
                print "Count: ", count
                print "\n"
                count = 0

        # If the point was reached, move on to the next point, until the trajectory is completed
        if point_reached == True:
            if pt == num_points - 1:
                print "Trajectory Completed!"
                exit()
            elif pt < num_points - 1:
                pt += 1  # go to next point
                point_reached = False
                pos_before = pos_now

    # print "\n"


if __name__ == '__main__':
    main()
