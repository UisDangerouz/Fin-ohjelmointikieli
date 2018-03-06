import sys
from datetime import datetime
import time
import os

#GLOBAALEJA MUUTTUJIA
koodi_tiedosto_nimi = "koodi.txt"
koodin_aloitus_aika = datetime.now()
#JOS TRUE KIRJOITTAA kirjoita_log_tietoa() KUTSUT, PÄÄLLÄ OLLESSA HELPOMPI DEBUGATA KOODIA
debug_mode = True

#TYHJENTÄÄ KONSOLIN TEKSISTÄ, KOODI TARKISTAA MIKÄ KÄYTTÖJÄRJESTELMÄ ON KYSEESSÄ JA VALITSEE SEN MUKAAN OIKEAN clear TAVAN
def siivoa_konsoli():
    os.system('cls' if os.name=='nt' else 'clear')

#LUOKKA KOMENNOT
class komennot:
	jos = "jos"
	kirjoita = "kirjoita"
	muuttuja = "muuttuja"
	kommentti = "#"
	aseta = "aseta"
	debug_kirjoitus_pois = "debug_kirjoitus_pois"
	odota_input = "odota_input"
	mene = "mene"
	odota = "odota"
	siivoa = "siivoa"

#LUOKKA VÄRIT
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#alustetaan funktiot
def kirjoita_log(teksti):
	nykyinen_aika = datetime.now()
	print(colors.OKGREEN +  "[" + nykyinen_aika.strftime('%d.%m.%Y %H:%M:%S') + "] " + teksti)

def kirjoita_log_virhe(teksti):
	nykyinen_aika = datetime.now()
	print(colors.FAIL +  "[" + nykyinen_aika.strftime('%d.%m.%Y %H:%M:%S') + "] " + teksti)

def kirjoita_log_tietoa(teksti):
	if debug_mode == True:
		nykyinen_aika = datetime.now()
		print(colors.OKBLUE +  "[" + nykyinen_aika.strftime('%d.%m.%Y %H:%M:%S') + "] " + teksti)

def aika_sekunneiksi(aika_string):
	t, m, s = aika_string.split(":")
	return  str(int(t) * 3600 + int(m) * 60 + float(s))

def korvaa_muuttujat(teksti, muuttujan_nimet, muuttujan_arvot):
	#KORVAA MUUTTUJIEN NIMET NIIDEN ARVOILLA
	for muuttuja in range(0, len(muuttujan_nimet)):
		if muuttujan_nimet[muuttuja] in str(teksti):
			teksti = teksti.replace(str(muuttujan_nimet[muuttuja]), str(muuttujan_arvot[muuttuja]))
	return teksti

