from pymol import cmd, stored
import util_funcs as ut
import color_funcs as co
import sqlite3;
import MapHapToRegion as map
import heapq
import copy

'''
@author Changhua Yu
@date 180617
This module aim to scratch information from mute_corr_count_2 table
and to create visualization of the position of the correlated mutations on the
pymol model


1. Design a Threshold for plotting
2. Restrict to the pymol range
3. Color by array
'''

'''
180618: For now just humanly select 10 significant sequence to plotting
1.[29,43,48,30,92]
2.[11,16,19,65,84,92]
3.[35,50,55,84,88,92]
4.[44, 50, 87, 92]

'''
source = [[29,43,48,30,92], [11,16,19,65,84,92], [35,50,55,84,88,92], [44, 50, 87, 92]]

def getIndexFromPatternId(ls):
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    rs = []
    for elem in ls:
        cmd1 = '''select site from mute_pattern_id where id = ?'''
        cur.execute(cmd1,(elem,))
        all = cur.fetchall()
        temp = all[0][0]
        rs.append(temp)
    return rs

def PlotEach():
    for i in range(len(source)):
        lis = source[i]
        ls = getIndexFromPatternId(lis)
        print(ls)
        #Initialization: show chainbow transparent surface
        cmd.reinitialize()
        cmd.fetch ("3IS1")
        cmd.hide(representation = "",selection = "all")
        cmd.show("cartoon", "all")
        #cmd.show("surface", "all")
        util.chainbow("3IS1")
        #cmd.hide(representation = "cartoon",selection = "all")
        #cmd.color(color = "white", selection = "all")
        cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")
        co.ColorByArray(ls,"red")

        filename = "../out/ViewAdjacency/" + str(i)+ ".pse"
        # picture_name = "../out/ViewAdjacency/" + str(i)+ ".png"
        # cmd.save(picture_name)

        cmd.save(filename)

    cmd.extend( "PlotEach", PlotEach);

def PlotEachWithFuncRegion():
    for i in range(len(source)):
        lis = source[i]
        ls = getIndexFromPatternId(lis)
        print(ls)
        mutate_input, mutate_input_name, mutate_color = ut.GetReportedRegions()
        mutate_input_all = []
        for ll in mutate_input:
            mutate_input_all += ll

        #Initialization: show chainbow transparent surface
        cmd.reinitialize()
        cmd.fetch ("3IS1")
        cmd.hide(representation = "",selection = "all")
        cmd.show("cartoon", "all")
        #cmd.show("surface", "all")
        util.chainbow("3IS1")
        #cmd.hide(representation = "cartoon",selection = "all")
        #cmd.color(color = "white", selection = "all")
        cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")

        for ll in mutate_input:
            col = mutate_color[mutate_input.index(ll)]
            co.ColorByArray(ll,col)

        arr_1_only, arr_2_only, intersect = ut.OrganizeSet(mutate_input_all, ls)
        co.ColorByArray(intersect,"red")
        co.ColorByArray(arr_2_only,"blue")
        cmd.png("../out/ViewAdjacency/" + "with_func" + str(i)+ ".png")
        filename = "../out/ViewAdjacency/" + "with_func" + str(i)+ ".pse"
        #picture_name = "../out/ViewAdjacency/" + "with_func" + str(i)+ ".png"

        cmd.save(filename)
    cmd.extend( "PlotEachWithFuncRegion", PlotEachWithFuncRegion);
