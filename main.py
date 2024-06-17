import flet as ft
import random

class Hangman(ft.UserControl):
    def __init__(self, page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.words = ["rato", "teclado", "computador", "windows", "monitor", "cd", "word", "apple", "processador"]  # list of words
        self.word = random.choice(self.words)  # select a random word
        self.guesses = []
        self.lives = 8
        self.word_state = ["_"] * len(self.word)
        self.images = ["forca.png", "cabeca.png", "tronco.png", "1braco.png", "2braco.png", "1perna.png", "2perna.png", "olhos.png", "boca.png"]  # list of images

    def build(self):
        self.page.title = "Jogo da Forca"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.update()

        self.word_label = ft.Text(value=" ".join(self.word_state), size=24)
        self.guess_input = ft.TextField(label="Digite uma letra", max_length=1, width=200)
        self.guess_button = ft.ElevatedButton(text="Adivinhar", on_click=self.guess_letter, width=200)
        self.lives_label = ft.Text(value=f"Vidas: {self.lives}", size=18)
        self.result_label = ft.Text(value="", size=24)
        self.image_control = ft.Image(src=self.images[0], width=400, height=400)
        self.restart_button = ft.ElevatedButton(text="Recomeçar", on_click=self.restart_game, width=200, visible=False)

        self.page.add(ft.Column([self.image_control, self.word_label, self.guess_input, self.guess_button, self.lives_label, self.result_label, self.restart_button]))

    def guess_letter(self, e):
        letter = self.guess_input.value
        self.guess_input.value = ""
        if letter in self.guesses:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Você já inseriu esta letra!")))
        elif letter in self.word:
            for i, c in enumerate(self.word):
                if c == letter:
                    self.word_state[i] = letter
            self.word_label.value = " ".join(self.word_state)
            self.guesses.append(letter)
            if "_" not in self.word_state:
                self.show_dialog("Parabéns!", "Você ganhou!", self.restart_game)
        else:
            self.lives -= 1
            self.lives_label.value = f"Vidas: {self.lives}"
            self.image_control.src = self.images[8 - self.lives]
            self.page.update()
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Letra incorreta!")))
            if self.lives == 0:
                self.guess_button.disabled = True
                self.restart_button.visible = True
                self.show_dialog("Game Over", "Você perdeu!", self.restart_game)

        self.page.update()

    def restart_game(self, e):
        self.word = random.choice(self.words)  # select a new random word
        self.guesses = []
        self.lives = 8
        self.word_state = ["_"] * len(self.word)
        self.word_label.value = " ".join(self.word_state)
        self.lives_label.value = f"Vidas: {self.lives}"
        self.result_label.value = ""
        self.image_control.src = self.images[0]
        self.guess_button.disabled = False
        self.restart_button.visible = False
        self.page.update()

    def show_dialog(self, title, message, on_click):
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        title_control = ft.Text(value=title)
        message_control = ft.Text(value=message)

        dialog = ft.AlertDialog(
            modal=True,
            title=title_control,
            content=message_control,
            actions=[
                ft.TextButton("recomeçar", on_click=lambda e: [on_click(e), close_dialog(e)]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        self.page.dialog.open = True

def main(page):
    hangman = Hangman(page)
    hangman.build()

ft.app(main)