def koodin_suorittaja(koodi):
	tokenit, kihara_sulku_info = generoi_tokenit(koodi)
	#ALKUPERÄINEN TOKEN SISÄLTÄÄ ALKUPERÄISEN ARVON, ENNEN MUUTTUJAN NIMEN KORVAUSTA ARVOLLA, HUOM KÄYTETÄÄN AINOASTAAN KORVAA_MUUTTUJAT FUNKTIOSSA
	orig_tokenit = tokenit[:]


	kirjoita_log("Suoritetaan koodia...")
	koodin_aloitus_aika = datetime.now()

	#OHJELMAN MUUTTUJAT 
	muuttuja_arvot = []
	muuttuja_nimet = []

	#LASKEE MILLÄ RIVILLÄ OHJELMA ON
	rivi_nro = 1
	viimeinen_rivi = rivi_nro
	#TALLENTAA TOKENIN NUMERON, JOLLA UUSI RIVI ALKAA
	rivi_alku_token_num = [] 


	#i = token num
	i = 0 
	#ALOITUS i:n arvo
	aloitus_i = 0
	while i <= len(tokenit):
		aloitus_i = i

		if len(tokenit) > i + 1 and tokenit[i-1] == "rivi_loppu":
			rivi_alku_token_num.append(str(rivi_nro) + ":" + str(i))
		if len(tokenit) > i and tokenit[i] == "rivi_loppu":
			rivi_nro += 1
			viimeinen_rivi = rivi_nro

		#JOS
		if len(tokenit) >= i + 6 and tokenit[i] == komennot.jos and tokenit[i+1] == "(" and tokenit[i+2] and tokenit[i+3] == "==" and tokenit[i+4] and tokenit[i+5] == ")" and tokenit[i+6][:1] == "{":

			#KORVAA MUUTTUJIEN NIMET NIIDEN ARVOILLA JOS NIITÄ LÖYTYY
			tokenit[i+2] = korvaa_muuttujat(tokenit[i+2],muuttuja_nimet,muuttuja_arvot)
			tokenit[i+4] = korvaa_muuttujat(tokenit[i+4],muuttuja_nimet,muuttuja_arvot)

			if not tokenit[i+2] == tokenit[i+4]:
				#Jos Ehto ei toteudu hyppää jos lauseen loppuun
				for sulku in kihara_sulku_info:
					alku, loppu = sulku.split(":")

					if int(alku) == i + 6:
						i = int(loppu)
						break

			tokenit[i+2] = orig_tokenit[i+2]
			tokenit[i+4] = orig_tokenit[i+4]

		#KIRJOITA				
		elif len(tokenit) >= i + 3 and tokenit[i] == komennot.kirjoita and tokenit[i+1] == "(" and tokenit[i+2] and tokenit[i+3] == ")":

			#KORVAA MUUTTUJIEN NIMET NIIDEN ARVOILLA
			tokenit[i+2] = korvaa_muuttujat(tokenit[i+2],muuttuja_nimet,muuttuja_arvot)

			#POISTAA HIPSUT, KOSKA NIITÄ EI ENÄÄ TARVITA
			tokenit[i+2] = tokenit[i+2].replace("\"","")
			print(tokenit[i+2])

			tokenit[i+2] = orig_tokenit[i+2]

		#ODOTA
		elif len(tokenit) >= i + 3 and tokenit[i] == komennot.odota and tokenit[i+1] == "(" and tokenit[i+2] and tokenit[i+3] == ")":
			time.sleep(int(tokenit[i+2]))

		#LUO MUUTTUJA
		elif len(tokenit) >= i + 3 and tokenit[i] == komennot.muuttuja and tokenit[i+1] == "(" and tokenit[i+2] and tokenit[i+3] == ")":
			if not tokenit[i+2] in {komennot.aseta, komennot.muuttuja, komennot.jos, komennot.kirjoita, komennot.debug_kirjoitus_pois, komennot.odota_input}:
				if tokenit[i+2].isalpha():
					muuttuja_nimet.append(str(tokenit[i+2]))
					muuttuja_arvot.append("")
				else:
					kirjoita_log_virhe("Virhe rivillä " + str(rivi_nro) + " muuttujan nimessä voi olla ainoastaan kirjaimia")
			else:
				kirjoita_log_virhe("Virhe rivillä " + str(rivi_nro) + " et voi luoda muuttujaa, jonka nimi on " + tokenit[i+2] + ", koska se on komento")

		#ASETA MUUTTUJA
		elif len(tokenit) >= i + 5 and tokenit[i] == komennot.aseta and tokenit[i+1] == "(" and tokenit[i+2] and tokenit[i+3] == "=" and tokenit[i+4] and tokenit[i+5] == ")":
			#ETSII KYSEISEN MUUTTUJAN JA ASETTAA SEN HALUTTUUN ARVOON
			muuttuja_olemassa = False

			for muuttuja in range(0, len(muuttuja_nimet)):
				if muuttuja_nimet[muuttuja] == tokenit[i+2]:
					#KORVAA MUUTTUJIEN NIMET NIIDEN ARVOILLA
					if tokenit[i+4] == komennot.odota_input:
						tokenit[i+4] = input(">")
					else:
						tokenit[i+4] = korvaa_muuttujat(tokenit[i+4],muuttuja_nimet,muuttuja_arvot)

					#JOS ASETETTAVASSA ARVOSSA EI OLE HIPSUJA, YRITTÄÄ LASKEA ARVOT YHTEEN
					if "\"" not in str(tokenit[i+4]):
						try:
							tokenit[i+4] = eval(tokenit[i+4])
						except:
							muuttuja_arvot[muuttuja] = tokenit[i+4]
							pass

					muuttuja_arvot[muuttuja] = tokenit[i+4]
					muuttuja_olemassa = True

					tokenit[i+4] = orig_tokenit[i+4]

			if not muuttuja_olemassa:
				kirjoita_log_virhe("Virhe rivillä " + str(rivi_nro) + " muuttujaa " + tokenit[i+2] + " ei ole olemassa")
		
		#MENE
		elif len(tokenit) >= i + 3 and tokenit[i] == komennot.mene and tokenit[i+1] == "(" and tokenit[i+2].isdigit and tokenit[i+3] == ")":
			#KOHDE RIVI ON -1 SILLÄ HALUAMME SUORITTAA SIITÄ RIVISTÄ _LÄHTIEN_
			kohde_rivi = int(tokenit[i+2]) - 1
			kohde_rivi = str(kohde_rivi)

			token_index = 0
			for tok in tokenit:
				
				if "rivi_loppu:" in str(tok):
					alku, loppu = tok.split(":")

					if loppu == kohde_rivi:
						i = token_index 

				token_index += 1
		#SIIVOA
		elif len(tokenit) >= i + 3 and tokenit[i] == komennot.siivoa and tokenit[i+1] == "("  and tokenit[i+3] == ")":
			print("LOL")
			siivoa_konsoli()

		#TARKISTAA, ETTÄ SUORITUS EI OLE HYPÄNNYT TOISELLE RIVILLE esim. JOS LAUSEEN LOPPU
		if aloitus_i == i:
			i += 1

	for muuttuja in range(0, len(muuttuja_nimet)):
		kirjoita_log_tietoa("muuttuja " + str(muuttuja) + ": " + muuttuja_nimet[muuttuja] + " = " + str(muuttuja_arvot[muuttuja]))



