import sqlite3;
import MapHapToRegion as map
import util_funcs as ut
import heapq

'''
@author Changhua Yu
@date 180611
This module build a table called mute_specific_count
hap_id | site | to_which_AA
and then output the result of c count id group by a specific (site,AA) pair
'''
def main():
    rs = get()
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' INSERT INTO mute_specific_count_180727 VALUES(?,?,?)'''
    for elem in rs:
        site = elem[1]
        hap_id = elem[0]
        to_which_AA = elem[2]
        temp_values = (hap_id, site, to_which_AA)
        cur.execute(cmd,temp_values)
    conn.commit()

def get():
    rs = []
    dict_index, lines_used, pymol_index, index_ls = ut.GetDictIndex()
    index = ut.GetAllIndex(index_ls)
    print(len(index))
    for ind in dict_index:
        print(ind)
        dict_hap_site = ut.getSingleHapMutateSites(ind)
        print(len(dict_hap_site))
        for i in range(len(index)):
            if dict_hap_site[i] != '.':
                rs.append((ind, index[i], dict_hap_site[i]))
        	#Change to fix the deletion issue 180726
            #if dict_hap_site[i] != '.' and dict_hap_site[i] != '-':
                

    return rs
