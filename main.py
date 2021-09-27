import tkinter as tk
import random as rand

# const variables
NUM_CARD = 26
NUM_IMG = 14
CARD_WIDTH = 120
CARD_HEIGHT = 168
CARD_FACE = 1
CARD_BACK = 0
CARD_NONE = 2
FNT = ('Times New Roman', 36)
EMPTY = 0
RESET = 0

# variables
phase = 0
timer = 0
selected_card1 = 0
selected_card2 = 0
player_card = 0
computer_card = 0

# lists
img = [None] * NUM_IMG
card = [0] * NUM_CARD
face = [0] * NUM_CARD
memory = [0] * NUM_CARD
process = {'start_game': 0,
           'player_turn1': 1,
           'player_turn2': 2,
           'judge_player': 3,
           'computer_turn1': 4,
           'computer_turn2': 5,
           'judge_computer': 6,
           'end_game': 7}


# functions
def game_progress():
    global phase, timer, selected_card1, selected_card2, player_card, computer_card
    timer += 1
    draw_card()
    if phase == process['start_game'] and (timer % 10) < 5:
        cvs.create_text(780, 580, text='Click to start!', fill='green', font=FNT)
    elif process['player_turn1'] <= phase <= process['judge_player']:
        cvs.create_rectangle(840, 60, 960, 200, fill='blue', width=0)
    elif process['computer_turn1'] <= phase <= process['judge_computer']:
        cvs.create_rectangle(840, 260, 960, 400, fill='red', width=0)
    cvs.create_text(900, 100, text='YOU', fill='silver', font=FNT)
    cvs.create_text(900, 160, text=player_card, fill='white', font=FNT)
    cvs.create_text(900, 300, text='COM', fill='silver', font=FNT)
    cvs.create_text(900, 360, text=computer_card, fill='white', font=FNT)

    if phase == process['judge_player'] and timer == 10:  # 二枚目をめくってから15回ループ後に判定の処理をさせる
        if card[selected_card1] == card[selected_card2]:
            face[selected_card1] = CARD_NONE
            face[selected_card2] = CARD_NONE
            player_card += 2
            phase = process['player_turn1']
            if player_card + computer_card == NUM_CARD:
                phase = process['end_game']
        else:
            face[selected_card1] = CARD_BACK
            face[selected_card2] = CARD_BACK
            memory[selected_card1] = card[selected_card1]
            memory[selected_card2] = card[selected_card2]
            phase = process['computer_turn1']
        timer = RESET

    elif phase == process['computer_turn1'] and timer == 5:
        selected_card1 = rand.randint(0, NUM_CARD-1)
        while face[selected_card1] != CARD_BACK:  # コンピューターが裏向きのカードを探す
            selected_card1 = (selected_card1 + 1) % NUM_CARD
        face[selected_card1] = CARD_FACE
        phase = process['computer_turn2']
        timer = RESET

    elif phase == process['computer_turn2'] and timer == 5:
        selected_card2 = rand.randint(0, NUM_CARD - 1)
        while face[selected_card2] != CARD_BACK:  # コンピューターが裏向きのカードを探す
            selected_card2 = (selected_card2 + 1) % NUM_CARD
        for index in range(NUM_CARD):
            if memory[index] == card[selected_card1] and face[index] == CARD_BACK:
                selected_card2 = index
        face[selected_card2] = CARD_FACE
        phase = process['judge_computer']
        timer = RESET

    elif phase == process['judge_computer'] and timer == 10:
        if card[selected_card1] == card[selected_card2]:
            face[selected_card1] = CARD_NONE
            face[selected_card2] = CARD_NONE
            computer_card += 2
            phase = process['computer_turn1']
            if player_card + computer_card == NUM_CARD:
                phase = process['end_game']
        else:
            face[selected_card1] = CARD_BACK
            face[selected_card2] = CARD_BACK
            memory[selected_card1] = card[selected_card1]
            memory[selected_card2] = card[selected_card2]
            phase = process['player_turn1']
        timer = RESET

    elif phase == process['end_game']:
        if player_card > computer_card:
            cvs.create_text(780, 580, text="Player win!", fill='skyblue', font=FNT)
        elif computer_card > player_card:
            cvs.create_text(780, 580, text="Computer win!", fill='pink', font=FNT)
        if timer == 20:
            phase = process['start_game']

    root.after(200, game_progress)


def draw_card():
    cvs.delete('all')
    for number in range(NUM_CARD):
        x = (number % 7) * CARD_WIDTH + (CARD_WIDTH / 2)
        y = int(number / 7) * CARD_HEIGHT + (CARD_HEIGHT / 2)
        if face[number] == CARD_BACK:
            cvs.create_image(x, y, image=img[CARD_BACK])
        if face[number] == CARD_FACE:
            cvs.create_image(x, y, image=img[card[number]])


def shuffle_card():
    for i in range(NUM_CARD):
        card[i] = 1 + (i % 13)
        face[i] = CARD_BACK
        memory[i] = RESET
    shuffle_amount = 100
    for i in range(shuffle_amount):
        r1 = rand.randint(0, 12)
        r2 = rand.randint(13, 25)
        card[r1], card[r2] = card[r2], card[r1]


def flip_card(e):
    global phase, timer, selected_card1, selected_card2, player_card, computer_card
    origin_point = 0
    max_column = 6
    max_row = 3
    column = int(e.x/CARD_WIDTH)
    row = int(e.y/CARD_HEIGHT)

    if phase == process['start_game']:
        shuffle_card()
        player_card = EMPTY
        computer_card = EMPTY
        phase = process['player_turn1']
        return

    if origin_point <= column <= max_column and origin_point <= row <= max_row:
        number = column + row * 7   # 何枚目のカードかを指定
        if number >= NUM_CARD:
            return
        if face[number] == CARD_BACK:
            if phase == process['player_turn1']:
                face[number] = CARD_FACE
                selected_card1 = number
                phase = process['player_turn2']
            elif phase == process['player_turn2']:
                face[number] = CARD_FACE
                selected_card2 = number
                phase = process['judge_player']
                timer = RESET


# main
root = tk.Tk()
root.title('Memory')
root.resizable(False, False)
root.bind('<Button>', flip_card)
cvs = tk.Canvas(width=CARD_WIDTH*8, height=CARD_HEIGHT*4, bg='black')
cvs.pack()
for file in range(NUM_IMG):
    img[file] = tk.PhotoImage(file=f'card/{file}.png')
game_progress()
root.mainloop()