def generoi_tokenit(koodi):
	kirjoita_log("Luetaan merkkejä...")

	lukija = ""
	tokenit = []

	#0 = tällä hetkellä ei yhtään sulkuja auki 
	sulkuja = 0
	kiharia_sulkuja = 0
	# kihara_sulku_info[aloitus_token] = lopetus_token
	kihara_sulku_info = []
	hipsuja = 0

	#LASKEE MILLÄ RIVILLÄ OHJELMA ON
	rivi_nro = 0

	for rivi in koodi.split("\n"):

		for merkki in rivi:
			#HIPSUT
			if merkki == "\"":
				if hipsuja == 0:
					hipsuja = 1
				elif hipsuja == 1:
					hipsuja = 0

			#POISTAA " " JOS HIPSUT EI AUKI
			if merkki == " " and hipsuja == 0:
				merkki = ""


			#LUKIJA
			lukija += merkki 


			#JOS KOMENTTI LOPETTAA RIVIN SUORITTAMISEN
			if lukija == komennot.kommentti:
				lukija = ""
				break

			#TESTAA LÖYTYYKÖ KOMENTOJA
			elif lukija in {komennot.aseta, komennot.muuttuja, komennot.jos, komennot.kirjoita, komennot.debug_kirjoitus_pois, komennot.mene, komennot.odota, komennot.siivoa}:
				tokenit.append(lukija)
				lukija = ""

			#SULUT 
			elif merkki == "(":
				tokenit.append(lukija)
				lukija = ""
				sulkuja += 1

			#PARAMETRIT
			elif sulkuja > 0 and merkki == ")":
				if "==" in lukija:
					parametrit = lukija[:len(lukija) - 1].split("==")
					tokenit.append(parametrit[0])
					tokenit.append("==")
					tokenit.append(parametrit[1])
				elif "=" in lukija :
					parametrit = lukija[:len(lukija) - 1].split("=")
					tokenit.append(parametrit[0])
					tokenit.append("=")
					tokenit.append(parametrit[1])
				else:
					tokenit.append(lukija[:len(lukija) - 1])

				tokenit.append(merkki)
				lukija = ""
				sulkuja -= 1

			#KIHARAT SULUT
			elif lukija == "{":
				tokenit.append(lukija)
				kihara_sulku_info.append(str(len(tokenit)-1) + ":" + str(kiharia_sulkuja))

				lukija = ""
				kiharia_sulkuja += 1

			elif kiharia_sulkuja > 0 and merkki == "}":
				tokenit.append(lukija[:len(lukija) - 1])
				tokenit.append(merkki)

				lukija = ""	
				kiharia_sulkuja -= 1

				sulku_index = 0
				#TALLENTAA SULUN ALKU JA LOPPU KOHDAN
				for sulku in kihara_sulku_info:
					alku, loppu = sulku.split(":")

					if str(loppu) == str(kiharia_sulkuja):
						#KUN AVOIMEN SULKEEN LOPPU LÖYDETTY TÄYDENTÄÄ LOPPU KOHDAN SAMAAN MUUTTUJAAN
						kihara_sulku_info[sulku_index] = alku + ":" + str(len(tokenit) - 1) 

					sulku_index += 1

		#LISÄÄ RIVI_LOPPU, KUN RIVI PÄÄTTYY, TARKOITUKSELLA ENSIN LISÄÄ 1 JONKA JÄLKEEN LSIÄÄ TOKENIN SILLÄ IHMISELLE 1 ON ENSIMMÄINEN OHJELMALLE 0 ON ENSMIMMÄINEN RIVI
		rivi_nro += 1
		tokenit.append("rivi_loppu:" + str(rivi_nro))

		lukija = ""



	#LISÄÄ KOODIN LOPPUUN 20 rivi_loppu, jotta mene() toimisi 20 riviä koodin loputtua
	for n in range(0,20):
		rivi_nro += 1
		tokenit.append("rivi_loppu:" + str(rivi_nro))

	#MUUNTAA KAIKKI TOKENIT STRINGIKSI
	for token_ind in range(0,len(tokenit)):
		tokenit[token_ind] = str(tokenit[token_ind])




	if tokenit[0] == komennot.debug_kirjoitus_pois:
		global debug_mode 
		debug_mode = False

	for i in range(0,len(tokenit)):
		kirjoita_log_tietoa("merkki " + str(i).zfill(3) + ": " + tokenit[i])
	
	for sulku in kihara_sulku_info:
		print(sulku)
		alku, loppu = sulku.split(":")
		kirjoita_log_tietoa("Koodi sulku alkaa kohdassa " + str(alku) + " ja loppuu " + str(loppu))

	#VIRHEIDEN TARKASTUS
	if sulkuja > 0:
		kirjoita_log_virhe("Virhe: ) puuttuu jostakin")
	elif sulkuja < 0:
		kirjoita_log_virhe("Virhe: ( puuttuu jostakin")

	if kiharia_sulkuja > 0:
		kirjoita_log_virhe("Virhe: } puuttuu jostakin")
	elif sulkuja < 0:
		kirjoita_log_virhe("Virhe: { puuttuu jostakin")

	return tokenit, kihara_sulku_info



