import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np

"""
Voici mon logiciel de dessin style packet tracer
J'ai recuperer une partie de code sur internet pour le menu bar et le canva (50 lignes environ) et j'ai fait tout le reste
J'y ai passer beaucoup de temps et je sais que je me suis beaucoup compliquer la vie mais je n'ai pas trouvé d'autre solution pour faire ce que je voulais
Je suis preneur de toute critique   
"""

# creation d’une fenêtre
fen1=Tk()
fen1.title('packHESS tracer')
compteur_routeur = StringVar()
compteur_routeur.set(0)

compteur_switch = StringVar()
compteur_switch.set(0)

compteur_client = StringVar()
compteur_client.set(0)

compteur_client_mobile = StringVar()
compteur_client_mobile.set(0)

def tabeffacer(): 
    tableau.delete(ALL)         # ça effacera tout ce qu'il y a dans le tableau  

# creation de la barre de menu
menuDraweasy = Menu(fen1) #
def info(): # affiche les coordonnées du clic gauche
    fenetre_prop = Toplevel()
    fenetre_prop.title("Mode D'emploi")
    fenetre_prop.geometry("600x100")
    fenetre_prop.resizable(width=False, height=False)
    # zone de texte
    zone_texte = Text(fenetre_prop, width=150, height=20)
    zone_texte.pack()
    zone_texte.insert(END, "Bienvenue dans le mode d'emploi de l'application PackHess Tracer\n")
    zone_texte.insert(END, "Le clic gauche sert a sélectionner et placer les items\n")
    zone_texte.insert(END, "La ligne est tracée entre le point de clic et celui de déclic.\n")
    zone_texte.insert(END, "La molette sert a déplacer les items et les namestags\n")
    zone_texte.insert(END, "Le clic droit sert a affciher les propriétés\n")
    fenetre_prop.configure(bg='white')

info()

################# creation des icones #################
def img_routeur():
    image = Image.open("routeur.png")
    image = image.resize((50, 50))
    image_routeur = ImageTk.PhotoImage(image)
    return image_routeur
image_routeur = img_routeur()

def img_line():
    image = Image.open("line.png")
    image = image.resize((50, 50))
    image_line = ImageTk.PhotoImage(image)
    return image_line
image_line = img_line()

def img_switch():
    image = Image.open("switch.jpg")
    image = image.resize((50, 50))
    image_switch = ImageTk.PhotoImage(image)
    return image_switch
image_switch = img_switch()

def image_cli_pc():
    image = Image.open("pc.png")
    image = image.resize((50, 50))
    image_client_pc = ImageTk.PhotoImage(image)
    return image_client_pc
image_client_pc = image_cli_pc()

def image_suppr():
    image = Image.open("1214428.png")
    image = image.resize((50, 50))
    image_supp = ImageTk.PhotoImage(image)
    return image_supp
image_supp = image_suppr()

def image_client_mobile():
    image = Image.open("mobile.png")
    image = image.resize((50, 50))
    image_mobile = ImageTk.PhotoImage(image)
    return image_mobile
