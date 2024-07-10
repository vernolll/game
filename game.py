import tkinter
import random

def move_wrap(canvas, obj, move):
    canvas.move(obj, move[0], move[1])
    x, y = canvas.coords(obj)
    if x + move[0] <= 600:
        canvas.move(obj, 600, 0)
    if x >= 0:
        canvas.move(obj, -600, 0)
    if y >= 0:
        canvas.move(obj, 0, -600)
    if y + move[1] <= 600:
        canvas.move(obj, 0, 600)

def key_pressed(event):
    global stop_counter
    if event.keysym == 'Up':
        move_wrap(canvas, player, (0, -step))
    if event.keysym == 'Down':
        move_wrap(canvas, player, (0, step))
    if event.keysym == 'Left':
        move_wrap(canvas, player, (-step, 0))
    if event.keysym == 'Right':
        move_wrap(canvas, player, (step, 0))

    for enemy in enemies:
        if stop_counter == 0:
            move = move_towards(enemy)
            move_wrap(canvas, enemy, move)
        else:
            stop_counter -= 1
            move_wrap(canvas, enemy, (0, 0))

    check_move()

def check_move():
    global stop_counter
    if canvas.coords(player) == canvas.coords(exit_):
        label.config(text="You Win!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="You Lose!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e):
            label.config(text="You Lose!")
            master.bind("<KeyPress>", do_nothing)
    for s in stars:
        if canvas.coords(player) == canvas.coords(s):
            label.config(text="You pick up the star!")
            stop_counter = 9
            stars.remove(s)
            canvas.delete(s)

def do_nothing():
    pass

def move_towards(enemy):
    enemy_x, enemy_y = canvas.coords(enemy)
    player_x, player_y = canvas.coords(player)
    if enemy_x < player_x:
        return (step, 0)
    elif enemy_x > player_x:
        return (-step, 0)
    elif enemy_y < player_y:
        return (0, step)
    elif enemy_y > player_y:
        return (0, -step)
    else:
        return (0, 0)

def check_positions():
    player_coords = canvas.coords(player)
    exit_coords = canvas.coords(exit_)
    if player_coords == exit_coords:
        return False

    for fire in fires:
        fire_coords = canvas.coords(fire)
        if player_coords == fire_coords or exit_coords == fire_coords:
            return False

    for enemy in enemies:
        enemy_coords = canvas.coords(enemy)
        if player_coords == enemy_coords or exit_coords == enemy_coords:
            return False

    for enemy in enemies:
        for fire in fires:
            fire_coords = canvas.coords(fire)
            enemy_coords = canvas.coords(enemy)
            if fire_coords == enemy_coords:
                return False

    for star in stars:
        star_coords = canvas.coords(star)
        if star_coords == player_coords or exit_coords == star_coords:
            return False

    for star in stars:
        for fire in fires:
            star_coords = canvas.coords(star)
            fire_coords = canvas.coords(fire)
            if fire_coords == star_coords:
                return False

    for star in stars:
        for enemy in enemies:
            star_coords = canvas.coords(star)
            enemy_coords = canvas.coords(enemy)
            if enemy_coords == star_coords:
                return False

    return True

def prepare_and_start():
    global player, exit_, fires, enemies, stars, stop_counter
    canvas.delete("all")
    stop_counter = 0
    player_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
    player = canvas.create_image(player_pos, image=player_pic, anchor='nw')
    exit_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
    exit_ = canvas.create_image(exit_pos, image=exit_pic, anchor='nw')
    N_STARS = 2
    stars = []
    for i in range(N_STARS):
        star_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        star = canvas.create_image(star_pos, image=star_pic, anchor='nw')
        stars.append(star)
    N_FIRES = 6
    fires = []
    for i in range(N_FIRES):
        fire_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        fire = canvas.create_image(fire_pos, image=fire_pic, anchor='nw')
        fires.append(fire)
    N_ENEMIES = 3
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append(enemy)
    while not check_positions():
        prepare_and_start()
    label.config(text="Find the Exit!")
    master.bind("<KeyPress>", key_pressed)

master = tkinter.Tk()
master.title("Game")
player_pic = tkinter.PhotoImage(file="images/doctor.gif")
exit_pic = tkinter.PhotoImage(file="images/exit.gif")
fire_pic = tkinter.PhotoImage(file="images/fire.gif")
enemy_pic = tkinter.PhotoImage(file="images/monster.gif")
star_pic = tkinter.PhotoImage(file="images/star.gif")
step = 60
N_X = 10
N_Y = 10
label = tkinter.Label(master, text="Find the Exit")
label.pack()
canvas = tkinter.Canvas(master, bg='pink', height=N_X * step, width = N_Y * step)
canvas.pack()
restart = tkinter.Button(master, text="Restart", command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()