kirjoita_log("Etsitään suoritettavaa koodia (" + koodi_tiedosto_nimi + ")...")

#testataan löytyykö koodi tiedostoa, jos ei löydy tekee sen
try:
	koodi_tiedosto = open(koodi_tiedosto_nimi,'r', encoding='utf-8-sig')
	kirjoita_log("Suoritettava koodi löytyi...")

	#tiedosto löydetty, luetaan se
	koodi = koodi_tiedosto.read()
	koodi_tiedosto.close
	#suoritetaan koodi
	koodin_suorittaja(koodi)
except FileNotFoundError:
	kirjoita_log_virhe("Koodi tiedostoa ei löytynyt...")
	kirjoita_log("Luodaan koodi tiedosto...")
	kirjoita_log_tietoa("Luodusta Koodi tiedostosta löytyy lisätietoja tästä ohjelmointikielestä.")

	koodi_tiedosto = open(koodi_tiedosto_nimi,'w', encoding='utf-8-sig')

	koodi_tiedosto.write("# Fin-ohjelmointikieli 1.0\n")
	koodi_tiedosto.write("\n")
	koodi_tiedosto.write("# Copyright Matias Rantala. Kaikki oikeudet pidetään.\n")
	koodi_tiedosto.write("\n")
	koodi_tiedosto.write("# Syntaksi:\n")
	koodi_tiedosto.write("# debug_kirjoitus_pois            || ei näytä debuggaamiseen tarvittavia tietoja koodia suoritettaessa. Tämä komento pitää olla ensimmäinen ohjelman komento toimiakseen.\n")
	koodi_tiedosto.write("# jos(x==y) {suoritettava koodi.} || Jos x ei ole y hyppää sulkujen {, } sisällä olevan koodin yli.\n")
	koodi_tiedosto.write("# aseta(x=5)                      || asettaa x arvoon. 5\n")
	koodi_tiedosto.write("# odota(5)                        || Odottaa 5 sekuntia.\n")
	koodi_tiedosto.write("# aseta(x=odota_input)            || Odottaa käyttäjän inputtia ja tallentaa sen muuttujaan.\n")
	koodi_tiedosto.write("# mene(4)                         || Menee riville 4. x\n")
	koodi_tiedosto.write("#                                 || Kommentti. Lopettaa koko rivin suorituksen ja jatkaa seuraavalle riville.\n")
	koodi_tiedosto.write("# siivoa()                        || Tyhjentää konsolin tekstistä. Huom! ei toimi muualla kuin Windows ja Linux konsoleissa\n")
	koodi_tiedosto.write("\n")
	koodi_tiedosto.write("Muuta huomioitavaa:\n")
	koodi_tiedosto.write("# 1) Ohjelmointikielen info-kirjoitukset ovat sinisiä, debug-kirjoitukset vihreitä ja virhe-ilmoitukset punaisia, mutta värit näkyvät vain väriä-tukevissa konsoleissa.\n")
	koodi_tiedosto.write("# 2) ...\n")







#time.sleep(3.5)

#LASKEE AJAN SEKUNTTEINA, JOKA MENI KOODIN SUORITUKSEEN
suoritus_aika = (datetime.now() - koodin_aloitus_aika )
suoritus_aika = aika_sekunneiksi(str(suoritus_aika))
kirjoita_log("Koodi suoritettu (" + suoritus_aika + " sekunnissa)")