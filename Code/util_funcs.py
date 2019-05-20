import sqlite3;

def GetMutatedSites():
    '''
    @Goal: To Get the list of mutated site in exactly as in MEGA file
    '''
    rs = []
    # in_file = open(filename, "rt")
    # lines = []
    # for line in in_file:
    #     lines.append(line.rstrip('\n'))
    ls_1 = list("0000011111112222223333333333334444444455555555555566666666666666666666677777777777788")
    ls_2 = list("0359902345890345560033445666790112335801223344468811255677888889999999901222355567701")
    ls_3 = list("8073856640908564952427029237125674287358014927831415934147027891234567801034845934602")
    for i in range(len(ls_1)):
        elem_1, elem_2, elem3 = int(ls_1[i]), int(ls_2[i]), int(ls_3[i])
        rs.append(elem_1 * 100 + elem_2 * 10 + elem3)
    return rs

def GetPymolIndex(index_ls):
    '''
    @Goal to get the correct index in PyMol 3IS1 model from MEGA file index range only within the crystal display region
    '''
    rs = list()
    for elem in index_ls:
        if elem < 392 or elem == 717 or elem == 718:
            continue
        elif elem < 717:
            rs.append(elem)
        elif elem > 718:
            rs.append(elem - 2)
    return rs

def GetAllIndex(index_ls):
    '''
    Get the pymol index as well as the N1 region with the correct index
    '''
    rs = list()
    for elem in index_ls:
        if elem < 392:
            rs.append(elem)
        elif elem < 717:
            rs.append(elem)
        elif elem == 717 or elem == 718:
            continue
        elif elem > 718:
            rs.append(elem - 2)
    return rs

def GetBothIndexes():
    '''
    @Geal: to yield both index in txt and index in pymol
    '''
    index_ls = GetMutatedSites()
    pymol_index = GetPymolIndex(index_ls)
    return index_ls, pymol_index

def GetTxtBody():
    filename = "../Seq/uafA Protein sequence.txt"
    # parse in the file
    in_file = open(filename, "rt")
    lines = []
    for line in in_file:
        lines.append(line.rstrip('\n'))
    lines_used = lines[13:]
    return lines_used

def GetAlignList(line):
    temp = line.split()
    # should be ['xxxxx', 'xxxxx']
    temp = temp[1:]
    temp[:] = [''.join(temp[:])]
    # should be ['a','b','c'...]
    temp_str_ls = list(temp[0])
    return temp_str_ls

def GetIndexList(line):
    # separate the title and the matching of each lien
    temp = line.split()
    temp_index = temp[0]
    hap_index = int(temp_index[5:7])
    return hap_index

def FindFreqAll():
    '''
    The find freq function that extends to the non-pymol visualized region
    '''
    index_ls, pymol_index = GetBothIndexes()
    index = GetAllIndex(index_ls)
    #Initialize a freq_table
    freq_table = [0] * len(index_ls)
    #Parse in Body
    lines_used = GetTxtBody()
    # Check whether there's a point mutation for each line
    for line in lines_used:
        temp_str_ls = GetAlignList(line)
        for j in range(len(temp_str_ls)):
            if temp_str_ls[j] != '.' and temp_str_ls[j] != '-':
                freq_table[j] += 1
    return freq_table

def FindFreq():
    index_ls, pymol_index = GetBothIndexes()
    pymol_index
    #Initialize a freq_table
    freq_table = [0] * len(index_ls)
    #Parse in Body
    lines_used = GetTxtBody()
    # Check whether there's a point mutation for each line
    for line in lines_used:
        temp_str_ls = GetAlignList(line)
        for j in range(len(temp_str_ls)):
            if temp_str_ls[j] != '.' and temp_str_ls[j] != '-':
                freq_table[j] += 1

    pymol_freq = FilterToModelRange(freq_table)
    print(pymol_freq)
    # PymolFreq = [float(i)/max(PymolFreq) for i in PymolFreq]
    pymol_freq = [float(i)/12.0 for i in pymol_freq]
    return pymol_freq

def FilterToModelRange(arr):
    '''
    arr should be with the same length as index_ls and will turn to the length of pymol_index
    '''
    index_ls, pymol_index = GetBothIndexes()
    rs = [arr[i] for i in range(len(index_ls)) if not (index_ls[i] < 392 or index_ls[i] == 717 or index_ls[i] == 718)]
    return rs

def GetDictIndex():
    '''
    return an array with with the numbering of haplotype correlate to line index start from line 13
    along with some other useful output for cache
    '''
    index_ls, pymol_index = GetBothIndexes()
    lines_used = GetTxtBody()
    # Get a dictionary with hap index and line number in the txt file
    dict_index = [None]*len(lines_used)
    for i in range(len(lines_used)):
        dict_index[i] =  GetIndexList(lines_used[i])

    return dict_index, lines_used, pymol_index, index_ls

def getSingleHapMutateSites(hap_index):
    '''
    return the mutated site array for the selected hap_index, restricted to pymol display region
    '''
    dict_index, lines_used, pymol_index, index_ls = GetDictIndex()
    # Get the line index in lines_used from the dict_index
    line_index = dict_index.index(hap_index)
    dict_hap_site = GetAlignList(lines_used[line_index])
    return dict_hap_site
    #rs = FilterToModelRange(dict_hap_site)
    #return rs

def GetReportedRegions():
    # The inputs from literature
    mutate_input = []
    mutate_input_name = []
    mutate_input.append(list(range(689,695))) # N3-B loop
    mutate_input_name.append("N3-B loop")
    mutate_input.append([423,459,460,461,514,515,520,545,553,554,555,557,608,609,611,685]) #N2-N3 interface
    mutate_input_name.append("N2-N3 interface")
    mutate_input.append([392,442,460,464,474,475,493,494,693,728,730,733,736,749,751])
    mutate_input_name.append("N2-B interface")
    mutate_input.append([775,780,778,709,714]) # Mostly not present on the pymol model
    mutate_input_name.append("B loop stabilized by K")
    mutate_input.append(list(range(489,498)))
    mutate_input_name.append("latch motif")
    #mutate_color = ["red","green","yellow","cyan", "blue"]
    mutate_color = ["yellow","green","purple","orange", "greencyan"]
    return mutate_input, mutate_input_name, mutate_color


def OrganizeSet(arr_1, arr_2):
    '''
    export a array with 3 parts splited: arr_1 only, arr_2 only, overlapped
    '''
    set_1 = set(arr_1)
    set_2 = set(arr_2)
    intersect = set_1.intersection(set_2)
    set_1_only = set_1 - set_2
    set_2_only = set_2 - set_1
    rs = [None] * 3
    return list(set_1_only), list(set_2_only), list(intersect)


def GetHapMutatedIndex(hap_index):
    '''
    get the index of the mutated indexes of a haplotype by the hap_id
    '''
    dict_index, lines_used, pymol_index, index_ls = GetDictIndex()
    dict_hap_site = getSingleHapMutateSites(hap_index)
    rs = []
    for i in range(len(pymol_index)):
        if dict_hap_site[i] != '.' and dict_hap_site[i] != '-':
            rs.append(pymol_index[i])
    return rs

def CatListToString(list):
    '''
    cat a list of number/strings to a single string delimited by ',' for sqlite insertion
    '''
    temp = [str(x) for x in list]
    temp[:] = [','.join(temp[:])]
    return temp[0]


def CatStringToList(string):
    return [int(elem) for elem in string.split(",")]

def getSQLiteID(table_name):
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = '''select count(*) from '''
    cur.execute(cmd + table_name)
    count = cur.fetchall()
    count[0][0] + 1
    return count[0][0] + 1
