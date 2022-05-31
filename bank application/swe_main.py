#importering av biblotek
from tkinter import *
import os
from PIL import ImageTk, Image

#Skapar filk med titelen bank...
GUI = Tk()
GUI.title('Bank Applikation')

#Funktion som tittar ifall kontot finns
def finish_reg():
    #temporärt lägger variblerna
    namn = temp_namn.get()
    ålder = temp_ålder.get()
    kön = temp_kön.get()
    lösenord = temp_lösenord.get()
    #tittar igenom mapp
    alla_konton = os.listdir()

    #tittar ifall variblerna innehåller något
    if namn == "" or ålder == "" or kön == "" or lösenord == "":
        #ifall de inte gör det så skrivs nedan ut i röd färg
        notifikation.config(fg="purple",text="Alla fält krävs * ")
        return

    #tittar igenom namn som finns i namn
    for namn_check in alla_konton:
        #ifall namnet finns redan i mappen så skriv nedan ut i rött och returnar värde
        if namn == namn_check:
            notifikation.config(fg="purple",text="Kontot finns redan")
            return
        else:
            #annars gör den en ny fil med namnet man skrev in
            ny_fil = open(namn,"w")
            #skriver ut varje varibel med ny rad
            ny_fil.write(namn+'\n')
            ny_fil.write(lösenord+'\n')
            ny_fil.write(ålder+'\n')
            ny_fil.write(kön+'\n')
            #sätter beloppet till 0 den kan användas för framtida belopp ändringar
            ny_fil.write('0')
            #stänger filen
            ny_fil.close()
            #skickar en "notification" ut att kontot har skapats i grön färg
            notifikation.config(fg="blue", text="Kontot har skapats")

def registera():
    #sätter vaiblerna gobalt så de kan användas utanför funktionen
    global temp_namn
    global temp_ålder
    global temp_kön
    global temp_lösenord
    global notifikation
    temp_namn = StringVar()
    temp_ålder = StringVar()
    temp_kön = StringVar()
    temp_lösenord = StringVar()
    
    #Skapar nytt fönster med titel registera
    registerings_skärm = Toplevel(GUI)
    registerings_skärm.title('Registrera')

    #Label för varje numrerad row, har ingen specifik font, textstorlekt = 12
    #Pady 10, sätter mellanrum mellan knapparna och kanterna på fönstret
    Label(registerings_skärm, text="Ange dina uppgifter nedan för att registrera dig", font=('deafult',12)).grid(row=0,sticky=N,pady=10)
    #lägger texten på rad 1
    #sticky = W, bestämmer hur mycket extra utrymme inom cellen som inte är upptagen av en widget (W= west, left center)
    Label(registerings_skärm, text="Namn", font=('deafult',12)).grid(row=1,sticky=W)
    Label(registerings_skärm, text="Ålder", font=('deafult',12)).grid(row=2,sticky=W)
    Label(registerings_skärm, text="Kön", font=('deafult',12)).grid(row=3,sticky=W)
    Label(registerings_skärm, text="Lösenord", font=('deafult',12)).grid(row=4,sticky=W)
    notifikation = Label(registerings_skärm, font=('deafult',12))
    notifikation.grid(row=6,sticky=N,pady=10)

    #Entry skapar en ruta där man kan fylla i sitt svar
    #Lägger entry på samma row som label
    Entry(registerings_skärm,textvariable=temp_namn).grid(row=1,column=0)
    Entry(registerings_skärm,textvariable=temp_ålder).grid(row=2,column=0)
    Entry(registerings_skärm,textvariable=temp_kön).grid(row=3,column=0)
    Entry(registerings_skärm,textvariable=temp_lösenord,show="*").grid(row=4,column=0)

    #Knapp för att registera klart och kör kommandot(funktionen) finish_reg
    Button(registerings_skärm, text="Registrera", command = finish_reg, font=('deafult',12)).grid(row=5,sticky=N,pady=10)


