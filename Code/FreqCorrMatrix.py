import sqlite3;
import MapHapToRegion as map
import util_funcs as ut
import heapq
import copy

'''
This module will output the new corr_matrix table 'mute_corr_freq' with the corr_freq counted as
p(A1A2)/p(A1)p(A2), with the p() as the count of that particular pattern
the output db should have the following demo columns:
pattern_id| word_length| line| hap_id| corr_freq

1. After the word_length = 2 is outputted, should compare it with the previous mute_corr_count table
2. Discuss how to calculate the freq with a word_length larger than 2

'''
def getSingleCount(pattern_id):
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    # Get the count for a1 and a2 individually
    # 1. Get the site and to_which_aa from querying the mute_pattern_id
    cmd1 = ''' select site, to_which_aa from mute_pattern_id_180727  where id = ?'''
    cur.execute(cmd1,(pattern_id,))
    rs = cur.fetchall()[0]
    this_site = rs[0]
    print(rs)
    this_aa = rs[1]
    cmd2 = '''select count(hap_id) from mute_specific_count_180727 where site = ? and to_which_aa = ?'''
    cur.execute(cmd2,(this_site, this_aa))
    rs_count = cur.fetchall()[0]
    return rs_count[0]




def main():
    '''
    @author Changhua Yu
    @Date 180726
    '''
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    #180727: Fix for the deletion to consider it as a mutation pattern
    cmd1 = '''select pattern_id, word_length, line, hap_id, count from mute_corr_count_2_180727 where word_length = 2 and count > 0'''
    cur.execute(cmd1)
    all = cur.fetchall()

    cmd2 = ''' INSERT INTO mute_corr_freq VALUES(?,?,?,?,?)'''
    for elem in all:
        pattern_id = elem[0]
        word_length = elem[1]
        line = elem[2]
        line_ls = ut.CatStringToList(elem[2])
        hap_id = elem[3]
        hap_id_ls = ut.CatStringToList(elem[3])
        count_a1a2 = elem[4]
        count_a1 = getSingleCount(line_ls[0])
        count_a2 = getSingleCount(line_ls[1])
        corr_freq = pow(count_a1a2,2)/(count_a1 * count_a2)
        temp_values = (pattern_id,word_length,line,hap_id,corr_freq)
        cur.execute(cmd2,temp_values)
        conn.commit()
    print("Done")
