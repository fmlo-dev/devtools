# coding: utf-8

"""Control a FG and an SG by SCPI commands.

Note:
    This script is for the replica exam of LMT/FMLO.
    Please rewrite constants before you use the script.
    Execute the script where `scpi.py` is placed.
"""

# standard library
import sys
import time
if sys.version_info.major == 2:
    input = raw_input

# dependent packages
import scpi

# constants
IP_FG = 'xxx.xxx.xxx.xxx'
IP_SG = 'xxx.xxx.xxx.xxx'
PORT_FG = 8000
PORT_SG = 8000
TAU_TRIG = 0.0 # sec
TRIG_MODE = '1PPS' # 1PPS/FG/manual
FMP = '1.40E+10, 1.41E+10, 1.42E+10, 1.43E+10, 1.44E+10, 1.45E+10'


# main part
if __name__ == '__main__':
    # Initial settings
    FG = scpi.SCPI(IP_FG, port=PORT_FG)
    SG = scpi.SCPI(IP_SG, port=PORT_SG)

    # FG setup (t << -2.0 sec)
    FG.reset()
    # wave function
    FG.send('FREQ 10.0')
    FG.send('UNIT:ANGL DEG')
    FG.send('PHAS 0')
    FG.send('FUNC PULS')
    FG.send('FUNC:PULS:DCYC +5.0E+01')
    FG.send('FUNC:PULS:HOLD DCYC')
    FG.send('FUNC:PULS:TRAN +1.0E-08')
    # voltage
    FG.send('VOLT:HIGH +3.3E+00')
    FG.send('VOLT:LOW +0.0E+00')
    FG.send('VOLT:LIM:HIGH +3.4E+00')
    FG.send('VOLT:LIM:LOW -1.0E+00')
    FG.send('VOLT:LIM:STAT ON')
    # FG trigger (<-- 1pps)
    FG.send('TRIG:SOUR EXT')
    FG.send('TRIG:DELay {0:.9E}'.format(1.0-TAU_TRIG))
    FG.send('TRIG:SLOP POS')
    # burst mode
    FG.send('BURS:MODE TRIG')
    FG.send('BURS:NCYC INF')
    FG.send('BURS:STAT ON')
    # 10MHz ext oscillator
    FG.send('ROSC:SOUR EXT')
    # finally
    FG.send('INIT:CONT OFF')
    FG.send('OUTPut ON')

    # SG setup (t << -2.0 sec)
    SG.reset()
    SG.send('OUTP ON')
    SG.send('INIT:CONT OFF')
    SG.send('FREQ:MODE CW')
    # list sweep
    SG.send('LIST:TYPE LIST')
    SG.send('LIST:DWEL 1.0E-03')
    SG.send('LIST:FREQ {0}'.format(FMP))
    # SG trigger (<-- FG)
    SG.send('LIST:TRIG:SOUR EXT')
    # finally
    SG.send('FREQ:MODE LIST')

    try:
        # let FG wait for a trigger
        if TRIG_MODE == '1PPS':
            input('Hit return key to make FG trigger active.')
            FG.send('INIT:CONT ON')
        elif TRIG_MODE == 'FG':
            FG.send('SOUR2:FREQ 1.0')
            FG.send('SOUR2:FUNC PULS')
            FG.send('SOUR2:FUNC:PULS:DCYC 50.0')
            FG.send('SOUR2:VOLT 3.0')
            FG.send('OUTP2 ON')
            FG.send('INIT:CONT ON')
        elif TRIG_MODE == 'manual':
            input('Hit return key to trigger.')
            FG.send('TRIG')

        time.sleep(0.5)
        SG.send('INIT:CONT ON')

        # querying status
        for i in range(180):
            time.sleep(1.0)
            print('Remaining {0:3d} sec'.format(180-i))
            FG.send('SYSTem:ERRor?')
            FG.get()
            SG.send('SYSTem:ERRor?')
            SG.get()
    except:
        print('Interrupted by some error!')
    finally:
        # post processes after a scan
        FG.send('INIT:CONT OFF')
        FG.send('ABOR')
        FG.send('OUTP OFF')
        FG.send('OUTP2 OFF')
        SG.send('FREQ:MODE CW')
        SG.send('OUTP OFF')
