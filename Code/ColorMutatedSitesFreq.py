from pymol import cmd, stored
import util_funcs as ut

def ColorMutatedSitesFreq():
   '''
   To color the mutated sites provided by
   "uafA Protein sequence variants (n=49 on 267 sequences)""
   @output A PyMol model with the mutated sites colored, with a spectrum by site frequency
   The more frequent, the more red; the less frequent, the more green
   '''
   index_ls, pymol_index = ut.GetBothIndexes()
   freq_table = ut.FindFreq()

   cmd.fetch ("3IS1")
   cmd.hide(representation = "",selection = "all")
   cmd.show("cartoon", "all")
   util.chainbow("3IS1")
   cmd.set(name = "cartoon_transparency", value = "0.6", selection = "all")


   for i in range(len(pymol_index)):
       i_resi = "resi" + " " + str(pymol_index[i])
       i_color = freq_table[i]
       if (i_color > 1.00) :
           #ceiling the color as some mutations are too frequent
           i_color = 1.00
       color_array = [i_color, 1.00 - i_color, 0.00]
       cmd.set_color(name = "current" + str(i), rgb = color_array)
       cmd.show(representation="surface", selection= i_resi )
       # cmd.show(representation="stick", selection= i_resi )
       cmd.color(color = "current" + str(i), selection = i_resi)

   filename = "../out/ColorMutatedSitesFreq/" + "ColorMutatedSitesFreq" + ".pse"
   cmd.save(filename)
   cmd.extend( "ColorMutatedSitesFreq", ColorMutatedSitesFreq );
