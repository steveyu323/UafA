from pymol import cmd, stored
import util_funcs as ut
import color_funcs as co

'''

The MutateByInput function takes in an array of residue number and do following:
1. color the mutated sites with certain color
'''
mutate_input, mutate_input_name, mutate_color = ut.GetReportedRegions()

aa_dict = {"CYS": "C", "ASP": "D", "SER": "S", "GLN": "Q", "LYS": "K",
  "ILE": "I", "PRO": "P", "THR": "T", "PHE": "F", "ASN": "N",
  "GLY": "G", "HIS": "H", "LEU": "L", "ARG": "R", "TRP": "W",
  "ALA": "A", "VAL":"V", "GLU": "E", "TYR": "Y", "MET": "M"}



def MutatedByInput(ind):
   '''
   Color the single Haplotype with the AA change and colored surface
   The other part depict a very translucent surface
   '''

# build the name and index for the potential functional sites
   cmd.reinitialize()
   cmd.fetch ("3IS1")
   cmd.hide(representation = "",selection = "all")
   cmd.show("cartoon", "all")
   #cmd.show("surface", "all")
   util.chainbow("3IS1")
   #cmd.hide(representation = "cartoon",selection = "all")
   cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")

   co.ColorByArray(mutate_input[ind],"red")

   filename = "../out/PotentialSites/" + mutate_input_name[ind] + ".pse"
   cmd.save(filename)
   cmd.extend( "MutatedByInput", MutatedByInput);

def ExportEach():
    #Create a Pymol session for each kind of sites
    for i in range(len(mutate_input)):
        MutatedByInput(i)


def ExportAll():
    #Mutate All the sites on one single map
    cmd.fetch ("3IS1")
    cmd.hide(representation = "",selection = "all")
    cmd.show("cartoon", "all")
    #cmd.show("surface", "all")
    util.chainbow("3IS1")
    #cmd.hide(representation = "cartoon",selection = "all")
    cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")

    for ls in mutate_input:
        col = mutate_color[mutate_input.index(ls)]
        co.ColorByArray(ls,col)

    filename = "../out/PotentialSites/" + "all" + ".pse"
    cmd.save(filename)
    cmd.extend( "ExportAll", ExportAll);




def ExportAllWithLabels():
    #Mutate All the sites on one single map
    cmd.fetch ("3IS1")
    cmd.hide(representation = "",selection = "all")
    cmd.show("cartoon", "all")
    #cmd.show("surface", "all")
    util.chainbow("3IS1")
    #cmd.hide(representation = "cartoon",selection = "all")
    cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")

    for ls in mutate_input:
        col = mutate_color[mutate_input.index(ls)]
        co.ColorByArray(ls,col)

    # Select One residue from each of the region to
    label_set = [693, 515, 475, 790, 495]
    for num in label_set:
        resi_num = "resi" + " " + str(num)
        cmd.label(selection = resi_num, expression = "resi")

    filename = "../out/PotentialSites/" + "all_with_label" + ".pse"
    cmd.save(filename)
    cmd.extend( "ExportAllWithLabels", ExportAllWithLabels);
