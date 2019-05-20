import util_funcs as ut

'''
@author Changhua Yu
@date 180605
@Goal: This module will do the following command:
    for each of the haplotype:
        1. Parse in the line and hap_id
        2. OrganizeSet with each of the annotated regions
        3. Note down the intersections
        4. Create a dictionary with following fields:
           hap_id|line|MutatedSites|FuncRegionsOverlap1|2|3|4|5

'''
def MapHapToRegion():
    lines_used = ut.GetTxtBody()
    mutate_input, mutate_input_name, mutate_color = ut.GetReportedRegions()
    # Create a dictionary with hap_id (i.e 72)as key and the list of alignment (i.e ['a', 'd','a'])
    dict_id_line = {}
    for ls in lines_used:
        key = ut.GetIndexList(ls)
        value = ut.GetAlignList(ls)
        dict_id_line[key] = value

    # Create a dictionary with hap_id (i.e 72)as key and the muatedSites (i.e ['a', 'd','a'])
    dict_id_mutesites = {}
    for ls in lines_used:
        key = ut.GetIndexList(ls)
        value = ut.GetHapMutatedIndex(key)
        dict_id_mutesites[key] = value


    # Create a dictionary with hap_id as key and the value : a list of 5 elems: list of overlapping indexes
    dict_id_overlap = {}
    for key in dict_id_mutesites.keys():
        value = [None] * 5
        hap_mutated_index = dict_id_mutesites[key]
        for i in range(len(value)):
            hap_only, func_only, intersect = ut.OrganizeSet(hap_mutated_index, mutate_input[i])
            value[i] = intersect
        dict_id_overlap[key] = value


    return dict_id_line, dict_id_mutesites, dict_id_overlap