image_mobile = image_client_mobile()
#######################################################             A partir d'ici c'est recuperer sur internet puis adapter a mon besoin          ############################################################
# Jy comprennais strictement rien et ca m'a pas mal aider sauf les boutons fait dans dans des boucles ca m'a pas mal compliquer la vie 
#####################################################################
#pris sur internet
# creation du menu fichier
fichier = Menu(menuDraweasy)
menuDraweasy.add_cascade(label="Fichier",menu=fichier)                 # on crée une barre de menu
fichier.add_command(label="Quitter", command=fen1.destroy)         # on ajoute une option au menu
# creation du menu effacer
effacer = Menu(menuDraweasy)
menuDraweasy.add_cascade(label="Effacer",menu=effacer)
effacer.add_command(label="Effacer tout", command=lambda : tabeffacer())        
# afficher le menu
fen1.config(menu=menuDraweasy)
# creation des differents cadres
Tableau=LabelFrame(fen1)
Tableau.configure(text='',bd=2,relief='flat')
Tableau.grid(row=0,rowspan=3,column=2,padx=0,pady=0)
Couleur=LabelFrame(fen1)
Couleur.configure(text='Couleur du trait',font='Courier 10',bd=2,relief='flat')
Couleur.grid(row=0,column=1,padx=0,pady=0,sticky=W)
Style=LabelFrame(fen1)
Style.configure(text='Style de forme',font='Courier 10',bd=2,relief='flat')
Style.grid(row=1,column=1,padx=0,pady=0,sticky=W)
Epaisseur=LabelFrame(fen1)
Epaisseur.configure(text='Epaisseur du trait',font='Courier 10',bd=2,relief='flat')
Epaisseur.grid(row=2,column=1,padx=0,pady=0,sticky=W)
# creation des boutons du cadre Tableau
tableau=Canvas(Tableau)
tableau.focus_set()
tableau.configure(width=800,height=700,bg='white')
tableau.grid()
#creation variable item selectionner
style=StringVar()
style.set(0) # 0 = routeur, 1 = switch, 2 = client, 3 = ligne, 4 = suppr
# adaptation du code trouvé sur internet
# j'ai eu la flemme de changer les variables au debut mais mtn elles sont partout ca va etre trop long de toutes les changer...
# creation des boutons de choix d'item
couleur=IntVar()
couleur.set(0)
palette=[image_routeur,image_switch,image_client_pc,image_mobile , image_line, image_supp]
objet=['routeur', 'switch', 'client pc','client mobile', 'ligne', 'gomme' ]
rcouleur={}
#######################################################
    # creation des boutons du cadre Epaisseur
epaisseur=IntVar()                 
epaisseur.set(1)
repaisseur={}
for e in range(1,5):
    repaisseur[e]=Radiobutton(Epaisseur)
    repaisseur[e].configure(variable=epaisseur,value=e,text=str(e),indicatoron=1)
    repaisseur[e].grid(sticky=N, padx=5)
#######################################################
#######################################################             A partir d'ici c'est de nouevau a moi              ############################################################
etatboutonsouris='haut'# etat du bouton gauche de la souris au début
#######################################################
def declic_suppr(event): # supprime l'item selectionner
    global etatboutonsouris,X2,Y2
    etatboutonsouris='haut'
    X2=event.x
    Y2=event.y
    item = tableau.find_closest(X2,Y2)
    tableau.delete(item)
    print("done")
#######################################################
    palette=[image_routeur,image_switch,image_client_pc,image_mobile , image_line, image_supp]
#######################################################
def choix_style_menubar(): # selon l'item selectionner, on bind la fonction associée
    if tableau.find_closest(X1, Y1) != (): # si on ne clique pas sur rien
        if tableau.find_closest(X1, Y1) == (rcouleur[0]):
            style.set(0)
            tableau.bind('<ButtonRelease-1>',declic)
        elif tableau.find_closest(X1, Y1) == (rcouleur[1]):
            style.set(1)
            tableau.bind('<ButtonRelease-1>',declic)
        elif tableau.find_closest(X1, Y1) == (rcouleur[2]):
            style.set(2)
            tableau.bind('<ButtonRelease-1>',declic)
        elif tableau.find_closest(X1, Y1) == (rcouleur[3]):
            style.set(3)
            tableau.bind('<ButtonRelease-1>',declic)
        elif tableau.find_closest(X1, Y1) == (rcouleur[4]):
            style.set(4)
            tableau.bind('<ButtonRelease-1>',declic)
        elif tableau.find_closest(X1, Y1) == (rcouleur[5]):
            style.set(5)
            print('its me')
            tableau.bind('<ButtonRelease-1>',declic_suppr)
    else: # si jamais on clique sur rien
        tableau.bind('<ButtonRelease-1>',declic)
        ligne_selected = ['true','first clic done']
