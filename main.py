# importejam bibliotekas
# from contextlib import redirect_stdout
import customtkinter # User interface
from PIL import Image # lai apstradat un paradit bildes
import os # lai stradat ar operatajsistemu un directorijam (tikai bildem)
import time # lai nomerit laiku datora gajienam

# izveidojam klasi Virsotne, kur glabajas visa info par katru virsotni koka
class Virsotne:
    
    # inicializacijas funkcija lai izveidotu objektu ar klasi Virsotne
    def __init__(self, id, akmenu_skaits = None, p1 = None, p2 = None, limenis = None, h_vertejums = None, starp_vertejums = None, precizs_vertejums = None, nogrieznis = None):
        self.id=id # virsotnes id
        self.akmenu_skaits = akmenu_skaits
        self.p1 = p1 # pirmajam speletajam punktu skaits
        self.p2 = p2 # otrajam speletajam punktu skaits
        self.limenis = limenis 
        self.h_vertejums = h_vertejums # hieristiskais vertejums virsotnei
        self.starp_vertejums = starp_vertejums # alpha-beta algoritmam
        self.precizs_vertejums = precizs_vertejums # alpha-beta algoritmam
        self.nogrieznis = nogrieznis # alpha-beta algoritmam

# izveidojam klasi Speles koks, kur glabajas visas virsotnes un pati koks               
class Speles_koks:
    
    # inicializacijas funkcija lai izveidotu objektu ar klasi speles koks
    def __init__(self):
        self.virsotnu_kopa=[] # massivs ar visam virsotnem. Tiek glabati ka objekti no klasa Virsotne 
        self.loku_kopa=dict() # vardnica ar visiem virostnu lokiem. {virsotnes id: [kreisa berna id, laba berna id]}

    # funkcija, lai pievienot objektu Virsotne pie massiva ar visam virsotnem
    def pievienot_virsotni(self, Virsotne):
        self.virsotnu_kopa.append(Virsotne)
        
    # funkcija, lai pievienot virsotni un vinu lokus pie vardnicas loku_kopa
    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        self.loku_kopa[sakumvirsotne_id]=self.loku_kopa.get(sakumvirsotne_id,[])+[beiguvirsotne_id]
            
# izpilda hierarhisku funkciju
def hierarhiska_funkcija(akmenu_skaits, player1_score, player2_score):
    score = 0
    # ja akmenu skits ir para skaitlis
    if akmenu_skaits % 2 == 0:
        score += 1
    
    # ja pirmajam speletajam ir vairak punktu neka otrajam
    if player1_score > player2_score:
        score += 1

    return score