def login_session():
    #global variabel
    global login_namn
    #använder os för att titta igenom dir(mapp)
    alla_konton = os.listdir()
    #lägger temporär "data" på variblerna via ifyllnings fält
    login_namn = temp_login_name.get()
    login_lösenord = temp_login_password.get()

    #letar igenom namn inom alla konton ifall det matchar
    for namn in alla_konton:
        if namn == login_namn:
            #öppnar filen med r
            fil = open(namn,"r")
            #läser filen
            fil_data = fil.read()
            #splitar den med "enter"
            fil_data = fil_data.split('\n')
            #lösenord är andra raden
            lösenord  = fil_data[1]
            if login_lösenord == lösenord:
                #stänger ner login skärmen med destroy()
                login_skärm.destroy()
                konto_översikt = Toplevel(GUI)
                konto_översikt.title('Översikt')
                Label(konto_översikt, text="Konto Översikt", font=('deafult',12)).grid(row=0,sticky=N,pady=10)
                Label(konto_översikt, text="Välkommen "+namn, font=('deafult',12)).grid(row=1,sticky=N,pady=5)
                Button(konto_översikt, text="Kontouppgifter",font=('deafult',12),width=30,command=personlig_detalj).grid(row=2,sticky=N,padx=10)
                Button(konto_översikt, text="Insättning",font=('deafult',12),width=30,command=instättning).grid(row=3,sticky=N,padx=10)
                Button(konto_översikt, text="Dra tillbaka",font=('deafult',12),width=30,command=ta_ut).grid(row=4,sticky=N,padx=10)
                Label(konto_översikt).grid(row=5,sticky=N,pady=10)
                return
            else:
                #skickar notikation i röd text
                login_notifikation.config(fg="purple", text="Inkorrekt lösenord!")
                return
    #ifall inget hittas så skrivs nedan ut i rött            
    login_notifikation.config(fg="purple", text="Inget konto hittades!")

def instättning():
    #globala variabler
    global belopp
    global insättning_notifikation
    global nuvarande_belopp_label
    belopp = StringVar()
    fil   = open(login_namn, "r")
    fil_data = fil.read()
    användar_detaljer = fil_data.split('\n')
    detaljer_saldo = användar_detaljer[4]
    insättning_skärm = Toplevel(GUI)
    insättning_skärm.title('Insättning')
    Label(insättning_skärm, text="Insättning", font=('deafult',12)).grid(row=0,sticky=N,pady=10)
    nuvarande_belopp_label = Label(insättning_skärm, text="Aktuellt saldo : Kr "+detaljer_saldo, font=('deafult',12))
    nuvarande_belopp_label.grid(row=1,sticky=W)
    Label(insättning_skärm, text="Belopp : ", font=('deafult',12)).grid(row=2,sticky=W)
    insättning_notifikation = Label(insättning_skärm,font=('deafult',12))
    insättning_notifikation.grid(row=4, sticky=N,pady=5)
    Entry(insättning_skärm, textvariable=belopp).grid(row=2,column=1)
    Button(insättning_skärm,text="Sätt in",font=('deafult',12),command=uppd_instättning).grid(row=3,sticky=W,pady=5)

def uppd_instättning():
    #ifall fältet är tomt skrivs ut text med röd färg och retunerar
    if belopp.get() == "":
        insättning_notifikation.config(text='Belopp krävs!',fg="purple")
        return
        #ifall beloppet är mindre än noll så funkar det ej
    if float(belopp.get()) <=0:
        insättning_notifikation.config(text='Negativ valuta accepteras inte', fg='purple')
        return
    #öppnar fil med login namn och läser med r+
    fil = open(login_namn, 'r+')
    fil_data = fil.read()
    detaljer = fil_data.split('\n')
    nuvarande_belopp = detaljer[4]
    upp_saldo = nuvarande_belopp
    #sätter strängen till en float och plusar med nummret som skrevs in i fältet
    upp_saldo = float(upp_saldo) + float(belopp.get())
    #ändrar i filen med en ny sträng dvs det nya beloppet
    fil_data = fil_data.replace(nuvarande_belopp, str(upp_saldo))
    #går längst upp i filen
    fil.seek(0)
    fil.truncate(0)
    fil.write(fil_data)
    #stänger filen
    fil.close()
    #uppdaterar texten på skärmen i grön färg
    nuvarande_belopp_label.config(text="Aktuellt saldo : Kr "+str(upp_saldo),fg="blue")
    insättning_notifikation.config(text='Saldot uppdaterat', fg='blue')

#samma princip som insättning 
def ta_ut():
    global ta_ut_belopp
    global ta_ut_notifikation
    global nuvarande_belopp_label
    ta_ut_belopp = StringVar()
    fil = open(login_namn, "r")
    fil_data = fil.read()
    användar_detaljer = fil_data.split('\n')
    detaljer_saldo = användar_detaljer[4]
    ta_ut_skärm = Toplevel(GUI)
    ta_ut_skärm.title('Ta ut')
    Label(ta_ut_skärm, text="Deposition", font=('deafult',12)).grid(row=0,sticky=N,pady=10)
    nuvarande_belopp_label = Label(ta_ut_skärm, text="Aktuellt saldo : Kr "+detaljer_saldo, font=('deafult',12))
    nuvarande_belopp_label.grid(row=1,sticky=W)
    Label(ta_ut_skärm, text="Belopp : ", font=('deafult',12)).grid(row=2,sticky=W)
    ta_ut_notifikation = Label(ta_ut_skärm,font=('deafult',12))
    ta_ut_notifikation.grid(row=4, sticky=N,pady=5)
    Entry(ta_ut_skärm, textvariable=ta_ut_belopp).grid(row=2,column=1)
    Button(ta_ut_skärm,text="Sätt in",font=('deafult',12),command=uppd_ta_ut).grid(row=3,sticky=W,pady=5)