#######################################################
#######################################################
def clic_en_fonction_de_style(): # si autre que suppr, lacher clic gauche = declic, sinon clic gauche = declic_suppr
    if str(style.get()) == '0':
        tableau.bind('<ButtonRelease-1>',declic)
    elif str(style.get()) == '1':
        tableau.bind('<ButtonRelease-1>',declic)
    elif str(style.get()) == '2':
        tableau.bind('<ButtonRelease-1>',declic)
    elif str(style.get()) == '3': 
        tableau.bind('<ButtonRelease-1>',declic)
    elif str(style.get() )== '4':  # si suppr
        tableau.bind('<ButtonRelease-1>',declic)
    elif str(style.get()) == '5':
        tableau.bind('<ButtonRelease-1>',declic_suppr)
    else: 
        print(f"erreur style.get() = {style.get()}")
#######################################################
#######################################################         # evenement associe au clic sur le tableau
def clic(event):                                                # creation d'un objet "event" lorsque l'on appuie sur le tableau
    global etatboutonsouris,X1,Y1, ligne_selected               # X1 et Y1 sont les attributs qui contiennent les coordonnées au moment du clic
    if str(style.get()) == "3":
        ligne_selected = 'true'
    etatboutonsouris='bas'      
    X1=event.x
    Y1=event.y
    choix_style_menubar()                                       # si jamais clic sur un item du menu
    clic_en_fonction_de_style()
#######################################################
#### creation des boutons de choix d'item
for c in range(0,6):
    rcouleur[c]=Radiobutton(Couleur)
    rcouleur[c].config(image=palette[c])
    rcouleur[c].configure(variable=style,value=str(c),padx=8,indicatoron=1, width=50, height=50, command=lambda : print(f"style.get : {style.get()} et item : {objet[int(style.get())]}"))
    rcouleur[c].grid(sticky=W, padx=5)
style.set(0) # valeur par defaut car sinon selectionne tout
# move image with mouse 
def clicM(event): #lors du clic sur la molette on recupere les coordonées
    global etatboutonsouris,XM,YM
    etatboutonsouris='bas'
    XM=event.x
    YM=event.y

def releaseM(event): # lors du relachement de la molette on recupere les coordonées
    global etatboutonsouris,XMR,YMR
    XMR=event.x
    YMR=event.y
    etatboutonsouris='haut'
    if etatboutonsouris =='haut': # ici on déplace l'objet au coordonées du relachement de la molette
        item = tableau.find_closest(XM,YM)
        tableau.move(item,XMR-XM,YMR-YM)
    
tableau.bind('<ButtonRelease-2>',releaseM) # on associe le relachement de la molette à la fonction releaseM
tableau.bind('<Button-2>', clicM) # on associe le clic de la molette à la fonction clicM

def declic(event):# evenements associe au declic sur le tableau
    global etatboutonsouris,X2,Y2
    etatboutonsouris='haut'
    X2=event.x
    Y2=event.y
    # declic basique si un choix a etait fait dans le menu
    if (style.get()=="0"): # si a choisi routeur
        icon = tableau.create_image(X1,Y1,anchor=NW,image=image_routeur, tags=('routeur'+str(compteur_routeur.get())))
        tableau.create_text(X1+24,Y1+60, text=tableau.gettags(icon), tags='texte')
        c = int(compteur_routeur.get()); c = c+1; compteur_routeur.set(c)
    elif (style.get()=="1"): # si a choisi switch
        icon1 = tableau.create_image(X1,Y1,anchor=NW,image=image_switch, tags=('switch'+str(compteur_switch.get())))
        tableau.create_text(X1+20,Y1+20, text=tableau.gettags(icon1), tags='texte')
        c = int(compteur_switch.get()); c = c+1; compteur_switch.set(c)
    elif (style.get()=="2"): # si a choisi pc
        icon2 = tableau.create_image(X1,Y1,anchor=NW,image=image_client_pc, tags=('client'+str(compteur_client.get())))
        tableau.create_text(X1+20,Y1+20, text=tableau.gettags(icon2), tags='texte')
        c = int(compteur_client.get()); c = c+1; compteur_client.set(c)
    elif (style.get()=="3"): # si a choisi mobile
        icon3 = tableau.create_image(X1,Y1,anchor=NW,image=image_mobile, tags=('mobile'+str(compteur_client_mobile.get())))
        tableau.create_text(X1+20,Y1+20, text=tableau.gettags(icon3), tags='texte')
        c = int(compteur_client_mobile.get()); c = c+1; compteur_client_mobile.set(c)
    elif (style.get() == "4"): # si a choisi ligne
        tableau.create_line(X1,Y1,X2,Y2,fill='black',width=epaisseur.get(), tags=('ligne'))
