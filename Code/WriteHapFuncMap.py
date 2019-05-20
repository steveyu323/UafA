import sqlite3;
import MapHapToRegion as map
import util_funcs as ut

def main():
    '''
    Build the sqlite table hap_func_match
    '''
    dict_id_line, dict_id_mutesites, dict_id_overlap = map.MapHapToRegion()

    db_file = "../db/uafa.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd = ''' INSERT INTO hap_func_match VALUES(?,?,?,?,?,?,?,?)'''
    for key in dict_id_line.keys():
        hap_id = key
        line = ut.CatListToString(dict_id_line[key])
        mutesites = ut.CatListToString(dict_id_mutesites[key])
        ov_1 = ut.CatListToString(dict_id_overlap[key][0])
        ov_2 = ut.CatListToString(dict_id_overlap[key][1])
        ov_3 = ut.CatListToString(dict_id_overlap[key][2])
        ov_4 = ut.CatListToString(dict_id_overlap[key][3])
        ov_5 = ut.CatListToString(dict_id_overlap[key][4])
        temp_values = (hap_id, line, mutesites, ov_1,ov_2,ov_3,ov_4,ov_5)
        cur.execute(cmd,temp_values)
    conn.commit()
    return None
