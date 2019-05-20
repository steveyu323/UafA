from pymol import cmd, stored
import util_funcs as ut
import color_funcs as co
import MutatedHap as mutehap
'''
@author Changhua YU
@DATE 180531
'''

mutate_input, mutate_input_name, mutate_color = ut.GetReportedRegions()
#Override the orginal mutate color scheme
#mutate_color = ["yelloworange","limon","wheat","sand", "greencyan"]
mutate_input_all = []
for ls in mutate_input:
    mutate_input_all += ls



def ColorSuperimpose(arr_1, arr_2):
    '''
    @input two arrays of mutated sites that are already within the range of PyMol display
    @output a pymol session with Superimposion
    '''
    # Get the splitted arrays with 3 parts splited: arr_1 only, arr_2 only, overlapped
    arr_1_only, arr_2_only, intersect = ut.OrganizeSet(arr_1, arr_2)
    # Color the three different array with different color
    co.ColorByArray(arr_1_only,"blue")
    co.ColorByArray(arr_2_only,"green")
    co.ColorByArray(intersect,"red")


def ColorBindingWithHapAll():
    '''
    1. color each of the potential functioning region as in MutatedByInput
    2. find the overlapping region of mutate_input_all and pymol_index
    3. color the intersect and pymol_only
    '''
    #Initialization: show chainbow transparent surface
    cmd.reinitialize()
    cmd.fetch ("3IS1")
    cmd.hide(representation = "",selection = "all")
    cmd.show("cartoon", "all")
    #cmd.show("surface", "all")
    util.chainbow("3IS1")
    cmd.hide(representation = "cartoon",selection = "all")
    #cmd.color(color = "white", selection = "all")
    cmd.set(name = "cartoon_transparency", value = "0.8", selection = "all")

    #Step 1: color each of the potential functioning region as in MutatedByInput
    for ls in mutate_input:
        col = mutate_color[mutate_input.index(ls)]
        co.ColorByArray(ls,col)

    #Step 2: find the overlapping region of mutate_input_all and pymol_index
    index_ls, pymol_index = ut.GetBothIndexes()
    # print(mutate_input_all)
    # print(pymol_index)
    arr_1_only, arr_2_only, intersect = ut.OrganizeSet(mutate_input_all, pymol_index)
    # print(arr_1_only)
    # print(arr_2_only)
    # print(intersect)

    #Step 3: color the intersect and pymol_only
    co.ColorByArray(intersect, "red")
    co.ColorByArray(arr_2_only, "blue")

    filename = "../out/Superimpose/" + "all" + ".pse"
    cmd.save(filename)
    cmd.extend( "ColorBindingWithHapAll", ColorBindingWithHapAll);

def SuperimposeEachRegion():
    '''
    Export 5 pymol sessions with the overall mutated sites overlap with each of the functional regions,
    with the GetMutatedSites only as blue, functional region only as green and overlapping region as red
    '''
    index_ls, pymol_index = ut.GetBothIndexes()
    for ls in mutate_input:
        #Initialization: show chainbow transparent surface
        cmd.reinitialize()
        cmd.fetch ("3IS1")
        cmd.hide(representation = "",selection = "all")
        cmd.show("cartoon", "all")
        #cmd.show("surface", "all")
        util.chainbow("3IS1")
        cmd.hide(representation = "cartoon",selection = "all")
        #cmd.color(color = "white", selection = "all")
        cmd.set(name = "cartoon_transparency", value = "0.8", selection = "all")

        ColorSuperimpose(pymol_index, ls)
        name = mutate_input_name[mutate_input.index(ls)]
        filename = "../out/Superimpose/" + "super_with" + name + ".pse"
        cmd.save(filename)
        cmd.extend( "SuperimposeEachRegion", SuperimposeEachRegion);

def SuperimposeEachHapEachRegion():
    # To get the dict_index
    dict_index, lines_used, pymol_index, index_ls = ut.GetDictIndex()
    mutate_input, mutate_input_name, mutate_color = ut.GetReportedRegions()
    # For each of the dict_index (hap_ids)
    for hap_id in dict_index:
        dict_hap_site = ut.getSingleHapMutateSites(hap_id)
        # Get the mutated sit for a single hap_id
        dict_mute_site = []
        for i in range(len(pymol_index)):
            if dict_hap_site[i] != '.' and dict_hap_site[i] != '-':
                dict_mute_site.append(pymol_index[i])
        # Double For Loop Start!
        for ls in mutate_input:
            #Initialization: show chainbow transparent surface
            cmd.reinitialize()
            cmd.fetch ("3IS1")
            cmd.hide(representation = "",selection = "all")
            cmd.show("cartoon", "all")
            #cmd.show("surface", "all")
            util.chainbow("3IS1")
            cmd.hide(representation = "cartoon",selection = "all")
            #cmd.color(color = "white", selection = "all")
            cmd.set(name = "cartoon_transparency", value = "0.8", selection = "all")

            ColorSuperimpose(dict_mute_site, ls)
            name = mutate_input_name[mutate_input.index(ls)]
            filename = "../out/SuperimposeEachHapEachRegion/" + "hap" + str(hap_id) + "super_with" + name + ".pse"
            cmd.save(filename)
            cmd.extend( "SuperimposeEachRegion", SuperimposeEachRegion);
