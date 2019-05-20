from pymol import cmd, stored
import util_funcs as ut

aa_dict = {"CYS": "C", "ASP": "D", "SER": "S", "GLN": "Q", "LYS": "K",
  "ILE": "I", "PRO": "P", "THR": "T", "PHE": "F", "ASN": "N",
  "GLY": "G", "HIS": "H", "LEU": "L", "ARG": "R", "TRP": "W",
  "ALA": "A", "VAL":"V", "GLU": "E", "TYR": "Y", "MET": "M"}

def ColorSingleHapMutateSites(hap_index):
   '''
   Color the single Haplotype with the AA change and colored surface
   The other part depict a very translucent surface
   '''
   index_ls, pymol_index = ut.GetBothIndexes()
   dict_hap_site = ut.getSingleHapMutateSites(hap_index)
   cmd.reinitialize()
   cmd.fetch ("3IS1")
   cmd.hide(representation = "",selection = "all")
   cmd.show("surface", "all")
   util.chainbow("3IS1")
   cmd.hide(representation = "cartoon",selection = "all")
   cmd.set(name = "transparency", value = "0.6", selection = "all")

   for i in range(len(pymol_index)):
       if dict_hap_site[i] != '.' and dict_hap_site[i] != '-':
           i_resi = "resi" + " " + str(pymol_index[i])
           i_aa = (list(aa_dict.keys())[list(aa_dict.values()).index(dict_hap_site[i])])
           #DO
           cmd.wizard("mutagenesis")
           cmd.do("refresh_wizard")
           # lets mutate
           cmd.get_wizard().set_mode(i_aa)
           cmd.get_wizard().do_select(i_resi)
           # Select the first rotamer, which is most probable
           cmd.frame(1)
           # Apply the mutation
           cmd.get_wizard().apply()
           # Close wizard
           cmd.wizard(None)
           cmd.show(representation="sphere", selection= i_resi)
           cmd.color(color = "red", selection = i_resi)
   filename = "../out/MutatedHap/" + str(hap_index) + ".pse"
   print(filename)
   cmd.save(filename)
   cmd.extend( "ColorSingleHapMutateSites", ColorSingleHapMutateSites );



def ColorAllHapMutateSites():
    index_ls, pymol_index = ut.GetBothIndexes()
    dict_index, lines_used, pymol_index, index_ls = ut.GetDictIndex()
    for elem in dict_index:
        ColorSingleHapMutateSites(elem)
