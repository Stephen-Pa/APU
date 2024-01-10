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
from belex_libs.arithmetic import mul_u16
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
    #place value at section location (position 3)
    write_to_marked(vr,mark_vr,section,2)
    #move the marker position to the right 1 place
    walk_marks_eastward(mark_vr,section)
    #place value at section location (position 0)
    col_mask = Belex.Mask(15)
    write_to_marked(vr,mark_vr,section,col_mask) #stand alone number represents column numbers
    #move the marker position to the right 1 place
    walk_marks_eastward(mark_vr,section)
    #place value at section location (position 2 and 6)
    write_to_marked(vr,mark_vr,section,"135")
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
    x = 50
    RL[::] <= 0
    vr[::] <= RL()
    temp[::] <= RL()
    section = 0
    temp[section] <= ~WRL()
    #put in 10 values
    for _ in range(11):
        num = x
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

@belex_apl
def multInt(Belex, dst: VR, vr1: VR, vr2: VR, temp: VR):
    #consider two vrs with one element in each, do mutliply on elements
    RL[::] <= 0
    dst[::] <= RL()
    #considers worst case scenario which two numbers are both 8 bits long
    #which would be 255*255 = 65025, which is less than the max of 65535
    #Note: this can be increased, but there can be overflow

    #if loop is problem, loop unravel
    for _ in range(8):
        #get which numbers in v2 to be added to sum for mult result
        RL[0] <= vr1()
        GL[0] <= RL()
        RL[::] <= vr2() & GL()
        #store numbers and add to final
        temp[::] <= RL()
        add_u16(dst,temp,dst)
        #can these two steps be done in parallel with RL and GL?
        #now shift vr1 down
        RL[::] <= vr1()
        vr1[::] <= SRL()
        #now shift vr2 up
        RL[::] <= vr2()
        vr2[::] <= NRL()
    print(str(Belex.glass(dst, plats=16, sections=16)))

@belex_apl
def sumVr(Belex, dst: VR):
    #this method sums the numbers in a VR
    #x determines how many elements are summed
    #and can be changed to sum more elements in the VR
    temp = Belex.VR(0)
    x = 256
    while x:
        RL[::] <= dst()
        for _ in range(x):
            temp[::] <= ERL()
            RL[::] <= temp()
        #now add
        add_u16(dst,temp,dst)
        x = int(x/2)

