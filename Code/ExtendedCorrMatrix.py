import sqlite3;
import MapHapToRegion as map
import util_funcs as ut
import heapq
import copy
'''
This module aims to get all the k-word matching and corresponding counts for the
(mutate_site - AA change pair)
the output db should have the following demo columns:
pattern_id | word_length | text         | hap_id     |  count    |
3846385      2/3/4...     333A, 443L..     1-71        1/2/3..

1. Amend the k = 2 matrix generation for SimpleCorrMatrix to include the hap_id
2. find the k = 3 ones from the k = 2 matrix (adding a pair one element in the pair,
   the other not) and has overlapping hap id
3. continue on until there's no more pairs to add
'''
def WriteMutePatternId():
    '''
    Generate mute_pattern_id list with the columns
    id| site | to_which_aa
    There are in total 1-65 id
    '''
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    #180727: Fix for the deletion to consider it as a mutation pattern
    cmd1 = '''select site, to_which_aa from mute_specific_count_180727 group by site, to_which_aa'''
    cur.execute(cmd1)
    all = cur.fetchall()
    cmd = ''' INSERT INTO mute_pattern_id_180727 VALUES(?,?,?)'''
    for elem in all:
        id = ut.getSQLiteID("mute_pattern_id_180727")
        site = elem[0]
        to_which_aa = elem[1]
        temp_values = (id, site, to_which_aa)
        cur.execute(cmd,temp_values)
        conn.commit()





def LengthTwo():
    '''
    Export a list, with each element a tuple of 7 elements: mute_id first_mute_site, first_mute_AA, second_mute_site, second_mute_AA, corr_count, hap_with_mute
    '''
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd1 = '''select site, to_which_aa from mute_specific_count_180727 group by site, to_which_aa order by count(hap_id)'''
    cur.execute(cmd1)
    all = cur.fetchall()
    matrix = []
    matrix_hap = []
    for i in range(len(all)):
        matrix.append([0]*len(all))

    for i in range(len(all)):
        matrix_hap.append([None]*len(all))

    for i in range(len(all)):
        for j in range(len(all)):
            matrix_hap[i][j] = set()

    cmd2 = '''select hap_id, site, to_which_aa from mute_specific_count_180727'''
    cur.execute(cmd2)
    all_pairs = cur.fetchall()
    for tup in all_pairs:
        hap_i, site_i, to_which_aa_i = tup[0], tup[1], tup[2]
        pair_i = (site_i, to_which_aa_i)
        cmd3 = '''select site, to_which_aa from mute_specific_count_180727 where site != ? and  hap_id = ?'''
        cur.execute(cmd3, (site_i, hap_i))
        rs_i = cur.fetchall()
        ind = all.index(pair_i)
        for rem in rs_i:
            rem_ind = all.index(rem)
            matrix[ind][rem_ind] = matrix[ind][rem_ind] + 1

            matrix_hap[ind][rem_ind].add(hap_i)

    rs = []
    for i in range(len(all)):
        for j in range(i+1, len(all)):
            cmd_temp = ''' select id from mute_pattern_id_180727 where site = ? and to_which_aa = ?'''
            cur.execute(cmd_temp, (all[i][0],all[i][1]))
            res1 = cur.fetchall()[0]
            index1 = res1[0]
            cur.execute(cmd_temp, (all[j][0],all[j][1]))
            res2 = cur.fetchall()[0]
            index2 = res2[0]
            rs.append((index1, index2, matrix[i][j], list(matrix_hap[i][j])))
    return rs

def WriteTwoToSql():
    rs = LengthTwo()
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' INSERT INTO mute_corr_count_2_180727 VALUES(?,?,?,?,?)'''
    for elem in rs:
        pattern_id = ut.getSQLiteID("mute_corr_count_2_180727")
        word_length = 2
        line = ut.CatListToString([str(elem[0]),str(elem[1])])
        hap_id = ut.CatListToString(elem[3])
        count = elem[2]
        temp_values = (pattern_id, word_length, line, hap_id, count)
        cur.execute(cmd,temp_values)
        conn.commit()

def WriteAllSql():
    # Get the list of k = k_word amd k = 2
    k_word = 5
    rs = []
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd2 = ''' select * from mute_corr_count_2_180727 where count != 0 and word_length = 2 and count > 1'''
    cur.execute(cmd2)
    base = cur.fetchall()
    processed_base = []
    for elem in base:
        elem = list(elem)
        elem[2] = CatStringToList(elem[2])
        elem[3] = CatStringToList(elem[3])
        processed_base.append(elem)

#while True:
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' select * from mute_corr_count_2_180727 where count != 0 and word_length = ? and count > 4'''
    cur.execute(cmd, (k_word - 1,))
    all = cur.fetchall()

    # if all == []:
    #     return None

    processed_k = []
    for elem in all:
        elem = list(elem)
        elem[2] = CatStringToList(elem[2])
        elem[3] = CatStringToList(elem[3])
        processed_k.append(elem)

    #Start the extend process

    for ls in processed_k:
        for pair in processed_base:
            extended_ls, extended_hap = ExtendHelper(ls, pair)
            if extended_ls != -1:
                # print(ls)
                # print(pair)
                # print((extended_ls, extended_hap))
                temp = [None] * 2
                temp[0] = extended_ls
                temp[1] = extended_hap
                AppendOrMerge(rs, temp)

    # k_word += 1
    cmd_4 = ''' INSERT INTO mute_corr_count_2_180727 VALUES(?,?,?,?,?)'''
    for elem in rs:
        pattern_id = ut.getSQLiteID("mute_corr_count_2_180727")
        word_length = len(elem[0])
        line = ut.CatListToString(elem[0])
        hap_id = ut.CatListToString(elem[1])
        count = len(elem[1])
        temp_values = (pattern_id, word_length, line, hap_id, count)
        cur.execute(cmd_4,temp_values)
        conn.commit()




def AppendOrMerge(rs,tup):
    extended_ls = tup[0]
    extended_hap = tup[1]
    rs_ls = [elem[0] for elem in rs]
    if extended_ls not in rs_ls:
        rs.append(tup)
    else:
        index = [rs.index(elem) for elem in rs if elem[0] == extended_ls][0]
        rs_hap = rs[index][1]
        merged_hap = list(set(extended_hap) | set(rs_hap))
        rs[index][1] = merged_hap




def ExtendHelper(l, p):
    ls = copy.deepcopy(l)
    pair = copy.deepcopy(p)
    ls_line, pair_line, hap_id_ls, hap_id_pair = ls[2], pair[2], ls[3], pair[3]
    elem_1 = pair_line[0]
    elem_2 = pair_line[1]
    ls_only, pair_only, intersect = ut.OrganizeSet(hap_id_ls, hap_id_pair)
    if intersect == []:
        return -1, None
    elif ((elem_1 not in ls_line) and (elem_2 not in ls_line)):
        return -1, None
    elif ((elem_1 in ls_line) and (elem_2 in ls_line)):
        return -1, None
    elif ((elem_1 not in ls_line) and (elem_2 in ls_line)):
        ls_line.append(elem_1)
        return sorted(ls_line), intersect
    elif ((elem_1 in ls_line) and (elem_2 not in ls_line)):
        ls_line.append(elem_2)
        return sorted(ls_line), intersect

def CatStringToList(string):
    return [int(elem) for elem in string.split(",")]
