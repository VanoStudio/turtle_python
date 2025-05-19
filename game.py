import turtle
import random
import winsound
import threading

# Setup screen
win = turtle.Screen()
win.title("Brick Blast")
win.bgcolor("#0D0D1A")
win.setup(width=900, height=600)
win.tracer(0)

# sfx
def play_bounce_sfx():
    threading.Thread(target=lambda: winsound.Beep(1000, 30)).start()

def play_break_sfx():
    threading.Thread(target=lambda: winsound.Beep(800, 30)).start()

def play_game_over_sfx():
    def sound():
        for i in range(3):
            winsound.Beep(500 - i * 100, 200)
    threading.Thread(target=sound).start()

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("#F5F5DC")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Variables
score = 0
balls = []
bricks = []
game_over_display = None
retry_display = None
skore_display = None
win_text = None
game_running = False
colors_hp = {"#241965": 1, "#653993": 2, "#9F4094": 3, "#F19406": 4}
special_color = "red"

# Ball
def make_ball():
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("yellow")
    ball.penup()
    ball.goto(0, -200)
    ball.dx = random.choice([-10, 10])
    ball.dy = 10
    balls.append(ball)

def create_new_ball(x, y):
    """Buat bola baru di posisi tertentu."""
    new_ball = turtle.Turtle()
    new_ball.speed(0)
    new_ball.shape("circle")
    new_ball.color("yellow")
    new_ball.penup()
    new_ball.goto(x, y)
    new_ball.dx = random.choice([-3, -2, 2, 3])
    new_ball.dy = 4
    balls.append(new_ball)

# Score
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

# Bricks
def create_bricks():
    global bricks
    bricks.clear()
    color_order = list(colors_hp.keys())

    for row, y in enumerate(range(110, 350, 25)):
        special_x = random.choice(range(-400, 410, 50))
        for x in range(-400, 410, 50):
            is_special = (x == special_x)
            warna = special_color if is_special else color_order[row % len(color_order)]
            hp = 1 if is_special else colors_hp[warna]

            brick = turtle.Turtle()
            brick.speed(0)
            brick.shape("square")
            brick.color(warna)
            brick.shapesize(stretch_wid=1, stretch_len=2)
            brick.penup()
            brick.goto(x, y)

            bricks.append({"turtle": brick, "hp": hp, "special": is_special})

# Paddle movement
def paddle_left():
    x = paddle.xcor()
    paddle.setx(max(x - 80, -390))

def paddle_right():
    x = paddle.xcor()
    paddle.setx(min(x + 80, 390))

win.listen()
win.onkeypress(paddle_left, "Left")
win.onkeypress(paddle_right, "Right")

def check_wall_collision(ball):
    if ball.xcor() > 440 or ball.xcor() < -440:
        ball.dx *= -1
        play_bounce_sfx()
    if ball.ycor() > 290:
        ball.dy *= -1
        play_bounce_sfx()

def check_paddle_collision(ball):
    if -230 > ball.ycor() > -250 and paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60:
        ball.dy *= -1
        play_bounce_sfx()

def game_over():
    global game_over_display, retry_display, game_running

    if not game_over_display:
        game_over_display = turtle.Turtle()
        game_over_display.color("red")
        game_over_display.penup()
        game_over_display.hideturtle()
        game_over_display.goto(0, 0)
        game_over_display.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

    if not retry_display:
        retry_display = turtle.Turtle()
        retry_display.color("white")
        retry_display.penup()
        retry_display.hideturtle()
        retry_display.goto(0, -40)
        retry_display.write("Press SPACE to try again", align="center", font=("Arial", 16, "normal"))

    game_running = False

def start_game():
    global score, balls, bricks, game_over_display, retry_display, skore_display, win_text, game_running

    if game_over_display:
        game_over_display.clear()
        game_over_display.hideturtle()
        game_over_display = None

    if retry_display:
        retry_display.clear()
        retry_display.hideturtle()
        retry_display = None

    if win_text:
        win_text.clear()
        win_text.hideturtle()
        win_text = None

    for ball in balls:
        ball.hideturtle()
    balls.clear()

    for brick in bricks:
        brick["turtle"].hideturtle()
    bricks.clear()

    score = 0
    update_score()
    paddle.goto(0, -250)
    make_ball()
    create_bricks()

    game_running = True
    game_loop()

win.onkeypress(start_game, "space")

def game_loop():
    global game_running, score

    if game_running:
        win.update()

        for i in range(len(balls) - 1, -1, -1):
            ball = balls[i]
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

            check_wall_collision(ball)
            check_paddle_collision(ball)

            if ball.ycor() < -290:
                ball.hideturtle()
                balls.pop(i)

        if not balls:
            game_over()
            play_game_over_sfx()
            return

        for i in range(len(bricks) - 1, -1, -1):
            brick = bricks[i]
            for ball in balls:
                if brick["turtle"].distance(ball) < 30:
                    ball.dy *= -1
                    brick["hp"] -= 1
                    play_break_sfx()

                    if brick["hp"] <= 0:
                        if brick["special"]:
                            # Multi-ball effect when hitting a special brick
                            for b in balls[:]:
                                create_new_ball(b.xcor(), b.ycor())

                        brick["turtle"].hideturtle()
                        bricks.pop(i)
                        score += 2 if brick["special"] else 1
                        update_score()
                        break

        if not bricks:
            global win_text
            win_text = turtle.Turtle()
            win_text.color("green")
            win_text.penup()
            win_text.hideturtle()
            win_text.goto(0, 0)
            win_text.write("YOU WIN!", align="center", font=("Arial", 36, "bold"))
            play_game_over_sfx()
            game_running = False
            return

    win.ontimer(game_loop, 10)

start_game()
win.mainloop()
