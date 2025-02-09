import tkinter as tk
import random

LARGEUR = 500  
HAUTEUR = 500  
TAILLE_CASE = 20  # Taille d'une case de la grille
COULEUR_SERPENT = "green"  # Couleur initiale du serpent
COULEUR_POMME = "red"  # Couleur de la nourriture
COULEUR_FOND = "black"  # Couleur de fond du jeu
police = "Comic Sans MS"

class JeuSnake:
    def __init__(self, root, couleur_serpent):
        # Initialise le jeu
        self.root = root
        self.root.title("The Soulless's Snake")
        self.root.resizable(False, False)  # Empêcher le redimensionnement de la fenêtre
        self.canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR, bg=COULEUR_FOND)
        self.canvas.pack()
        
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.pomme = self.placer_pomme()
        self.direction = "Right"
        self.couleur_serpent = couleur_serpent
        
        self.running = True
        self.root.bind("<KeyPress>", self.change_direction)
        self.update()
    
    def placer_pomme(self):
        # Génère une position aléatoire pour la pomme
        x = random.randint(0, (LARGEUR // TAILLE_CASE) - 1) * TAILLE_CASE
        y = random.randint(0, (HAUTEUR // TAILLE_CASE) - 1) * TAILLE_CASE
        return (x, y)
    
    def change_direction(self, event):
        # Change la direction du serpent selon la touche pressée
        directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if event.keysym in directions and directions[event.keysym] != self.direction:
            self.direction = event.keysym
    
    def bouger_serpent(self):
        # Met à jour la position du serpent
        if not self.running:
            return
        
        tete_x, tete_y = self.snake[0]
        
        if self.direction == "Up":
            tete_y -= TAILLE_CASE
        elif self.direction == "Down":
            tete_y += TAILLE_CASE
        elif self.direction == "Left":
            tete_x -= TAILLE_CASE
        elif self.direction == "Right":
            tete_x += TAILLE_CASE
        
        new_tete = (tete_x, tete_y)
        
        # On vérifie les collisions
        if new_tete in self.snake or tete_x < 0 or tete_x >= LARGEUR or tete_y < 0 or tete_y >= HAUTEUR:
            self.running = False
            return
        
        self.snake.insert(0, new_tete)
        
        # On vérifie si le serpent mange une pomme
        if new_tete == self.pomme:
            self.pomme = self.placer_pomme()
        else:
            self.snake.pop()
    
    def afficher(self):
        # Affiche le serpent et la pomme
        self.canvas.delete("all")
        self.canvas.create_oval(self.pomme[0], self.pomme[1], self.pomme[0] + TAILLE_CASE, self.pomme[1] + TAILLE_CASE, fill=COULEUR_POMME)
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + TAILLE_CASE, y + TAILLE_CASE, fill=self.couleur_serpent)
    
    def update(self):
        # Met à jour le jeu à intervalles réguliers
        if self.running:
            self.bouger_serpent()
            self.afficher()
            self.root.after(100, self.update)
        else:
            self.game_over()

    def game_over(self):
        self.canvas.create_text(LARGEUR//2, HAUTEUR//2, text="Game Over", fill="white", font=(police, 24))
        self.canvas.create_text(LARGEUR//2, HAUTEUR//2 + 30, text="Appuyez sur Entrée pour revenir au menu", fill="white", font=(police, 12))
        self.root.bind("<Return>", self.retour_menu)
        
    def retour_menu(self, event):
        self.canvas.pack_forget()  
        self.root.unbind("<Return>") 
        Menu(self.root)

class SelectionCouleur:
    def __init__(self, root, menu):
        # Initialise le menu de sélection des couleurs
        self.root = root
        self.menu = menu
        self.colors = ["white", "silver", "gray", "grey", "red", "maroon", "brown", 
               "orange", "gold", "yellow", "olive", "lime", "green", "teal", 
               "cyan", "blue", "navy", "purple", "magenta", "pink"]
        self.selected_index = self.colors.index("green")
        self.canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR, bg=COULEUR_FOND)
        self.canvas.pack()
        self.afficher_couleur()
        self.root.bind("<KeyPress>", self.navigation_couleurs)
    
    def afficher_couleur(self):
        # Affiche les couleurs disponibles
        self.canvas.delete("all")

        nom_couleur = self.colors[self.selected_index].upper()
        self.canvas.create_text(LARGEUR//2, 70, text=nom_couleur, fill="white", font=(police, 18))

        cols = 4
        rows = (len(self.colors) + cols - 1) // cols
        box_size = 50
        start_x = (LARGEUR - (cols * box_size)) // 2
        start_y = (HAUTEUR - (rows * box_size)) // 2
        
        for index, color in enumerate(self.colors):
            col = index % cols
            row = index // cols
            x = start_x + col * box_size
            y = start_y + row * box_size
            outline = "white" if index == self.selected_index else "black"
            self.canvas.create_rectangle(x, y, x + box_size, y + box_size, fill=color, outline=outline, width=3)
    
    def navigation_couleurs(self, event):
        # Gère la navigation entre les couleurs
        if event.keysym == "Left":
            self.selected_index = (self.selected_index - 1) % len(self.colors)
        elif event.keysym == "Right":
            self.selected_index = (self.selected_index + 1) % len(self.colors)
        elif event.keysym == "Return":
            self.menu.couleur_serpent = self.colors[self.selected_index]
            self.canvas.pack_forget()
            self.menu.canvas.pack()
            self.menu.afficher_menu()
            self.menu.root.bind("<KeyPress>", self.menu.naviguer_menu)
        self.afficher_couleur()

class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("The Soulless's Snake")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR, bg=COULEUR_FOND)
        self.canvas.pack()
        
        self.options = ["LANCER UNE PARTIE", "CHANGER DE COULEUR", "DIFFICULTÉ", "QUITTER"]
        self.current_option = 0
        self.couleur_serpent = "green"
        
        self.afficher_menu()
        self.root.bind("<KeyPress>", self.naviguer_menu)
    
    def afficher_menu(self):
        self.canvas.delete("all")
        self.canvas.create_text(LARGEUR//2, HAUTEUR//4, text="THE SOULLESS'S SNAKE", fill="white", font=(police, 24))
        for index, option in enumerate(self.options):
            color = "yellow" if index == self.current_option else "white"
            self.canvas.create_text(LARGEUR//2, HAUTEUR//2 + index * 30, text=option, fill=color, font=(police, 18))
    
    def naviguer_menu(self, event):
        if event.keysym == "Up":
            self.current_option = (self.current_option - 1) % len(self.options)
        elif event.keysym == "Down":
            self.current_option = (self.current_option + 1) % len(self.options)
        elif event.keysym == "Return":
            if self.current_option == 0:
                self.debut_jeu()
            elif self.current_option == 1:
                self.changer_couleur()
            elif self.current_option == 3:
                self.root.quit()
        self.afficher_menu()
    
    def debut_jeu(self):
        self.canvas.pack_forget()
        JeuSnake(self.root, self.couleur_serpent)
    
    def changer_couleur(self):
        self.canvas.pack_forget()
        SelectionCouleur(self.root, self)

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
