import turtle
import random
import winsound
import time

#Setup screen
win = turtle.Screen()
win.title("Brick Blast")
win.bgcolor("#0D0D1A")
win.setup(width=900, height=600)
win.tracer(0)

#sfx
def play_bounce_sfx():
    winsound.Beep(1000, 30)

def play_break_sfx():
    winsound.Beep(800, 30)

def play_game_over_sfx():
    for i in range(3):
        winsound.Beep(500 - i*100, 200)

#Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("#F5F5DC")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

#Variables
score = 0
balls = []
bricks = []
game_over_display = None
skore_display = None
game_running = True
colors_hp = {"#241965": 1, "#653993": 2, "#9F4094": 3, "#F19406": 4}

#Ball
def make_ball():
    global ball
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("yellow")
    ball.penup()
    ball.goto(0, -200)
    ball.dx = 4
    ball.dy = 4

#multi ball
    balls.append(ball)

def create_new_ball(x, y):
    new_ball = turtle.Turtle()
    new_ball.speed(0)
    new_ball.shape("circle")
    new_ball.color("yellow")
    new_ball.penup()
    new_ball.goto(x, y)
    new_ball.dx = random.choice([-3, -2, 2, 3])
    new_ball.dy = 4
    balls.append(new_ball)
    return new_ball

#Score
def update_score():
    global skore_display
    if not skore_display:
        skore_display = turtle.Turtle()
        skore_display.hideturtle()
        skore_display.penup()
        skore_display.goto(-420, -50)
        skore_display.color("#F5F5DC")
    
    skore_display.clear()
    skore_display.write(f"Score: {score}", font=("Arial", 14, "bold"))

#Bricks
def create_bricks():
    global bricks
    bricks = []
    colors_hp = {"#241965":1, "#653993":2, "#9F4094":3, "#F19406":4}
    special_color = "red"
    color_order = list(colors_hp.keys())

    for row, y in enumerate(range(110, 350, 25)):
        special_x = random.choice(range(-400, 410, 50))
        
        for x in range(-400, 410, 50):
            is_special = (x == special_x)
            
            if is_special:
                brick = turtle.Turtle()
                brick.speed(0)
                brick.shape("square")
                brick.color(special_color)
                brick.shapesize(stretch_wid=1, stretch_len=2)
                brick.penup()
                brick.goto(x, y)
                bricks.append({"turtle": brick, "hp": 1, "special": True})
            else:
                warna = color_order[row % len(color_order)]
                brick = turtle.Turtle()
                brick.speed(0)
                brick.shape("square")
                brick.color(warna)
                brick.shapesize(stretch_wid=1, stretch_len=2)
                brick.penup()
                brick.goto(x, y)
                bricks.append({"turtle": brick, "hp": colors_hp[warna], "special": False})

#Paddle movement
def paddle_left():
    x = paddle.xcor()
    x -= 80
    paddle.setx(max(x, -390))

def paddle_right():
    x = paddle.xcor()
    x += 80
    paddle.setx(min(x, 390))

win.listen()
win.onkeypress(paddle_left, "Left")
win.onkeypress(paddle_right, "Right")

#deteksi tabrakan:
#wall
def check_wall_collision(ball):
    if ball.xcor() > 440 or ball.xcor() < -440:
        ball.dx *= -1
        play_bounce_sfx()
    if ball.ycor() > 290:
        ball.dy *= -1
        play_bounce_sfx()
#paddle
def check_paddle_collision(ball):
    if (-230 > ball.ycor() > -250 and 
        paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60):
        relative_x = (ball.xcor() - paddle.xcor()) / 60
        ball.dx = relative_x * 8
        ball.dy = abs(ball.dy)
        ball.sety(-230)
        play_bounce_sfx()

def game_over():
    global game_over_display,text_Try_again

    # Jika sudah ada game_over_display, dan text_try_again, jangan buat lagi
    if game_over_display:
        return
    


    game_over_display = turtle.Turtle()
    game_over_display.speed(0)
    game_over_display.color("red")
    game_over_display.penup()
    game_over_display.hideturtle()
    game_over_display.goto(0, 0)
    game_over_display.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

    text_Try_again = turtle.Turtle()
    text_Try_again.color("white")
    text_Try_again.penup()
    text_Try_again.hideturtle()
    text_Try_again.goto(0, -20)
    text_Try_again.write('Press "Space" to try again', align="center", font=("Arial", 15, "normal"))
    game_running = False

def start_game():
    global score, balls, bricks, game_over_display, skore_display,text_Try_again,game_running
    
    if 'text_Try_again' not in globals():
        text_Try_again = None
    # Bersihkan tampilan "Game Over" jika ada
    if game_over_display:
        game_over_display.clear()
        game_over_display.hideturtle()
        game_over_display = None

    if text_Try_again:
        text_Try_again.clear()
        text_Try_again.hideturtle()
        text_Try_again = None
    
    # Hapus semua bola dari layar
    for ball in balls:
        ball.hideturtle()
    balls.clear()

    # Reset skor
    score = 0

    # Reset paddle
    paddle.goto(0, -250)

    # Buat bola baru di posisi awal
    make_ball()

    # Hapus semua brick dan buat ulang
    for brick in bricks:
        brick["turtle"].hideturtle()
    bricks.clear()
    create_bricks()

    # Update score display
    if skore_display:
        skore_display.clear()
    update_score()
    game_running = True

win.listen()
win.onkeypress(start_game,"space")

start_game()


#Main game loop
def game_loop():
    global game_running

    if game_running:
        win.update()

        # Move all balls
        for ball in balls[:]:
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

            check_wall_collision(ball)
            check_paddle_collision(ball)

            # kalo jatoh
            if ball.ycor() < -290:
                ball.hideturtle()
                balls.remove(ball)

                if len(balls) == 0:
                    game_over()
                    play_game_over_sfx()
                    game_running = False
                    return  # Hentikan game loop untuk sementara

        # Brick collision
        for brick in bricks[:]:
            for ball in balls[:]:
                if brick["turtle"].distance(ball) < 30:
                    # nentuin nabrak mana
                    if abs(ball.xcor() - brick["turtle"].xcor()) > abs(ball.ycor() - brick["turtle"].ycor()):
                        ball.dx *= -1  # horizontal collision
                    else:
                        ball.dy *= -1  # vertical collision

                    brick["hp"] -= 1
                    play_break_sfx()

                    if brick["hp"] <= 0:
                        if brick["special"]:
                            current_balls = balls[:]
                            for b in current_balls:
                                create_new_ball(b.xcor(), b.ycor())

                        brick["turtle"].hideturtle()
                        bricks.remove(brick)
                        score += 2 if brick["special"] else 1
                    else:
                        brick["turtle"].color(next(c for c, h in colors_hp.items() if h == brick["hp"]))

                    skore_display.clear()
                    skore_display.write(f"Score: {score}", font=("Arial", 16, "bold"))
                    break

        # kalo menang
        if len(bricks) == 0:
            win_text = turtle.Turtle()
            win_text.speed(0)
            win_text.color("green")
            win_text.penup()
            win_text.hideturtle()
            win_text.goto(0, 0)
            win_text.write("YOU WIN!", align="center", font=("Arial", 36, "bold"))
            play_game_over_sfx()
            game_running = False
            return

    # Panggil ulang game loop setelah 10ms
    win.ontimer(game_loop, 10)

# Mulai game loop pertama kali
game_loop()

win.mainloop()