tableau.bind('<Button-1>',clic) # clic gauche = clic

################## partie modification et infos ############################
'''
def test():
    items_nom.append(str(string_nom.get()))
    items_ip.append(str(string_ip.get()))
    items_mac.append(str(string_mac.get()))
    items_mdp.append(str(string_mdp.get()))
     
    print(f"nom : {items_nom} ip : {items_ip} mac : {items_mac} mdp : {items_mdp}")
'''

global items_nom
items_nom = {}
#
global string_nom
string_nom = StringVar()

global items_ip
items_ip = {}
#
global string_ip
string_ip = StringVar()
# 
global items_mac
items_mac = {}
#
global string_mac
string_mac = StringVar()
#
global items_mdp
items_mdp = {}
#
global string_mdp
string_mdp = StringVar()

def adding_to_dict():
    item = tableau.find_closest(localX, localY)
    name = tableau.gettags(item)[0] + str(item)[1:2]
    items_nom[name] = str(name)
    items_nom[name] = str(string_ip.get())
    items_nom[name] = str(string_mac.get())
    items_nom[name] = str(string_mdp.get())
    print(f"dico : items_nom : {items_nom}")
    print(f"nom : {items_nom} ip : {items_ip} mac : {items_mac} mdp : {items_mdp}")
  
def window_propriété(event):
# fenetre de propriété
    fenetre_prop = Toplevel()
    fenetre_prop.title("Propriétés propriétés")
    fenetre_prop.geometry("400x400")
    fenetre_prop.resizable(width=False, height=False)
    fenetre_prop.configure(bg='white')
# formulaire texte
    # champs entree texte
    item = tableau.find_closest(event.x, event.y)
    name = tableau.gettags(item)[0] + str(item)[1:2]
    #for i in range(tableau.find_all())
    label_nom = Label(fenetre_prop, text='nom').pack()
    entry_nom = Entry(fenetre_prop, textvariable=string_nom).pack()
    # champs entree texte
    label_ip = Label(fenetre_prop, text='ip').pack()
    entry_ip = Entry(fenetre_prop, textvariable=string_ip).pack()
    # champs entree texte
    label_mac = Label(fenetre_prop, text='mac').pack()
    entry_mac = Entry(fenetre_prop, textvariable=string_mac).pack()
    # champs entree texte
    label_mdp = Label(fenetre_prop, text='mdp').pack()
    entry_mdp = Entry(fenetre_prop, textvariable=string_mdp).pack()
    # Bouton valider
    bouton_valider = Button(fenetre_prop, text='Valider', command=adding_to_dict).pack()
    fenetre_prop.mainloop()
    return fenetre_prop

def proprietes(event):
    global localX
    localX = event.x
    global localY
    localY = event.y
    ### create a new small window when clicking on the image
    if tableau.find_closest(event.x, event.y, halo=1) != ():
        item = tableau.find_closest(event.x, event.y)
        name = tableau.gettags(item)[0] + str(item)[1:2]
        print(name)
        print('item = ', item)
        fenetre_prop = window_propriété(event)
        tableau.bind('<Button-1>',window_propriété)
    #fenetre_prop.grab_set()
        fenetre_prop.focus_set()
        fenetre_prop.wait_window()
        fenetre_prop.mainloop()
tableau.bind('<Button-3>',proprietes) # clic droit = proprietes
# attente des evenements
fen1.mainloop()             # démarre l'observateur d'évènements




