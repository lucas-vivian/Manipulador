#!/usr/bin/python
# coding: utf8

import struct
import serial

porta='/dev/ttyUSB0'
baud_rate=115200
Obj_porta=serial.Serial(porta,baud_rate)

msg_fixa=0

#align='>' #trocando de volta para big-endian, seguindo o protocolo
align='<' #seguindo o documento Erros do Protocolo
start='B'
master_values='3B'
#motor='1B3H1Bx' #seguindo o protocolo
motor='1B2H3Bx' #formato atual
check='B'
end='B'

flag_corromp = False

def temper(valor):
    temp=((float(valor)/255.0)*3.3)/0.00661016949
    return temp

def cor_master(valor):
    valor=float(valor)
    amps=(((valor/511.0*3.3)/(39.0/59.0))/0.625)*6.0-0.2
    return amps

def cor_individual(valor):
    valor=((float(valor))*1.0)/65535.0
    return valor

def tensao(valor):
    valor=float(valor)
    voltage=(valor/255.0*3.3)/(6800.0/111500.0)
    return voltage

def info_motor(motor,mensagem): #imprime a informação de cada motor
    #print 'Motor', motor
    if motor==1:
        print'(Shoulder)'
    elif motor==2:
        print'(Slew)'
    elif motor==3:
        print'(Elbow)'
    elif motor==4:
        print'(Jaw Rotate)'
    else:
        print'(Jaw Open/Close)'
    #print '\n'
    motor=motor-1
    size_msg_motor=6 # (0x01 (byte) - posição (short) - velocidade (short) - corrente (short) - byte (temp) )
    #posicao das informacoes do primeiro motor
    posicao=5
    velocidade=6
    corrente=9
    temperatura=8  # temperatura
    print 'Posição: ', posicao_motor(mensagem[(posicao+motor*size_msg_motor)],motor+1)
    #print 'Posição: ', mensagem[(posicao+motor*size_msg_motor)]
    print 'Velocidade: ', mensagem[(velocidade+motor*size_msg_motor)],' RPM'
    #valor_corrente = mensagem[(corrente+motor*size_msg_motor)]
    print 'Corrente: ', mensagem[(corrente+motor*size_msg_motor)], ' AD' 
    print 'Temperatura: ', temper(mensagem[(temperatura+motor*size_msg_motor)]),' °C'
    
def tipo_dado(): #recebe a mensagem da serial e, através do protocolo conhecido, transforma-a em uma lista
    # while(1):
        byte_final=Obj_porta.read()
        if byte_final=='\xe5':
            mensagem_raw=Obj_porta.read(51) #começa a partir do byte seguinte a ele
            print("\n")
            print " ".join(c.encode('hex') for c in mensagem_raw)
            if mensagem_raw[0] != '\xe7':
                return None
            elif mensagem_raw[50] != '\xe5':
                return None
            chksum = 0x00
            for i in range(0, 48):
                chksum += ord(mensagem_raw[i])                
            chksum = chksum % 256
            #print 'cheksum: ', chksum, '=', ord(mensagem_raw[49])
            if chksum != ord(mensagem_raw[49]):
                print("Pacote corrompido")
                msg=struct.unpack(align+start+master_values+5*motor+check+end,mensagem_raw)
                print(msg)
                return None
            else:
                print("Pacote OK")
                msg=struct.unpack(align+start+master_values+5*motor+check+end,mensagem_raw)
                return msg
            
def trata_msg(mensagem_raw): #recebe uma mensagem teste, trata e retorna-a
    if msg_fixa == True and mensagem_raw != '\x00':
        msg=struct.unpack(align+start+master_values+5*motor+check+end,mensagem_raw)
    else:
        msg = tipo_dado()
    return msg

def checa_inicio(mensagem):
    if mensagem[0]==231:
        print 'Início da mensagem'
        
def checa_fim(mensagem):
    if mensagem[-1]==229:
        print 'Fim da mensagem'
        
def val_master(mensagem):
    print 'Master Temperature: ',temper(mensagem[1]),' °C'
    print 'Master Voltage: ',tensao(mensagem[2]),'V'
    print 'Master Current: ',cor_master(mensagem[3]),'A'
    
def posicao_motor(val,tipo): # imprime raw
    pos_max_elbow = 20318;
    pos_max_shoulder = 20334;
    pos_max_slew = 20296;
    if tipo==1: #shoulder varia 90 graus
        #new_val=map(val,0,65535,0,90)
        new_val=(90.0*val)/65535.0
        return new_val
    elif tipo==2: #Slew varia 120 graus
        new_val=(120.0*val)/65535.0
        return val
    elif tipo==3: #Elbow varia 135 graus
        new_val=(145.0*val)/65535.0
        return new_val
    elif tipo==4: #Jaw Rotate varia continuamente (360 graus)
        new_val=(359.0*val)/65535.0
        return new_val
    else: #Jaw Open/Close varia 140 mm
        new_val=(140.0*val)/65535.0
        return new_val
    
def main():
    if msg_fixa == True:
        mensagem_raw='\xe7\x0f\x70\x07\x01\x00\x00\x00\x00' \
                     '\xc0\x0d\x00\x00\x01\xf3\xe6\x00\x00' \
                     '\x40\x0d\x00\x00\x01\xfc\xff\x00\x00' \
                     '\x40\x0d\x00\x00\x01\xbd\xf4\x00\x00' \
                     '\x40\x0d\x00\x00\x01\x93\xf4\x00\x00' \
                     '\x80\x0c\x00\x00\xbe\xe5'
        msg_final=trata_msg(mensagem_raw)
        print msg_final
        checa_inicio(msg_final)
        val_master(msg_final)
        for i in range(5):
            info_motor(i+1,msg_final)
        checa_fim(msg_final)
    
    else:
        while(1):
            msg_final=trata_msg('\x00')
            if msg_final is not None:
                # checagem de pacote valido
                print msg_final
                checa_inicio(msg_final)
                val_master(msg_final)
                for i in range(5):
                    info_motor(i+1,msg_final)
                checa_fim(msg_final)
                #Obj_porta.close()

if __name__ == '__main__':
    main()
    
