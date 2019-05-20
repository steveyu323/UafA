import sqlite3;
import MapHapToRegion as map
import util_funcs as ut
import heapq
def buildMatrix():
    '''
    Export a list, with each element a tuple of 5 elements: first_mute_site, first_mute_AA, second_mute_site, second_mute_AA, corr_count
    '''
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd1 = '''select site, to_which_aa from mute_specific_count group by site, to_which_aa order by count(hap_id)'''
    cur.execute(cmd1)
    all = cur.fetchall()
    matrix = []
    for i in range(len(all)):
        matrix.append([0]*len(all))


    cmd2 = '''select hap_id, site, to_which_aa from mute_specific_count'''
    cur.execute(cmd2)
    all_pairs = cur.fetchall()
    for tup in all_pairs:
        hap_i, site_i, to_which_aa_i = tup[0], tup[1], tup[2]
        pair_i = (site_i, to_which_aa_i)
        cmd3 = '''select site, to_which_aa from mute_specific_count where site != ? and  hap_id = ?'''
        cur.execute(cmd3, (site_i, hap_i))
        rs_i = cur.fetchall()
        ind = all.index(pair_i)
        for rem in rs_i:
            rem_ind = all.index(rem)
            matrix[ind][rem_ind] = matrix[ind][rem_ind] + 1

    rs = []
    for i in range(len(all)):
        for j in range(i+1, len(all)):
            rs.append((all[i][0],all[i][1],all[j][0],all[j][1], matrix[i][j]))
    return rs

def WriteToSql():
    rs = buildMatrix()
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' INSERT INTO mute_corr_count VALUES(?,?,?,?,?)'''
    for elem in rs:
        first_mute_site = elem[0]
        first_mute_AA = elem[1]
        second_mute_site = elem[2]
        second_mute_AA = elem[3]
        corr_count = elem[4]
        temp_values = (first_mute_site, first_mute_AA, second_mute_site, second_mute_AA, corr_count)
        cur.execute(cmd,temp_values)
    conn.commit()
