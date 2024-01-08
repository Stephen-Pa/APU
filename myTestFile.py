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
                    
from belex_libs.game_of_life import (
    gosper_glider_gun_tutorial,
)

from belex_libs.arithmetic import add_u16
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
def placeIntsInVrCorrectWay(Belex, vr: VR, mark_vr: VR):
    '''
    this section of code will utilize the belex functions to add values
    into a desired vr with the use of a section mask vr

    Functions:
    Belex.Mask(value)
    -> this function takes a given value and converts it to a mask
    that will be used to put the value into the vr
    EX: given value is a string "56", then mask will output a mask
    object that will put a 1 into plat locations 5 and 6 (numerically
    this numeber is 96)
    EX: given value is an integer 53. a mask object is generated to
    mask sections 0,2,4,5

    write_to_marked(dst_vr,marker_vr,section_number,col_msk)
    -> this function writes 1s in the plat of the dst_vr 
    in the plat that corresponds to the position of the 1 
    in section_number of the marker_vr with the sections in the col_msk
    -> basic town explaination: 
        the function expects a second vr (marker_vr) to contain only a 1
        bit in some location. The section which this 1 is located is indicated
        by the section_number and the choosen section does not matter.
        The plat which the 1 is located does matter and becomes the 
        corresponding plat which the desired number will be written.
        The number to be written into the plat of the vr is determined by
        the col_msk argument. This can be a mask object, number, or string.
        ***the Belex.Mask function above can be used to convert an integer to
        a mask object that will indicate which positions in the vr need to be
        a 1 to get the corresponding number***. Can also use an integer (i only
        tried a single integer) that will mask out a section and give the
        corresponding number (EX number is 3, then section 3 will contain a number
        and the resulting stored number is 8). The same idea can be done with a string
        (EX: string is "15" then stored number is 34).
    '''
    RL[::] <= 0
    vr[::] <= RL()
    mark_vr[::] <= RL()
    section = 0 #section just needs to be consistant, section # doesnt matter
    RL[::] <= 1
    mark_vr[section] <= ~WRL()
    #place value at section location (position 0)
    col_mask = Belex.Mask(1)
    write_to_marked(vr,mark_vr,section,col_mask) #stand alone number represents column numbers
    #move the marker position to the right 1 place
    walk_marks_eastward(mark_vr,section)
    #place value at section location (position 3)
    write_to_marked(vr,mark_vr,section,2)
    #move the marker position to the right 1 place
    walk_marks_eastward(mark_vr,section)
    #place value at section location (position 2 and 6)
    write_to_marked(vr,mark_vr,section,"15")
    #move the marker position to the right 1 place
    walk_marks_eastward(mark_vr,section)
    print(str(Belex.glass(vr, plats=16, sections=16)))
    '''
    Ending Questions:
    - with this method, the mask sections still need to come from numbers.
    in the "game_of_life.py" file in the function called gosper_gun_write_initial_pattern,
    these values are hard coded. If a numpy array (to store values) and loop
    (to go through values) cannot be used, how do values get placed into the device?
    - I think i have a general idea of how the GL works, but what is the
    explaination for it?
    - 
    '''

@belex_apl
def placeIntsGen(Belex, vr: VR, temp: VR):
    #while is not correct in actual design i guess? but for testing
    #im going to use one
    x = 0
    RL[::] <= 0
    vr[::] <= RL()
    temp[::] <= RL()
    section = 0
    temp[section] <= ~WRL()
    while x < 10:
        num = x+1
        col_mask = Belex.Mask(num)
        write_to_marked(vr,temp,section,col_mask)
        walk_marks_eastward(temp,section)
        x+=1
    #done

@belex_apl
def addTwoVrs(Belex, dst: VR, vr1: VR, vr2: VR, temp: VR):
    placeIntsGen(vr1,temp)
    print(str(Belex.glass(vr1, plats=16, sections=16)))
    placeIntsGen(vr2,temp)
    print(str(Belex.glass(vr2, plats=16, sections=16)))
    #shift vr2 over by 1 to left (east)
    RL[::] <= vr2()
    vr2[::] <= WRL()
    #now try the add method
    add_u16(dst,vr1,vr2)
    #display the VR
    print(str(Belex.glass(dst, plats=16, sections=16)))
    '''
    Questions:
    - why does the last number that is inserted keep repeating?
    this example just adds numbers 1 through 10 together...

    '''

@parameterized_belex_test
def test_driver_place(diri: DIRI):
    vr0 = 0
    vr1 = 1
    temp = 2
    #placeIntsInVr(vr0,temp)
    placeIntsInVrFaster(vr0,temp)
    #placeIntsInVrFaster(vr1,temp)
    #addVrs(vr0,vr1,temp)

@parameterized_belex_test
def test_correct_add_values(diri: DIRI):
    vr = 0
    temp = 1
    placeIntsInVrCorrectWay(vr,temp)

@parameterized_belex_test
def test_add_two_vr(diri: DIRI):
    dst = 0
    vr1 = 1
    vr2 = 2
    temp = 3
    addTwoVrs(dst,vr1,vr2,temp)