def uppd_ta_ut():
    if ta_ut_belopp.get() == "":
        ta_ut_notifikation.config(text='Belopp krävs!',fg="purple")
        return
    if float(ta_ut_belopp.get()) <=0:
        ta_ut_notifikation.config(text='Negativ valuta accepteras inte', fg='purple')
        return

    fil = open(login_namn, 'r+')
    fil_data = fil.read()
    detaljer = fil_data.split('\n')
    nuvarande_belopp = detaljer[4]

    if float(ta_ut_belopp.get()) >float(nuvarande_belopp):
        ta_ut_notifikation.config(text='Otillräckliga medel', fg='purple')
        return

    upp_saldo = nuvarande_belopp
    upp_saldo = float(upp_saldo) - float(ta_ut_belopp.get())
    fil_data = fil_data.replace(nuvarande_belopp, str(upp_saldo))
    fil.seek(0)
    fil.truncate(0)
    fil.write(fil_data)
    fil.close()

    nuvarande_belopp_label.config(text="Aktuellt saldo : Kr "+str(upp_saldo),fg="blue")
    ta_ut_notifikation.config(text='Saldot uppdaterat', fg='blue')
    

def personlig_detalj():
    fil = open(login_namn, 'r')
    fil_data = fil.read()
    användar_detaljer = fil_data.split('\n')
    #väljer ut spefika rader genom att skriva talet inom hakparanteser
    detalj_namn = användar_detaljer[0]
    detalj_ålder = användar_detaljer[2]
    detalj_kön = användar_detaljer[3]
    detaljer_saldo = användar_detaljer[4]
    personlig_detalj_skärm = Toplevel(GUI)
    personlig_detalj_skärm.title('Personliga detaljer')
    Label(personlig_detalj_skärm, text="Personliga detaljer", font=('deafult',12)).grid(row=0,sticky=N,pady=10)
    Label(personlig_detalj_skärm, text="Namn : "+detalj_namn, font=('deafult',12)).grid(row=1,sticky=W)
    Label(personlig_detalj_skärm, text="Ålder : "+detalj_ålder, font=('deafult',12)).grid(row=2,sticky=W)
    Label(personlig_detalj_skärm, text="Kön : "+detalj_kön, font=('deafult',12)).grid(row=3,sticky=W)
    Label(personlig_detalj_skärm, text="Saldo :Kr "+detaljer_saldo, font=('deafult',12)).grid(row=4,sticky=W)

def login():
    global temp_login_name
    global temp_login_password
    global login_notifikation
    global login_skärm
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    login_skärm = Toplevel(GUI)
    login_skärm.title('Login')
    Label(login_skärm, text="Logga in på ditt konto", font=('deafult',12)).grid(row=0,sticky=N,pady=10)
    Label(login_skärm, text="Användarnamn", font=('deafult',12)).grid(row=1,sticky=W)
    Label(login_skärm, text="Lösenord", font=('deafult',12)).grid(row=2,sticky=W)
    login_notifikation = Label(login_skärm, font=('deafult',12))
    login_notifikation.grid(row=4,sticky=N)
    Entry(login_skärm, textvariable=temp_login_name).grid(row=1,column=1,padx=5)
    Entry(login_skärm, textvariable=temp_login_password,show="*").grid(row=2,column=1,padx=5)
    Button(login_skärm, text="Login", command=login_session, width=15,font=('deafult',12)).grid(row=3,sticky=W,pady=5,padx=5)

#öppnar bilden med filnamnet
bild = Image.open('mora.png')
#ändrar storlekt på bilden
bild = bild.resize((300,300))
bild = ImageTk.PhotoImage(bild)

Label(GUI, text = "Bank application", font=('deafult',18)).grid(row=0,sticky=N,pady=10)
Label(GUI, text = "Använd alternativen nedan:", font=('deafult',14)).grid(row=1,sticky=N,pady=10)
Label(GUI, image=bild).grid(row=2,sticky=N,pady=15)
Label(GUI, text = "Mora please (oT-T)尸", font=("deafult", 10)).grid(row=2, sticky= N, pady=5)

Button(GUI, text="Registera", font=('deafult',12),width=20,command=registera).grid(row=3,sticky=N)
Button(GUI, text="Logga in", font=('deafult',12),width=20,command=login).grid(row=4,sticky=N,pady=10)

#startar gui
GUI.mainloop()