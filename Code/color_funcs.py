from pymol import cmd, stored
import util_funcs as ut


def ColorByArray(arr,col):
    '''
    Take in an array of target pymol indexes and a string color
    '''
    for i in arr:
        i_resi = "resi" + " " + str(i)
        #cmd.set(name = "cartoon_transparency", value = "0", selection = i_resi)
        cmd.show(representation="surface", selection= i_resi )
        #cmd.show(representation="sticks", selection= i_resi )
        cmd.color(color = col, selection = i_resi)
        cmd.set(name = "transparency", value = "0.0", selection = i_resi)

def GetResiSelection(arr):
    '''
    Take in an array of target pymol indexes and a string color
    '''
    print("in")
    rs = ""
    for i in arr:
        i_resi = "(" + "resi" + " " + str(i) + ")"
        #cmd.set(name = "cartoon_transparency", value = "0", selection = i_resi)
        #cmd.show(representation="surface", selection= i_resi )
        rs = i_resi + "&" + rs
        print(rs)

    return rs
