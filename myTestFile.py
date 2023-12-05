import numpy as np
from belex.common.constants import (NUM_HALF_BANKS_PER_APUC,
                                    NUM_PLATS_PER_HALF_BANK)
from belex.diri.half_bank import DIRI
from belex.literal import (GL, INV_GL, INV_RL, NRL, RL, VR, WRL,
                           ERL, SRL, Mask, Section, RSP16,
                           apl_commands, belex_apl)
from belex.utils.example_utils import convert_to_u16

from belex_libs.common import cpy_imm_16, cpy_imm_16_to_rl
from belex_libs.tartan import (walk_marks_eastward,
                               write_markers_in_plats_matching_value,
                               write_to_marked)

from belex_tests.utils import parameterized_belex_test

from collections import deque 

@belex_apl
def placeIntsInVr(Belex, vr: VR, temp: VR):
    #This function takes a numpy array of int16 and stores it into a vr
    print()
    listVal = [1,2,3,4,5,6]
    listVal = np.array(listVal).astype('int16')
    #reset vr
    RL[:] <= 0
    vr[:] <= RL()
    #prep index 15 with a 1 in first plat
    RL[:] <= 1
    temp[15] <= ~WRL()
    RL[15] <= temp()

    i=0
    #for each bit position
    while i < 15:
        j=(len(listVal)-1)
        #for each value to add
        while j > -1:
            #start with LSB to MSB
            #bit position is a 1
            if listVal[j] & 1:
                RL[15] <= vr() | RL()
                vr[15] <= RL()
            #shift vr contents
            RL[15] <= vr()
            vr[15] <= WRL()
            #reset RL for next pass
            RL[15] <= temp()
            #take the entry in the list and shift
            listVal[j] = listVal[j]>>1
            j-=1
        #shift all entries down
        RL[:] <= vr()
        vr[:] <= SRL()
        RL[:] <= temp()
        i+=1
    RL[:] <= vr()
    vr[:] <= ERL()
    print(str(Belex.glass(vr, plats=16, sections=16)))

@belex_apl
def placeIntsInVrFaster(Belex, vr: VR, temp: VR):
    print()
    listVal = [1,2,3,3,5,6]
    listVal = np.array(listVal).astype('int16')
    #reset vr
    RL[:] <= 0
    vr[:] <= RL()
    #prep first plat with all 1s
    RL[:] <= 1
    temp[:] <= ~WRL()

    x=0
    while x < len(listVal):
        #reset RL
        RL[:] <= 0
        #convert list to hex and str for mask
        hexStr = str(hex(listVal[x]))
        RL[hexStr] = 1
        RL[:] <= temp() & RL()
        #put val into retVR
        RL[:] <= vr() | RL()
        vr[:] <= RL()
        #shift temp
        RL[:] <= temp()
        temp[:] <= WRL()
        x+=1
    print(str(Belex.glass(vr, plats=16, sections=16)))

@belex_apl
def addVrs(Belex, vrA: VR, vrB: VR, vrRet: VR):
    x = 0 
    RL[:] <= 0
    vrRet[:] <= RL()
    #one less because last has to be done differently
    while x < 15:
        #store carry
        RL[x] <= vrRet()
        RL[(x+1)] <= NRL()
        #sum
        RL[x] <= vrA() ^ vrB() ^ vrRet()
        #store sum
        vrRet[x] <= RL()
        #part of carry
        RL[x] <= vrA() & vrB()
        vrRet[(x+1)] <= NRL()
        #calc the other carry part
        RL[x] <= SRL()
        RL[x] <= RL() & vrRet()
        #get final carry result
        RL[(x+1)] <= NRL()
        RL[(x+1)] <=RL() | retVR()
        #store the carry vrRet for next rep
        retVR[(x+1)] <= RL()
        x+=1
    #last section, drop carry
    RL[x] <= vrA() ^ vrB() ^ vrRet()
    vrRet[x] <= RL[x]
    print(str(Belex.glass(vrRet, plats=16, sections=16)))


@parameterized_belex_test
def test_driver_place(diri: DIRI):
    vr0 = 0
    vr1 = 1
    temp = 2
    #placeIntsInVr(vr0,temp)
    placeIntsInVrFaster(vr0,temp)
    #placeIntsInVrFaster(vr1,temp)
    #addVrs(vr0,vr1,temp)



@belex_apl
def exercise_2(Belex, sb: VR):

    # BELEX takes 'sb', being the first parameter of this FUT
    # (function under test), implicitly as containing the actual
    # values to check against expected values in the C-sim. The
    # expected values are in the SB returned from the test
    # function, 'test_exercise_2', below. DIRI computes the
    # expected values, so DIRI is the "ground truth" for C-sim.

    os = "0x0001"
    fs = "0xFFFF"

    RL[fs] <= 0
    RL[os] <= 1
    sb[os] <= RL()


@parameterized_belex_test
def test_exercise_2(diri: DIRI):
    sb = 7
    exercise_2(sb)
    print(str(convert_to_u16(diri.hb[sb])))
    assert all(convert_to_u16(diri.hb[sb]) == 0x0001)
    return sb  # expected values in SB[7]