# funkcija, lai generet koka vienu virsotni (it ka izpilda gajienu)
def koka_gajiena_generesana (gajiena_tips,generetas_virsotnes,pasreizeja_virsotne):
    # ja speletejs panem 2 akmeni
    if gajiena_tips=='1':
        akm_panem=2
        jauns_akmenu_skaits = pasreizeja_virsotne[1] - akm_panem
    # ja speletejs panem 3 akmeni
    else:
        akm_panem = 3
        jauns_akmenu_skaits = pasreizeja_virsotne[1] - akm_panem
    
    # parbaudam vai spele ir beigusies vai ne (pasreizeja_virsotne[1] = akmenu skaits)
    if pasreizeja_virsotne[1]>2:
        # j ir virsotnes nakotnes id
        global j
        id_new=j
        j+=1
        
        # parbaudam cik punktu ielikt klat
        # parbaudam (pasreizeja_virsotne[4] = limenis) vai ir para vai nepara skaitlis
        # (ja ir para skaitlis, tad ta bija 2.speletaja gajiens, ja nepara tad 1.speletaja gajiens)
        if (pasreizeja_virsotne[4] % 2) == 0:
            # parbaudam cik akmenu paliek pec gajiena (ja para skaitlis tad pielikam klat vel 2 papildpunkti,
            # ja nepara tad atnemam 2 punkti)
            if (jauns_akmenu_skaits % 2) == 0:
                p1_new=pasreizeja_virsotne[2]
                p2_new=pasreizeja_virsotne[3] + 2 + akm_panem
            else:
                p1_new=pasreizeja_virsotne[2]
                p2_new=pasreizeja_virsotne[3] - 2 + akm_panem
        else:
            if (jauns_akmenu_skaits % 2) == 0:
                p1_new=pasreizeja_virsotne[2] + 2 + akm_panem
                p2_new=pasreizeja_virsotne[3] 
            else:
                p1_new=pasreizeja_virsotne[2] - 2 + akm_panem
                p2_new=pasreizeja_virsotne[3] 
  
        # saskaitam jauno limeni (palielinam tekoso par 1 vertibu)
        limenis_new=pasreizeja_virsotne[4]+1;
        
        # saskaitam hierarhisku funkciju pie datora gajiena
        h_funkcijas_rezultats = 0
        if (pasreizeja_virsotne[4] % 2) == 1:
            h_funkcijas_rezultats = hierarhiska_funkcija(jauns_akmenu_skaits, p1_new, p2_new)
        jauna_virsotne=Virsotne(id_new, jauns_akmenu_skaits, p1_new, p2_new, limenis_new, h_funkcijas_rezultats, -2, -2, False)
        
        # parbaudam, vai virsotnu kopa un loku kopa, exsiste virsotne, kuru mes tikai sakam skaitit.
        # Ja virsotnes ir, tad ejam talak
        parbaude=False
        i=0
        while (not parbaude) and (i<=len(sp.virsotnu_kopa)-1):
            if (sp.virsotnu_kopa[i].akmenu_skaits==jauna_virsotne.akmenu_skaits) and (sp.virsotnu_kopa[i].p1==jauna_virsotne.p1) and (sp.virsotnu_kopa[i].p2==jauna_virsotne.p2) and (sp.virsotnu_kopa[i].limenis==jauna_virsotne.limenis):
                parbaude=True
            else:
                i+=1   
        # Ja virsotnes nav, tad izveidojam vinu un pielikam klat musu strukturam
        if not parbaude:
            sp.pievienot_virsotni(jauna_virsotne)
            generetas_virsotnes.append([id_new, jauns_akmenu_skaits, p1_new, p2_new, limenis_new, h_funkcijas_rezultats, -2, -2, False])
            sp.pievienot_loku(pasreizeja_virsotne[0],id_new)
        else:
            j-=1
            sp.pievienot_loku(pasreizeja_virsotne[0],sp.virsotnu_kopa[i].id)

# Ielikam dark mode musu modalajam logam
customtkinter.set_appearance_mode("dark")

