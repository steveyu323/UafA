import sqlite3;



def main():
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    dict_index, hap_mutate_sites = GetDictIndexAndSites()
    cmd = ''' INSERT INTO raw_sequence VALUES(?, ?)'''
    for i in range(len(dict_index)):
        temp_values = (dict_index[i], hap_mutate_sites[i])
        cur.execute(cmd,temp_values)
    conn.commit()
    return None



def GetDictIndexAndSites():
    filename = "../Seq/uafA Protein sequence.txt"
    #Initialize a freq_table
    ls_1 = list("0000011111112222223333333333334444444455555555555566666666666666666666677777777777788")
    singleMutateTable = [None] * len(ls_1)
    # parse in the file
    in_file = open(filename, "rt")
    lines = []
    for line in in_file:
        lines.append(line.rstrip('\n'))
    lines_used = lines[13:]
    # Get a dictionary with hap index and line number in the txt file
    dict_index = [None]*len(lines_used)
    hap_mutate_sites = [None]*len(lines_used)
    for i in range(len(lines_used)):
        # separate the title and the matching of each lien
        temp = lines_used[i].split()
        temp_index = temp[0]
        hap_index = int(temp_index[5:7])
        dict_index[i] =  hap_index


        temp_align = temp[1:]
        temp_align[:] = [''.join(temp_align[:])]
        hap_mutate_sites[i] = temp_align[0]

    return dict_index, hap_mutate_sites
