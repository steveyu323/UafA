import sqlite3;
import MapHapToRegion as map
import util_funcs as ut
import heapq



def main():
    rs = getSiteFreq()
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' INSERT INTO mute_count VALUES(?,?,?)'''
    for elem in rs:
        mute_site = elem[1]
        num_mutants_in_all_hap = elem[0]
        func_region = elem[2]
        temp_values = (mute_site, num_mutants_in_all_hap, func_region)
        cur.execute(cmd,temp_values)
    conn.commit()


def getSiteFreq():
    '''
    Create a new table named mute_count that has the following column:
    site_pymol_index | # of mutants in all haplotypes | whether is on a region of target
    and then export the result of :
    1. the site mutation count order
    2. the region mutation count order
    h里面有count和site，
    '''

    def heapsort(iterable):
        h = []
        for value in iterable:
            heapq.heappush(h, value)
        return [heapq.heappop(h) for i in range(len(h))]


    # Get a frequency priority list
    freq = ut.FindFreqAll()
    index_ls, pymol_index = ut.GetBothIndexes()
    index = ut.GetAllIndex(index_ls)
    h = []
    for i in range(len(freq)):
        h.append((freq[i] ,index[i],getSiteFuncRegion(index[i])))
    heapsort(h)

    return h


def getSiteFuncRegion(index):
    '''
    return 0 if the site if not in the curated regions
    or return the number of the region as in hap_func_match lable
    '''
    region_index = 0
    mutate_input, mutate_input_name, mutate_color = ut.GetReportedRegions()

    for i in range(len(mutate_input)):
        mutate_ls = mutate_input[i]
        if (index in mutate_ls):
            region_index = i + 1
    return region_index