@belex_apl
def myMatrixMult(Belex, vec: VR):
    #performs MAC op on this matrix
    #             [1 ,2 ,3 ,4 ,5 ,6 ]
    #             [7 ,8 ,9 ,10,11,12]
    # [1,2,3,4] * [13,14,15,16,17,18]
    #             [19,20,21,22,23,24]
    #result
    #
    #
    # [130,140,150,160,170,180]
    #
    c1 = Belex.VR(0)
    c2 = Belex.VR(0)
    c3 = Belex.VR(0)
    c4 = Belex.VR(0)
    c5 = Belex.VR(0)
    c6 = Belex.VR(0)
    dst = Belex.VR(0)
    temp = Belex.VR(0)
    mark_vr = Belex.VR(0)
    #put row vector into vr
    RL[::] <= 0
    vec[::] <= RL()
    mark_vr[::] <= RL()
    section = 0 #section just needs to be consistant, section # doesnt matter
    RL[::] <= 1
    mark_vr[section] <= ~WRL()
    #fill vrs in each plat, this one is the first plat
    #(from vec,c1,c2,c3,c4,c5,c6 => 4,19,20,21,22,23,24)
    col_mask = Belex.Mask(4)
    write_to_marked(vec,mark_vr,section,col_mask)
    col_mask = Belex.Mask(19)
    write_to_marked(c1,mark_vr,section,col_mask)
    col_mask = Belex.Mask(20)
    write_to_marked(c2,mark_vr,section,col_mask)
    col_mask = Belex.Mask(21)
    write_to_marked(c3,mark_vr,section,col_mask)
    col_mask = Belex.Mask(22)
    write_to_marked(c4,mark_vr,section,col_mask)
    col_mask = Belex.Mask(23)
    write_to_marked(c5,mark_vr,section,col_mask)
    col_mask = Belex.Mask(24)
    write_to_marked(c6,mark_vr,section,col_mask)
    #finally shift
    walk_marks_eastward(mark_vr,section)
    #fill vrs in each plat, this is the second plat
    #(from vec,c1,c2,c3,c4,c5,c6 => 3,13,14,15,16,17,18)
    col_mask = Belex.Mask(3)
    write_to_marked(vec,mark_vr,section,col_mask)
    col_mask = Belex.Mask(13)
    write_to_marked(c1,mark_vr,section,col_mask)
    col_mask = Belex.Mask(14)
    write_to_marked(c2,mark_vr,section,col_mask)
    col_mask = Belex.Mask(15)
    write_to_marked(c3,mark_vr,section,col_mask)
    col_mask = Belex.Mask(16)
    write_to_marked(c4,mark_vr,section,col_mask)
    col_mask = Belex.Mask(17)
    write_to_marked(c5,mark_vr,section,col_mask)
    col_mask = Belex.Mask(18)
    write_to_marked(c6,mark_vr,section,col_mask)
    #finally shift
    walk_marks_eastward(mark_vr,section)
    #fill vrs in each plat, this is third plat
    #(from vec,c1,c2,c3,c4,c5,c6 => 2,7,8,9,10,11,12)
    col_mask = Belex.Mask(2)
    write_to_marked(vec,mark_vr,section,col_mask)
    col_mask = Belex.Mask(7)
    write_to_marked(c1,mark_vr,section,col_mask)
    col_mask = Belex.Mask(8)
    write_to_marked(c2,mark_vr,section,col_mask)
    col_mask = Belex.Mask(9)
    write_to_marked(c3,mark_vr,section,col_mask)
    col_mask = Belex.Mask(10)
    write_to_marked(c4,mark_vr,section,col_mask)
    col_mask = Belex.Mask(11)
    write_to_marked(c5,mark_vr,section,col_mask)
    col_mask = Belex.Mask(12)
    write_to_marked(c6,mark_vr,section,col_mask)
    #finally shift
    walk_marks_eastward(mark_vr,section)
    #fill vrs in each plat, this is the fourth plat
    #(from vec,c1,c2,c3,c4,c5,c6 => 1,1,2,3,4,5,6)
    col_mask = Belex.Mask(1)
    write_to_marked(vec,mark_vr,section,col_mask)
    col_mask = Belex.Mask(1)
    write_to_marked(c1,mark_vr,section,col_mask)
    col_mask = Belex.Mask(2)
    write_to_marked(c2,mark_vr,section,col_mask)
    col_mask = Belex.Mask(3)
    write_to_marked(c3,mark_vr,section,col_mask)
    col_mask = Belex.Mask(4)
    write_to_marked(c4,mark_vr,section,col_mask)
    col_mask = Belex.Mask(5)
    write_to_marked(c5,mark_vr,section,col_mask)
    col_mask = Belex.Mask(6)
    write_to_marked(c6,mark_vr,section,col_mask)
    #mult the vectors
    #c1
    RL[::] <= vec()
    temp[::] <= RL()
    multInt(dst,temp,c1,mark_vr)
    RL[::] <= dst()
    c1[::] <= RL()
    #c2
    RL[::] <= vec()
    temp[::] <= RL()
    multInt(dst,temp,c2,mark_vr)
    RL[::] <= dst()
    c2[::] <= RL()
    #c3
    RL[::] <= vec()
    temp[::] <= RL()
    multInt(dst,temp,c3,mark_vr)
    RL[::] <= dst()
    c3[::] <= RL()
    #c4
    RL[::] <= vec()
    temp[::] <= RL()
    multInt(dst,temp,c4,mark_vr)
    RL[::] <= dst()
    c4[::] <= RL()
    #c5
    RL[::] <= vec()
    temp[::] <= RL()
    multInt(dst,temp,c5,mark_vr)
    RL[::] <= dst()
    c5[::] <= RL()
    #c6
    RL[::] <= vec()
    temp[::] <= RL()
    multInt(dst,temp,c6,mark_vr)
    RL[::] <= dst()
    c6[::] <= RL()
    #sum the vrs
    sumVr(c1)
    sumVr(c2)
    sumVr(c3)
    sumVr(c4)
    sumVr(c5)
    sumVr(c6)
    #results from MAC operation stored in the first plat
    print(str(Belex.glass(c1, plats=1, sections=16)))
    print(str(Belex.glass(c2, plats=1, sections=16)))
    print(str(Belex.glass(c3, plats=1, sections=16)))
    print(str(Belex.glass(c4, plats=1, sections=16)))
    print(str(Belex.glass(c5, plats=1, sections=16)))
    print(str(Belex.glass(c6, plats=1, sections=16)))


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

@parameterized_belex_test
def test_mult(diri: DIRI):
    #my mult
    dst = 0
    vr = 1
    vr2 = 2
    temp = 3
    placeIntsGen(vr,temp)
    placeIntsGen(vr2,temp)
    multInt(dst,vr,vr2,temp)
    #Question:
    #when i use this multiply that i made, after a certain
    #magnitude of numbers to be multiplied together (say 50*50)
    #the following error is thrown:
    #myTestFile.py::test_mult - RuntimeError: Exhausted SM_REG registers
    #HOWEVER, the multiplied numbers are correct when numbers multiplied
    #together will not overflow

@parameterized_belex_test
def test_mul_u16(diri: DIRI):
    #artimetic function in belex
    #gives error as follows: 
    #myTestFile.py::test_mul_u16 - 
    #KeyError: 'Register value for RN_REG_12 has not been initialized.'
    dst = 0
    vr = 1
    vr2 = 2
    temp = 3
    placeIntsGen(vr,temp)
    placeIntsGen(vr2,temp)
    mul_u16(dst,vr,vr2)

@parameterized_belex_test
def test_add_vr(diri: DIRI):
    #tests the sumVR method with values from vr filling method
    dst = 0
    marker = 1
    placeIntsInVrCorrectWay(dst,marker)
    sumVr(dst)

@parameterized_belex_test
def test_matrix_mult(diri: DIRI):
    #just initiates the matrix mult with random vector
    startVec = 0
    myMatrixMult(startVec)