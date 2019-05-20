import sqlite3;

def main():
    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute(''' SELECT hap_id FROM raw_sequence''')
    hap_ids = cur.fetchall()


    txt_indexes = GetMutatedSites()
    cmd_1 = ''' SELECT string_aligned_full FROM raw_sequence WHERE hap_id = '''
    for hap_id in hap_ids:
        for txt_index in txt_indexes:
            cmd_2 = cmd_1 + str(hap_id)


def GetMutatedSites():
    '''
    To Get the list of mutated site in MEGA file
    '''
    rs = []
    ls_1 = list("0000011111112222223333333333334444444455555555555566666666666666666666677777777777788")
    ls_2 = list("0359902345890345560033445666790112335801223344468811255677888889999999901222355567701")
    ls_3 = list("8073856640908564952427029237125674287358014927831415934147027891234567801034845934602")
    for i in range(len(ls_1)):
        elem_1, elem_2, elem3 = int(ls_1[i]), int(ls_2[i]), int(ls_3[i])
        rs.append(elem_1 * 100 + elem_2 * 10 + elem3)
    return rs
