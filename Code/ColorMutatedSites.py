from pymol import cmd, stored
import util_funcs as ut

def ColorMutatedSites():
    '''
    @Goal: To color the mutated sites provided by "uafA Protein sequence variants (n=49 on 267 sequences)""
    @input nothing
    @output A PyMol model with the all the mutated sites colored red
    '''
    index_ls, pymol_index = ut.GetBothIndexes()

    cmd.fetch ("3IS1")
    cmd.hide(representation = "",selection = "all")
    cmd.show("cartoon", "all")
    util.chainbow("3IS1")
    cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")

    for index in pymol_index:
        i_resi = "resi" + " " + str(index)
        cmd.show(representation="surface", selection= i_resi )
        #cmd.show(representation="stick", selection= i_resi )
        cmd.color(color = "red", selection = i_resi)
    filename = "../out/ColorMutatedSites/" + "ColorMutatedSites" + ".pse"
    print(filename)
    cmd.save(filename)
    cmd.extend( "ColorMutatedSites", ColorMutatedSites);
