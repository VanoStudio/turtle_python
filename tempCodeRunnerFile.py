def game_over():
    global game_over_display, text_Try_again

    # Jika sudah ada game_over_display, dan text_try_again, jangan buat lagi
    if game_over_display:
        return
    
    if text_Try_again:
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

def start_game():
    global score, balls, bricks, game_over_display, skore_display
    
    # Bersihkan tampilan "Game Over" jika ada
    if game_over_display:
        game_over_display.clear()
        game_over_display.hideturtle()
        game_over_display = None
    
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

win.listen()
win.onkeypress(start_game,"space")

start_game()


#Main game loop
while True:
    win.update()
    time.sleep(0.01)  #Reduce CPU
    
    #Move all balls
    for ball in balls[:]:
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        check_wall_collision(ball)
        check_paddle_collision(ball)

        #kalo jatoh
        if ball.ycor() < -290:
            ball.hideturtle()
            balls.remove(ball)

            
            
            if len(balls) == 0:
                game_over()
                play_game_over_sfx()
                break
                

    #Brick collision
    for brick in bricks[:]:
        for ball in balls[:]:
            if brick["turtle"].distance(ball) < 30:
                #nentuin nabrak mana
                if abs(ball.xcor() - brick["turtle"].xcor()) > abs(ball.ycor() - brick["turtle"].ycor()):
                    ball.dx *= -1  #horizontal collision
                else:
                    ball.dy *= -1  #vertical collision
                
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

    #kalo menang
    if len(bricks) == 0:
        win_text = turtle.Turtle()
        win_text.speed(0)
        win_text.color("green")
        win_text.penup()
        win_text.hideturtle()
        win_text.goto(0, 0)
        win_text.write("YOU WIN!", align="center", font=("Arial", 36, "bold"))
        play_game_over_sfx()
        break

win.mainloop()