# izveidojam musu lietotnes klasi ar mantosanu no customtkinter
class App(customtkinter.CTk):
    width = 900 # platums
    height = 600 # garums
    algorithm = "Minimax" # noklusejuma algoritms
    current_stones = 50 # noklusejuma akmenu skaits
    first_move_selection = "Dators" # noklusejuma, kurs izpilda pirmo gajienu
    Input_player_name = "name" # pec noklusejuma speletaja vards

    # inicializacija funkcija, lai izveidotu objektu ar klasi App
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # inicializet ar parent klase

        self.title("Stone game") # nosaukums musu spelei
        self.geometry(f"{self.width}x{self.height}") # modalaja loga izmeri
        self.resizable(False, False) # vai ems varam mainit izmeru pec hor. un vert. (ne, ne)


        # load and create background image (translate to LV?)
        current_path = os.path.dirname(os.path.realpath(__file__)) # kur mes nemam bildi
        # bildes radisana
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/stones2.jpg"),
                                               size=(self.width, self.height)) 
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame (1.logs, kur jaievada primaros datus)
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Spēle ar akmentiņiem",
                                                  font=customtkinter.CTkFont(size=22, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(35, 15))
        self.player_name = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Spēlētāja vārds")
        self.player_name.grid(row=1, column=0, padx=0, pady=(15, 15))
        self.algorithm_selection_label = customtkinter.CTkLabel(self.login_frame, text="Datora algoritms",
                                                  font=customtkinter.CTkFont(size=15))
        self.algorithm_selection_label.grid(row=2, column=0, padx=30, pady=(50, 10))
        self.algorithm_selection = customtkinter.CTkOptionMenu(self.login_frame, width=200,
                                                        values=["Minimax", "Alfa-beta"])
        self.algorithm_selection.grid(row=3, column=0, padx=10, pady=(0, 0))
        self.move_selection_label = customtkinter.CTkLabel(self.login_frame, text="Pirmais spēlē",
                                                  font=customtkinter.CTkFont(size=15))
        self.move_selection_label.grid(row=4, column=0, padx=30, pady=(50, 0))
        self.first_move_selection = customtkinter.CTkOptionMenu(self.login_frame, width=200,
                                                        values=["Dators", "Speletajs"])
        self.first_move_selection.grid(row=5, column=0, padx=30, pady=(15, 15))
        self.stone_number = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Akmeņu skaits (50-70)")
        self.stone_number.grid(row=6, column=0, padx=0, pady=(50, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Sākt spēli", command=self.login_event, width=200)
        self.login_button.grid(row=7, column=0, padx=30, pady=(50, 15))

        # create main frame (2.logs ar gajienem)
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Spēle ar akmentiņiem",
                                                font=customtkinter.CTkFont(size=22, weight="bold"))
        self.main_label.grid(row=0, column=2, padx=30, pady=(30, 15))
        self.player_name_displayed = customtkinter.CTkLabel(self.main_frame, text="Dators: " )
        self.player_name_displayed.grid(row=3, column=3, padx=30, pady=(30, 15))
        self.take2_button = customtkinter.CTkButton(self.main_frame, text="Paņemt 2", command=self.take_2_stones, width=200)
        self.take2_button.grid(row=5, column=1, padx=30, pady=(15, 15))
        self.take3_button = customtkinter.CTkButton(self.main_frame, text="Paņemt 3", command=self.take_3_stones, width=200)
        self.take3_button.grid(row=6, column=1, padx=30, pady=(15, 15))
        self.back_button = customtkinter.CTkButton(self.main_frame, text="Pārtraukt spēli", command=self.back_event, width=200)
        self.back_button.grid(row=7, column=2, padx=30, pady=(15, 15))

        self.pointsp1() # 1.speletaja punktu inicializacija
        self.pointsp2() # 2.speletaja punktu inicializacija
        self.uzvaretajs() 
        self.player_name_default = self.player_name
        self.first_move_selection_default = self.first_move_selection

    # koka generesana galvena funkcija
    def koka_generesana(self, kopejais_akmentinu_skaits):
        global sp
        sp=Speles_koks() # galvenais objekts
        generetas_virsotnes=[] # pagaidu (temp) datu struktura
        sakuma_id = 0 # sakuma virsotnes id

        # sakuma virostnes pievienosana
        sp.pievienot_virsotni(Virsotne(sakuma_id, kopejais_akmentinu_skaits, 0, 0, 1, 0, -2, -2, False))
        generetas_virsotnes.append([sakuma_id, kopejais_akmentinu_skaits, 0, 0, 1, 0, -2, -2, False])

        # tagadnejas virsotnes id
        global j
        j=sakuma_id+1
        # while kamer visas virsotnes nav apkatitas
        while len(generetas_virsotnes) > 0:
            # panemam virsotni    
            pasreizeja_virsotne=generetas_virsotnes[0]
            # izpildam 2 gajienus (izveidojam divus bernus)    
            koka_gajiena_generesana('1',generetas_virsotnes,pasreizeja_virsotne)
            koka_gajiena_generesana('2',generetas_virsotnes,pasreizeja_virsotne)
            generetas_virsotnes.pop(0)
        # atgriezam speles koka objektu
        return sp
    
    # Atjaunot speletaja vardu
    def reset_player_name(self):
        self.player_name = self.player_name_default
    # Atjaunot mainigo, kura atbild par kurs izpilda pirmo gajienu
    def reset_first(self):
        self.first_move_selection = self.first_move_selection_default
    
    # minimaksa galvena funkcija
    def minimax(self, sp, pirmais_gajiens_dators):

        global minimax_score
        minimax_score = dict() # izveidojam dictionary, kura glabasim aprēķinātās virsotnes

        for stavoklis in sp.virsotnu_kopa:
            # noskaidrot vai ir pecteci(berni) vai ne
            if stavoklis.id not in sp.loku_kopa.keys():
                    # pievienot vertejumu
                    # ja pirmais speletajs uzvar
                    if stavoklis.p1 > stavoklis.p2:
                        minimax_score.update({stavoklis.id: 1})
                    # ja neizskirts
                    elif stavoklis.p1 == stavoklis.p2:
                        minimax_score.update({stavoklis.id: 0})
                    # ja otrais speletajs uzvar
                    else:
                        minimax_score.update({stavoklis.id: -1})

        # noskaidrot pedejo limeni
        kopejais_limenu_skaits = sp.virsotnu_kopa[-1].limenis
        
        # novertesim stavoklus(virsotnes) no lejas uz augsu
        for pasreizeis_limenis in range(kopejais_limenu_skaits-1, 0, -1):
            # atradam visus virsotens uz saja limeni, kuri vel nav noverteti
            for stavoklis in sp.virsotnu_kopa:
                if stavoklis.limenis == pasreizeis_limenis and not minimax_score.get(stavoklis.id):
                    # panemam pectecus(bernus) no virsotnes
                    # pievinosim try catch bloku, jo dazreiz algoritms "grib" novertet virsotni otruo reizi
                    try:
                        pecteci = sp.loku_kopa[stavoklis.id] # []
                    except:
                        continue
                    else:
                        pecteci = sp.loku_kopa[stavoklis.id]
                    # noskaidrot kads ir limenis (min vai max) even(para) = min, odd(nepara) = max
                    if pasreizeis_limenis % 2 == 0:
                        # vertejums(score) no pecteciem(berniem)
                        pasreizejs_score = min( minimax_score.get(pecteci[0]),  minimax_score.get(pecteci[1]))
                        # pievienosim jaunu virsotni ar vertejumu(score)
                        minimax_score.update({stavoklis.id: pasreizejs_score})
                    else:
                        # ja max limenis
                        pasreizejs_score = max( minimax_score.get(pecteci[0]),  minimax_score.get(pecteci[1]))
                        minimax_score.update({stavoklis.id: pasreizejs_score})
                        
        if pirmais_gajiens_dators == "Speletajs":
            for key, value in minimax_score.items():
                if value > 0:
                    minimax_score.update({key: value-2})
                elif value < 0:
                    minimax_score.update({key: value+2})

        return minimax_score
    # izvadit novertetus virsotnus
    # print(dict(sorted(minimax_score.items(), key=lambda item: item[1])))

    # Alfa-beta algoritms
    def alphabeta(self, sp, pirmais_gajiens_dators, alpha=float('-1'), beta=float('1')):

        global minimax_score
        minimax_score = dict() # izveidojam dictionary, kura glabasim aprēķinātās virsotnes

        for stavoklis in sp.virsotnu_kopa:
            # noskaidrot vai ir pecteci(berni) vai ne
            if stavoklis.id not in sp.loku_kopa.keys():
                    # pievienot vertejumu
                    # ja pirmais speletajs uzvar
                    if stavoklis.p1 > stavoklis.p2:
                        minimax_score.update({stavoklis.id: 1})
                    # ja neizskirts
                    elif stavoklis.p1 == stavoklis.p2:
                        minimax_score.update({stavoklis.id: 0})
                    # ja otrais speletajs uzvar
                    else:
                        minimax_score.update({stavoklis.id: -1})

        # noskaidrot pedejo limeni
        kopejais_limenu_skaits = sp.virsotnu_kopa[-1].limenis
        
        for pasreizeis_pedejais_limenis in range(kopejais_limenu_skaits-1, 0, -1):
            for stavoklis in sp.virsotnu_kopa:
                if stavoklis.limenis == pasreizeis_pedejais_limenis and not minimax_score.get(stavoklis.id):
                    try:
                        pecteci = sp.loku_kopa[stavoklis.id]
                    except KeyError:
                        continue
                    else:
                        pecteci = sp.loku_kopa[stavoklis.id]
                    
                    if pasreizeis_pedejais_limenis % 2 == 0:
                        pasreizejs_score = min(
                            minimax_score.get(pecteci[0], alpha),
                            minimax_score.get(pecteci[1], alpha),
                            alpha,
                            beta
                        )
                        minimax_score[stavoklis.id] = pasreizejs_score
                        beta = min(beta, pasreizejs_score)
                        if pasreizejs_score <= alpha:
                            break
                    else:
                        pasreizejs_score = max(
                            minimax_score.get(pecteci[0], beta),
                            minimax_score.get(pecteci[1], beta),
                            alpha,
                            beta
                        )
                        minimax_score[stavoklis.id] = pasreizejs_score
                        alpha = max(alpha, pasreizejs_score)
                        if pasreizejs_score >= beta:
                            break

        if pirmais_gajiens_dators == "Speletajs":
            for key, value in minimax_score.items():
                if value > 0:
                    minimax_score.update({key: value-2})
                elif value < 0:
                    minimax_score.update({key: value+2})

        return minimax_score
    
    # datora gajiena funkcija kura atgriez tikai labako virsotni (izvelas bernu ar labako vertejumu, pec algoritma beigsanas)
    def datora_gajiens(self, sp, virsotne_id):
        # parbaudam vai virsotnei eksiste berni
        if sp.loku_kopa.get(virsotne_id) is not None:
            berni = sp.loku_kopa.get(virsotne_id)
            # meginam dabut rezultatu no berniem (parbaudam vai kad ir nogriezts)
            try:
                try:
                    int(minimax_score.get(berni[1]))
                except:
                    return sp.virsotnu_kopa[berni[0]]
                try:
                    int(minimax_score.get(berni[0]))
                except:
                    return sp.virsotnu_kopa[berni[1]]
            except:
                print("Nogriezni") 
            else: # ja abi berni ir, salidzinam vinus (panemam lielaku)
                if int(minimax_score.get(berni[0])) >= int(minimax_score.get(berni[1])):
                    return sp.virsotnu_kopa[berni[0]]
                else:
                    return sp.virsotnu_kopa[berni[1]]

    # saglabajam ievaditus datus
    def login_event(self):
        self.player_name=self.player_name.get() # speletaja vards
        self.algorithm = self.algorithm_selection.get() # algoritms
        self.first_move_selection = self.first_move_selection.get() # kurs izpilda pirmo gajienu
        self.current_stones=self.stone_number.get() # tagadnejais akmenu skaits
        self.speles_koks = self.koka_generesana(int(self.current_stones)) # izveido koku
        # izpildit vai minimaksa algo, vai alfa-beta
        st = time.time()
        if self.algorithm == "Minimax":
            self.minimax_score = self.minimax(self.speles_koks, self.first_move_selection)
        else:
            self.minimax_score = self.alphabeta(self.speles_koks, self.first_move_selection)
        et = time.time()
        elapsed_time = et - st
        print('Execution time minimaksa:', elapsed_time, 'seconds') # paradam cik laika izpildas algoritms
        
        self.pozicija_koka_tagad = 0    
        print("Player name:", self.player_name, "algorithm:", self.algorithm, "first move:", self.first_move_selection, "stone number", self.current_stones)

        self.login_frame.grid_forget()  # remove login frame
        st = time.time()
        if self.first_move_selection == "Dators":
            self.datora_gajiensai() #funkcija
        et = time.time()
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')
        self.stones_update() # akmenu atjaunosana uz UI (grafiska saskarne)
        self.initial_update() # sakuma grafiska saskarne atjaunisana un pierakstisana uz ekrana
        self.punktu_skaitu_update() # punktu skaitu atjaunosana uz ekrana
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame
        
    # akmenu atjaunosana uz UI (grafiska saskarne)
    def stones_update(self):
        self.stone_counter = customtkinter.CTkLabel(self.main_frame, text="Akmeņu skaits tagad ir "+str(self.current_stones), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.stone_counter.grid(row=2, column=2, padx=30, pady=(30, 15))
    
    # sakuma grafiska saskarne atjaunisana un pierakstisana uz ekrana
    def initial_update(self):
        self.first_move = customtkinter.CTkLabel(self.main_frame, text=self.first_move_selection +" spēlē pirmais",
                                                font=customtkinter.CTkFont(size=22, weight="bold"))
        self.first_move.grid(row=1, column=2, padx=30, pady=(30, 15))
        self.comp_algo_label = customtkinter.CTkLabel(self.main_frame, text= "Datora algoritms: " +self.algorithm)
        self.comp_algo_label.grid(row=3, column=3, padx=30, pady=(30, 15))
        self.player_name_displayed = customtkinter.CTkLabel(self.main_frame, text="Spēlētājs: " + self.player_name)
        self.player_name_displayed.grid(row=3, column=1, padx=30, pady=(30, 15))

    # punktu skaitu atjaunosana uz ekrana
    def punktu_skaitu_update(self):
            self.first_score_label = customtkinter.CTkLabel(self.main_frame, text= "Datora punktu skaits: " + str(self.pointsp22))
            self.first_score_label.grid(row=4, column=3, padx=30, pady=(30, 15))
            self.second_score_label = customtkinter.CTkLabel(self.main_frame, text="Spēlētāja punktu skaits: " + str(self.pointsp11))
            self.second_score_label.grid(row=4, column=1, padx=30, pady=(30, 15))
        
    # funkcija, cilveka gajiens kad panem 2 akmenus
    def take_2_stones(self):
        # Kura virsotne mes esam tagad
        self.pozicija_koka_tagad= self.speles_koks.loku_kopa.get(self.pozicija_koka_tagad)[0]
        # jasaskaita jauno akmentiu skaitu
        self.current_stones = str(self.speles_koks.virsotnu_kopa[self.pozicija_koka_tagad].akmenu_skaits)
        # jaatjauno kopejo akmenu skaitu lietotajam
        self.stones_update()

        self.pointsp11 += 2 # pieskaitam punkti par akmeniem

        # pieskaitam papildpunktus par para vai nepara kopeju akmena skaitu
        if int(self.current_stones) % 2 ==0:
            self.pointsp11 += 2
        else:
            self.pointsp11 -= 2

        # parbaudam vai spele ir beidzas, ja ne tad ir datora gajiens
        if int(self.current_stones) <= 2: 
            self.game_end()
        else:
            st = time.time()
            self.datora_gajiensai()
            et = time.time()
            elapsed_time = et - st
            print('Execution time:', elapsed_time, 'seconds')
        # atjaunojam punktu skaitu uz ekrana
        self.punktu_skaitu_update()
        
    
    # funkcija, cilveka gajiens kad panem 3 akmenus
    def take_3_stones(self):
        # Kura virsotne mes esam tagad
        self.pozicija_koka_tagad= self.speles_koks.loku_kopa.get(self.pozicija_koka_tagad)[1]
        # jasaskaita jauno akmentiu skaitu
        self.current_stones = str(self.speles_koks.virsotnu_kopa[self.pozicija_koka_tagad].akmenu_skaits)
        # jaatjauno kopejo akmenu skaitu lietotajam
        self.stones_update()
        # par akmeniem pieskiram punktus
        self.pointsp11 += 3 

        # pieskaitam papildpunktus par para vai nepara kopeju akmena skaitu
        if int(self.current_stones) % 2 ==0:
            self.pointsp11 += 2
        else:
            self.pointsp11 -= 2

        # parbaudam vai spele ir beidzas, ja ne tad ir datora gajiens
        if int(self.current_stones) <= 2:
            self.game_end()
        else:
            st = time.time()
            self.datora_gajiensai() #funkcija
            et = time.time()
            elapsed_time = et - st
            print('Execution time:', elapsed_time, 'seconds')
        # atjaunojam punktu skaitu uz ekrana
        self.punktu_skaitu_update()
        
     
    # datora gajiens, kurs skaitas: punkti, kopeju akmenu skaits, un pati rezultats paradas uz ekrana
    def datora_gajiensai(self):
        # akmenu skaits pirms gajiena
        self.stones_count_before_step = self.speles_koks.virsotnu_kopa[self.pozicija_koka_tagad].akmenu_skaits
        # tagadneja virsotnes id
        self.pozicija_koka_tagad = self.datora_gajiens(sp, self.pozicija_koka_tagad).id 
        # tagadnejs kopeju akmenu skaits
        self.current_stones = str(self.speles_koks.virsotnu_kopa[self.pozicija_koka_tagad].akmenu_skaits)
        self.panemtie_akmeni = self.stones_count_before_step - int(self.current_stones)
               
        # par akmeniem pieskirt       
        self.pointsp22 += self.panemtie_akmeni  
        # atjaunojam punktu skaitu uz ekrana 
        self.stones_update() 
        # pieskaitam papildpunktus par para vai nepara kopeju akmena skaitu
        if int(self.current_stones) % 2 ==0:
            self.pointsp22 += 2
        else:
            self.pointsp22 -= 2

        # parbaudam vai spele ir beidzas
        if int(self.current_stones) <= 2:  # Check if stone number is 2 or less
            self.game_end()
            
    # funkcija, kura atlauja partraukt speli jebkada bridi un sakt pa jauno
    def back_event(self):
        self.main_frame.grid_forget()  # remove main frame
        self.reset_player_name()
        self.reset_first()
        self.pointsp11 = 0
        self.pointsp22 = 0
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame
    
    # funkcija, kura tiek iedarbinata, kad mes gribam sakt speli no jauna
    def jauns_event(self):
        self.main_frame.grid_forget()
        self.uzvar.grid_forget()
        self.uzvar1.grid_forget()
        self.uzvarar_button.grid_forget()
        self.uzvarar_kurs.grid_forget()
        self.uzvarar_kurs1.grid_forget()
        self.uzvarar_kurs2.grid_forget()
        self.pointsp11 = 0
        self.pointsp22 = 0
        self.reset_player_name()
        self.reset_first()
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    # funkcija, kura tiek iedarbinata kad spele ir beidzas
    def game_end(self):
        self.main_frame.grid_forget()  # remove main frame
        self.uzvaretajs()  # Determine the winner

        self.uzvar = customtkinter.CTkFrame(self, corner_radius=0)
        self.uzvar.grid(row=0, column=0, sticky="ns", padx=100)
        self.uzvar1 = customtkinter.CTkLabel(self.uzvar, text="Spēle ar akmentiņiem",
                                            font=customtkinter.CTkFont(size=22, weight="bold"))
        self.uzvar1.grid(row=0, column=0, padx=30, pady=(15, 15))

        self.uzvarar_kurs = customtkinter.CTkLabel(self.uzvar, text= self.Uzvaretajs1)
        self.uzvarar_kurs.grid(row=2, column=0, padx=30, pady=(15, 15))  

        self.uzvarar_kurs1 = customtkinter.CTkLabel(self.uzvar, text="Punkti spēlētājam: " + self.Punktisp1)
        self.uzvarar_kurs1.grid(row=3, column=0, padx=30, pady=(15, 15)) 
        self.uzvarar_kurs2 = customtkinter.CTkLabel(self.uzvar, text="Punkti datoram:" + self.Punktisp2)
        self.uzvarar_kurs2.grid(row=4, column=0, padx=30, pady=(15, 15)) 

        self.uzvarar_button = customtkinter.CTkButton(self.uzvar, text="Sākt jaunu spēli", command=self.jauns_event, width=200)
        self.uzvarar_button.grid(row=5, column=0, padx=30, pady=(15, 15))

    # pieskiram 0 vertibu punktu skaitam 1.speletajam
    def pointsp1(self):
        self.pointsp11 = 0
        
    # pieskiram 0 vertibu punktu skaitam 2.speletajam
    def pointsp2(self):
        self.pointsp22 = 0
        
    # funkcija, kura nosaka kurs uzvareja
    def uzvaretajs(self):
        if self.pointsp11 > self.pointsp22:
            self.Uzvaretajs1 = "Uzvar Spēlētājs"
            self.Punktisp1 = str(self.pointsp11)
            self.Punktisp2 = str(self.pointsp22)
        elif self.pointsp11 < self.pointsp22:
            self.Uzvaretajs1 = "Uzvar Dators"
            self.Punktisp1 = str(self.pointsp11)
            self.Punktisp2 = str(self.pointsp22)
        else:
            self.Uzvaretajs1 = "Rezultats ir neizšķirts"
            self.Punktisp1 = str(self.pointsp11)
            self.Punktisp2 = str(self.pointsp22)

if __name__ == "__main__":
    app = App()
    app.mainloop()



    