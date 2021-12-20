# -*- coding: utf-8 -*-
"""
Minimal program (as an example) to simplify from a list contained in an input file *. in
Result of calculation in a file *. out for simplification of the direct form
and in a file *. Tool for simplification of the inverse form.
example :
ABCD
t1
0-0-
01--
-11-
1000
t0
1-01
001-

gives as a result

Termes essentiels
  1  0-0-  A'C'
Termes supplémentaires
  1  --00  C'D'
  2  01--  A'B
  3  1-1-  AC
  4  -1-0  BD'
  5  1--0  AD'
  6  -11-  BC
Synthèse
  1, 2, 3
  2, 3, 5
  1, 6
  5, 6


2 simplest solutions:
  A'C'+C'D'+BC
  A'C'+AD'+BC
"""

__author__ = 'Yvon Martin'
__version__ = "0.2"

from solvebool300 import input_tables_01, decode_bin, edit_solution, Simply

def lecture_fichier(nom_fichier):
    """
   Read file: output list in stack form
       reading with pop()
   """
    fichier_list = []
    try:
        with open(nom_fichier + ".in", 'r') as fichier_in:
            lignes = fichier_in.readlines()
            for ligne in lignes:
                if ligne.rstrip() != '':
                    fichier_list.append(ligne.rstrip())
            fichier_list.reverse()
    except:
        print("This file does not exist")
    return fichier_list

def my_suite(*args):
    result = ''
    for x in args:
        result += str(x)+ ' '
    return result


"""===============================MAIN==========================================="""

print("Simplification of a logical function")
print("=====================================")
nom = input("file name: ")
data_in = lecture_fichier(nom)  # contient le fichier des termes sous forme pile
print("-----------------")
dat = data_in[:]
print("Terms to be simplified")
while len(dat):
    print(dat.pop())
print("-----------------------")
if len(data_in) <= 1:
    print("---- Error: file name or empty file ----\n\n")
    quit()
nom_variable = data_in.pop()        # 1er data du fichier: nom des variables
nbr_variable = len(nom_variable)        # nombre de variables
list_normalise = input_tables_01(data_in, nbr_variable)  # listes normalisée: terme1, terme0, erreur

t1, t0, erreur = list_normalise
if erreur:
    print("---- Error in list of entries ----\n\n")
    quit()
extens = ".out1" #===================xxxx
rep = input("To have the reverse form type i")

print("------------------------------- ")


simply = Simply(nbr_variable, ['v'])
if rep != "i":
    t_essentiel, t_supplementaire, nu_synthese = simply(t1,t0)
    print("Direct form")
else:
    t_essentiel, t_supplementaire, nu_synthese = simply(t0,t1)
    extens = ".out1i"     #==================xxxx
    print("Inverse form")
#     print("table des termes essentiels")
#     print(t_essentiel)
#     print("table des termes supplémentaires")
#     print(t_supplementaire)
#     print("table de synthèse")
#     print(nu_synthese)
#     print()
with open(nom + extens, 'w') as fichier_out:
    print("Essential terms\n")
    fichier_out.write("Essential terms\n\n")
    tt_ess = [decode_bin(i, nbr_variable )for i in t_essentiel]
    sol_ess = [edit_solution(i, nom_variable )for i in tt_ess]
    for index, i in enumerate(tt_ess):
        ff = f"{index + 1:>3d}  {i}  {sol_ess[index]}"
        print(ff)
        fichier_out.write(ff + "\n")
    print("\nAdditional terms\n")
    tt_sup = [decode_bin(i, nbr_variable )for i in t_supplementaire]
    sol_sup = [edit_solution(i, nom_variable )for i in tt_sup]
    fichier_out.write("\nAdditional terms\n\n")
    tt_sup = [decode_bin(i, nbr_variable )for i in t_supplementaire]
    sol_sup = [edit_solution(i, nom_variable )for i in tt_sup]
    for index, i in enumerate(tt_sup):
        ff = f"{index + 1:>3d}  {i}  {sol_sup[index]}"
        print(ff)
        fichier_out.write(ff + "\n")
    print("----------------\nSummary of the additional terms\n")
    fichier_out.write("\nSummary of the additional terms\n\n")

    for i in nu_synthese:
            print(" ", my_suite(*i))
            fichier_out.write("  " + my_suite(*i) + "\n")

    print("----------------")
    fichier_out.write("\n")
