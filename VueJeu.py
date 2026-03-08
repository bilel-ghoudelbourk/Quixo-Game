import tkinter as tk
import GameConfig
class VueJeu:
    def __init__(self, jeu):
        self.jeu = jeu
        self.window = tk.Tk()
        self.window.title("Quixo Game")
        self.window.geometry("700x850")
        self.window.resizable(False, False)
        self.current_position = (None, None)
        self.is_selected = False
        self.game_over = False
        self.ai_delay_ms = 800
        self.create_mode_selection_ui()


    def set_controller(self, controller):
        self.controller = controller

    def create_mode_selection_ui(self):
        self.window.configure(bg=GameConfig.COULEUR_FOND)

        self.mode_frame = tk.Frame(self.window, bg=GameConfig.COULEUR_FOND)
        self.mode_frame.pack(expand=True, padx=40, pady=40)

        title_lbl = tk.Label(self.mode_frame, text="QUIXO", font=('Segoe UI Black', 36), bg=GameConfig.COULEUR_FOND, fg=GameConfig.COULEUR_PRIMAIRE)
        title_lbl.pack(pady=(0, 20))

        sub_title = tk.Label(self.mode_frame, text="Select Game Mode", font=('Segoe UI', 14), bg=GameConfig.COULEUR_FOND, fg=GameConfig.COULEUR_TEXTE)
        sub_title.pack(pady=(0, 20))

        btn_style = {'font': ('Segoe UI', 14, 'bold'), 'bg': GameConfig.COULEUR_PRIMAIRE, 'fg': GameConfig.COULEUR_TEXTE, 'activebackground': GameConfig.COULEUR_ACCENT, 'activeforeground': GameConfig.COULEUR_TEXTE, 'relief': 'flat', 'cursor': 'hand2', 'pady': 10}

        pvp_btn = tk.Button(self.mode_frame, text="Player vs Player", command=lambda: self.start_game(is_ai=False), **btn_style)
        pvp_btn.pack(pady=10, fill='x')

        pve_btn = tk.Button(self.mode_frame, text="Player vs AI", command=self.show_symbol_selection, **btn_style)
        pve_btn.pack(pady=10, fill='x')

        exit_btn = tk.Button(self.mode_frame, text="Exit", command=self.window.destroy, font=('Segoe UI', 14, 'bold'), bg=GameConfig.COULEUR_ATTENTION, fg=GameConfig.COULEUR_TEXTE, activebackground='#be123c', activeforeground=GameConfig.COULEUR_TEXTE, relief='flat', cursor='hand2', pady=10)
        exit_btn.pack(pady=(20, 10), fill='x')

    def show_symbol_selection(self):
        for widget in self.mode_frame.winfo_children():
            widget.destroy()

        title_lbl = tk.Label(self.mode_frame, text="Choose Your Symbol", font=('Segoe UI Black', 24), bg=GameConfig.COULEUR_FOND, fg=GameConfig.COULEUR_PRIMAIRE)
        title_lbl.pack(pady=(0, 20))

        btn_style = {'font': ('Segoe UI', 14, 'bold'), 'bg': GameConfig.COULEUR_SECONDAIRE, 'fg': GameConfig.COULEUR_TEXTE, 'activebackground': GameConfig.COULEUR_ACCENT, 'activeforeground': GameConfig.COULEUR_TEXTE, 'relief': 'flat', 'cursor': 'hand2', 'pady': 10}

        btn_x = tk.Button(self.mode_frame, text="Play as X (First)", command=lambda: self.start_game(is_ai=True, ai_symbol="O"), **btn_style)
        btn_x.pack(pady=10, fill='x')

        btn_o = tk.Button(self.mode_frame, text="Play as O (Second)", command=lambda: self.start_game(is_ai=True, ai_symbol="X"), **btn_style)
        btn_o.pack(pady=10, fill='x')
        
        back_btn = tk.Button(self.mode_frame, text="← Back", command=self.go_back_to_mode_selection, font=('Segoe UI', 12), bg=GameConfig.COULEUR_FOND, fg=GameConfig.COULEUR_TEXTE, relief='flat', cursor='hand2')
        back_btn.pack(pady=20)

    def go_back_to_mode_selection(self):
        self.mode_frame.destroy()
        self.create_mode_selection_ui()

    def start_game(self, is_ai, ai_symbol="O"):
        self.jeu.is_ai = is_ai
        self.jeu.ai_symbol = ai_symbol
        self.mode_frame.destroy()
        self.create_ui()
        self.update_view()
        self.check_ai_turn()



    def create_ui(self):
        self.game_frame = tk.Frame(self.window, bg=GameConfig.COULEUR_FOND)
        self.game_frame.pack(expand=True)
        
        for row in range(GameConfig.TAILLE_PLATEAU):
            for col in range(GameConfig.TAILLE_PLATEAU):
                pion = tk.Button(self.game_frame, text=' ', font=GameConfig.PION_FONT, height=GameConfig.PION_SIZE, width=GameConfig.PION_WIDTH,
                                 borderwidth=GameConfig.PION_BORDER_WIDTH, relief=GameConfig.PION_RELIEF,
                                 bg=GameConfig.COULEUR_PRIMAIRE, fg=GameConfig.COULEUR_TEXTE)
                pion.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
                pion.config(command=lambda p=pion, r=row, c=col: self.on_pion_click(p, r, c))
        directions = [
            {
                "name": "up",
                "symbol": "↓",
            },
            {
                "name": "down",
                "symbol": "↑",
            },
            {
                "name": "left",
                "symbol": "→",
            },
            {
                "name": "right",
                "symbol": "←",
            }
        ]
        direction_font = ('helvetica', 14, 'bold')

        self.dir_btns = []
        for i, direction in enumerate(directions):
            btn = tk.Button(
                self.game_frame,
                text=direction["symbol"],
                font=direction_font,
                bg=GameConfig.COULEUR_PRIMAIRE,
                fg=GameConfig.COULEUR_TEXTE,
                command=lambda d=direction["name"]: self.on_arrow_click(d)
            )
            btn.grid(row=GameConfig.TAILLE_PLATEAU, column=i, sticky='nsew', padx=15,
                     pady=15)
            self.dir_btns.append(btn)

        self.hide_arrows()

        for i in range(GameConfig.TAILLE_PLATEAU):
            self.game_frame.grid_rowconfigure(i, weight=1)
            self.game_frame.grid_columnconfigure(i, weight=1)

        self.player_turn_label = tk.Label(
            self.game_frame,
            text='Player 1 (X)',
            font=('Segoe UI', 18, 'bold'),
            bg=GameConfig.COULEUR_FOND,
            fg=GameConfig.COULEUR_TEXTE,
            borderwidth=0,
        )
        self.player_turn_label.grid(
            row=GameConfig.TAILLE_PLATEAU + 1,
            column=0,
            columnspan=GameConfig.TAILLE_PLATEAU,
            sticky='ew',
            padx=20,
            pady=15
        )
        self.result_label = tk.Label(
            self.game_frame,
            text='',
            font=('Segoe UI', 20, 'bold'),
            bg=GameConfig.COULEUR_FOND,
            fg=GameConfig.COULEUR_ATTENTION,
            borderwidth=0,
        )
        self.result_label.grid(
            row=GameConfig.TAILLE_PLATEAU + 2,
            column=0,
            columnspan=GameConfig.TAILLE_PLATEAU,
            sticky='ew',
            padx=20,
            pady=10
        )
        self.result_label.grid_forget()

        self.restart_button = tk.Button(self.game_frame, text="Restart game", font=('Segoe UI', 14, 'bold'),
                                        bg=GameConfig.COULEUR_SECONDAIRE, fg=GameConfig.COULEUR_TEXTE,
                                        activebackground=GameConfig.COULEUR_PRIMAIRE, activeforeground=GameConfig.COULEUR_TEXTE,
                                        relief='flat', cursor='hand2', pady=5,
                                        command=self.on_restart_click)
        self.restart_button.grid(row=GameConfig.TAILLE_PLATEAU + 3, column=0, columnspan=GameConfig.TAILLE_PLATEAU,
                                 sticky='ew', padx=10, pady=5)
                                 
        self.exit_button = tk.Button(self.game_frame, text="Exit", font=('Segoe UI', 14, 'bold'),
                                        bg=GameConfig.COULEUR_ATTENTION, fg=GameConfig.COULEUR_TEXTE,
                                        activebackground='#be123c', activeforeground=GameConfig.COULEUR_TEXTE,
                                        relief='flat', cursor='hand2', pady=5,
                                        command=self.window.destroy)
        self.exit_button.grid(row=GameConfig.TAILLE_PLATEAU + 4, column=0, columnspan=GameConfig.TAILLE_PLATEAU,
                                 sticky='ew', padx=10, pady=(5, 10))
        self.window.configure(bg=GameConfig.COULEUR_FOND)

    def on_restart_click(self):
        self.jeu.reset_game()
        # Destroy everything and show mode selection again
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_mode_selection_ui()
        self.current_position = (None, None)
        self.is_selected = False
        self.game_over = False


    def on_arrow_click(self, direction):
        row, col = self.current_position
        self.controller.play_turn(direction, row, col)
        self.hide_arrows()
        self.is_selected = False
        self.check_ai_turn()

    def check_ai_turn(self):
        if not self.game_over and self.jeu.is_ai and self.jeu.joueurs[self.jeu.current_turn].symbol == self.jeu.ai_symbol:
            self.window.config(cursor="watch") # feedback visuel que l'IA réfléchit
            self.window.update()
            self.window.after(self.ai_delay_ms, self.execute_ai_turn)

    def execute_ai_turn(self):
        if self.game_over: return
        import Minimax
        print("IA (" + self.jeu.ai_symbol + ") réfléchit...")
        best_move, score = Minimax.get_best_move(self.jeu, depth=3, alpha=-1000000, beta=1000000, is_maximizing=True, ai_symbol=self.jeu.ai_symbol)
        self.window.config(cursor="") 
        if best_move:
            print(f"IA a choisi {best_move}")
            # Mettre en évidence la case choisie par l'IA une fraction de seconde
            self.game_frame.grid_slaves(row=best_move[1], column=best_move[2])[0].config(bg=GameConfig.COULEUR_ACCENT)
            self.window.update()
            self.window.after(600, lambda: self._finalize_ai_move(best_move))
        else:
            print("L'IA n'a trouvé aucun coup jouable, égalité ou défaite imminente.")
    
    def _finalize_ai_move(self, best_move):
        # Verification que la frame existe toujours (si restart)
        if not hasattr(self, 'game_frame') or not self.game_frame.winfo_exists():
            return
        # On remet la bonne couleur
        self.game_frame.grid_slaves(row=best_move[1], column=best_move[2])[0].config(bg=GameConfig.COULEUR_PRIMAIRE)
        self.controller.play_turn(best_move[0], best_move[1], best_move[2])
        self.check_ai_turn()


    def display_arrows(self):
        row, col = self.current_position
        if row > 0:
            self.dir_btns[0].grid(row=GameConfig.TAILLE_PLATEAU, column=0)
        if row < GameConfig.TAILLE_PLATEAU - 1:
            self.dir_btns[1].grid(row=GameConfig.TAILLE_PLATEAU, column=1)
        if col > 0:
            self.dir_btns[2].grid(row=GameConfig.TAILLE_PLATEAU, column=2)
        if col < GameConfig.TAILLE_PLATEAU - 1:
            self.dir_btns[3].grid(row=GameConfig.TAILLE_PLATEAU, column=3)




    def hide_arrows(self):
        for i in range(len(self.dir_btns)):
            self.dir_btns[i].grid_forget()

    def on_pion_click(self, pion, row, col):
        if self.is_selected or self.game_over:
            return
            
        # Prevent manual play if it's the AI's turn
        if self.jeu.is_ai and self.jeu.joueurs[self.jeu.current_turn].symbol == self.jeu.ai_symbol:
            return

        if self.controller.check_legal("", row, col) and (pion["text"] == ' ' or pion["text"] == self.jeu.joueurs[self.jeu.current_turn].symbol):
            current_player = self.jeu.joueurs[self.jeu.current_turn].symbol
            pion.config(text=current_player, state='disabled')
            self.current_position = (row, col)
            self.display_arrows()
            self.is_selected = True


    def update_view(self):
        for i in range(GameConfig.TAILLE_PLATEAU):
            for j in range(GameConfig.TAILLE_PLATEAU):
                pion = self.jeu.plateau.get_pion(i, j)
                self.game_frame.grid_slaves(row=i, column=j)[0].config(text=pion.symbol(), state='normal')
        current_player = self.jeu.joueurs[self.jeu.current_turn].symbol
        self.player_turn_label.config(text=f'Player {self.jeu.current_turn + 1} ({current_player})')

    def announce_winner(self, winner):
        self.player_turn_label.grid_forget()
        self.result_label.grid(row=GameConfig.TAILLE_PLATEAU + 1, column=0, columnspan=GameConfig.TAILLE_PLATEAU, sticky='ew', padx=10, pady=10)
        self.result_label.config(text=f'Le joueur ({winner}) a gagné !')
        self.game_over = True

    def announce_draw(self):
        self.player_turn_label.grid_forget()
        self.result_label.grid(row=GameConfig.TAILLE_PLATEAU + 1, column=0, columnspan=GameConfig.TAILLE_PLATEAU, sticky='ew', padx=10, pady=10)
        self.result_label.config(text=f'Match nul !')
        self.game_over = True

    def start(self):
        self.window.mainloop()
