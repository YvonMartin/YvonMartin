# -*- coding: utf-8 -*-

"""
Version pour utiliser le format standard
Minimal program (as an example) to simplify from a list contained in an input file *. txt
Result of calculation in a file *. out for simplification of the direct form
and in a file *. Tool for simplifification of the inverse form.
example :

.i 4
.o 1
0-0- 1
01-- 1
-11- 1
1000 1
1-01 0
001- 0
.e

gives as a result

Termes essentiels
  1  0-0-
Termes supplémentaires
  1  --00
  2  01--
  3  1-1-
  4  -1-0
  5  1--0
  6  -11-
Synthèse
  1, 2, 3
  2, 3, 5
  1, 6
  5, 6


2 solutions:
with input variables ABCD:

  A'C'+C'D'+BC
  A'C'+AD'+BC
"""

__author__ = 'Yvon Martin'
__version__ = "0.5"

from solvebool502 import acqui_terme, decode_bin, edit_solution, Simply
import time
TYPE_FILE = '.txt'

def lecture_fichier(nom_fichier):
    """
   Read file: output list in stack form
       reading with pop()
   """
    error = False
    fichier_list = []
    try:
        with open('bench/'+ nom_fichier + TYPE_FILE, 'r') as fichier_in:
            lignes = fichier_in.readlines()
            for ligne in lignes:
                if ligne.rstrip() != '':
                    fichier_list.append(ligne.rstrip())
            fichier_list.reverse()
    except:
        error = True
    return fichier_list, error

def my_suite(*args):
    result = ''
    for x in args:
        result += str(x)+ ' '
    return result

def input_tables_01(data_in, num_out):
    """
    Decode the stack (alphabetical list of 3 characters '1-0') data_in to form
    the standardized list(s) of terms 1 and 0. Each element is a
    tuple (term, mask). the hidden bits of the term are normalized to 0
    """
    terme_0 = set()
    terme_1 = set()
    erreur = False
    nbr_variable = 0
    out_max = 1            # nbr de sorties

    #type_terme = 1
    while len(data_in) != 0:

        rep = data_in.pop()

        rep= rep.strip().split()
        if rep[0] == ".e":
            pass

        elif rep[0] == ".i":
            nbr_variable = int(rep[1])
        elif rep[0] == ".o":
            out_max = int(rep[1])
        elif nbr_variable == 0:
            terme_0 = set()
            terme_1 = set()
            erreur = True
            break
        else:
            terme, erreur = acqui_terme(rep[0], nbr_variable)
            if num_out > out_max:
                num_out = 1
                print("Incorrect output, default = 1")
            if erreur:
                terme_0 = set()
                terme_1 = set()
                break

            if rep[1][num_out - 1] == '1':
                terme_1.add(terme)
            elif rep[1][num_out - 1] == '0':
                terme_0.add(terme)


    return (nbr_variable, list(terme_1), list(terme_0),  erreur)  # liste normalisée

"""=============================================================================="""
def test():
    sortir = input('further simplification (y): ')
    if sortir != ('y' or 'Y'):
        FINISH = True
        exit()
"""===============================MAIN==========================================="""
FINISH = False
while not(FINISH):
    ERROR = 0
    while not(ERROR):
        print("Simplification of a logical function")
        print("=====================================")
        nom = input("file name: ")
        data_in, err = lecture_fichier(nom)  # contient le fichier des termes sous forme pile
        if err:
            ERROR = 1
            break
        print("-------------------------------------")

        dat = data_in[:]
        if len(data_in) == 0:
            ERROR = 2
            break
        print("Terms to be simplified \n")
        while len(dat):
            print(dat.pop())
        print("---------------------------------------------")

        num = input("output Numero ")
        if num.isnumeric():
            num_out = abs(int(num))
        else:
            print("Incorrect output, default = 1")
            num_out = 1



        # nom_variable = data_in.pop()        # 1er data du fichier: nom des variables
        # nbr_variable = len(nom_variable)        # nombre de variables
        nbr_variable, t1, t0,  erreur = input_tables_01(data_in, num_out)  # listes normalisée: nbr de variable, terme1, terme0, erreur

        if erreur:
            ERROR = 3
            break

        extens = ".out1" #===================xxxx

        rep = input("To have the reverse form type i: ")
        ver = input("To verbatim type v: ")
        if ver == 'v':
            verb = True
        else:
            verb = False

        post = input("to make post synthese type p: ")
        if post == 'p':
            post = True
            pst = 'on'
        else:
            post = False
            pst = 'off'

        accel = input("Accelerate type nombre: ")
        if accel.isnumeric():
            acc = abs(int(accel))
        else:
            print("Incorrect nombre, default = 0")
            acc = 0

        print("------------------------------- ")

        start = time.time()

        posi = 0

        simply = Simply(nbr_variable, a = acc, v = verb, p = post)

        if rep != "i":
            t_essentiel, t_supplementaire, nu_synthese,error = simply(t1,t0)
            if error:
                ERROR = 4
                break

            print("Direct form")
        else:
            t_essentiel, t_supplementaire, nu_synthese,error = simply(t0,t1)

            if error:
                ERROR = 4
                break
            extens = ".out1i"     #==================xxxx
            print("Inverse form")

        with open('bench-out/' + nom + extens, 'w') as fichier_out:
            print("Essential terms\n")

            fichier_out.write( nom + TYPE_FILE + '  -')
            if rep == 'i':
                fichier_out.write('Inverse form-\n\n')
            else:
                fichier_out.write('Direct forme-\n\n')

            fichier_out.write( 'Output numero: ' + str(num_out) + '\n')
            fichier_out.write( 'Post synchro: ' + pst + '\n')
            fichier_out.write( 'Accelerate: ' + str(acc) +'\n\n')

            fichier_out.write("Essential terms\n\n")

            tt_ess = [decode_bin(i, nbr_variable )for i in t_essentiel]

        #    sol_ess = [edit_solution(i, nom_variable )for i in tt_ess]
            for index, i in enumerate(tt_ess):
                ff = f"{index + 1:>3d} {i} "
                print(ff)
                fichier_out.write(i + "\n")

            print("\nAdditional terms\n")

            tt_sup = [decode_bin(i, nbr_variable )for i in t_supplementaire]
        #    sol_sup = [edit_solution(i, nom_variable )for i in tt_sup]


            fichier_out.write("\nAdditional terms\n\n")
            tt_sup = [decode_bin(i, nbr_variable )for i in t_supplementaire]

        #    sol_sup = [edit_solution(i, nom_variable )for i in tt_sup]
            for index, i in enumerate(tt_sup):
                ff = f"{index + 1:>3d} {i}"
                print(ff)
                fichier_out.write(ff + "\n")

            print("----------------\nSummary of the additional terms\n")
            fichier_out.write("\nSummary of the additional terms\n\n")

            for i in nu_synthese:
                    print(" ", my_suite(*i))
                    fichier_out.write("  " + my_suite(*i) + "\n")
            end = time.time()
            print("----------------")
            tp ='time to execute ' +str(int((end-start)*1000)) +' ms'
            print(tp)

            fichier_out.write("\n" + tp + "\n")
            fichier_out.close()


        if ERROR == 0:
            test()

    if ERROR == 1:
        print("---- Error: file name \n")
        test()
    elif ERROR == 2:
        print("---- Error: empty file \n")
        test()
    elif ERROR == 3:
        print("---- Error in list of entries ----\n")
        test()
    elif ERROR == 4:
        print("---- Error: terms 0 cover terms 1 ----\n\n")




