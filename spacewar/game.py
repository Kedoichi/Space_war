import turtle
import os
import math as m

# region Prepair screen

screen = turtle.Screen()
screen.setup(650, 650)
screen.bgcolor("black")
screen.title("Space war")
screen.tracer(0)

# Register shape
screen.register_shape("alien.gif")
screen.register_shape("spaceship.gif")

# endregion

# region Draw border

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.setposition(-300, -300)
pen.pendown()
pen.pensize(3)
# Draw a square
for side in range(4):
    pen.forward(600)
    pen.left(90)
pen.hideturtle()

# endregion

# region Alien

# create list of aliens
noAliens = 30
aliens = []

alienStartX = -200
alienStartY = 250
countAlien = 0

for alien in range(noAliens):
    aliens.append(turtle.Turtle())

for alien in aliens:
    alien.shape("alien.gif")
    alien.penup()
    alien.speed(0)
    x = alienStartX + (40*countAlien)
    y = alienStartY
    alien.setposition(x, y)
    countAlien += 1
    if countAlien == 10:
        alienStartY -= 50
        countAlien = 0


alien_speed = 0.5

# endregion

# region Player
player = turtle.Turtle()
player.shape("spaceship.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)

player_speed = 15
# endregion

# region Bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.shapesize(.3, .6)
bullet.speed(0)
bullet.setheading(90)
bullet.hideturtle()
bullet_status = "ready"

bullet_speed = 7
# endregion

# region Function


def move_left():
    x = player.xcor() - player_speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor() + player_speed
    if x > 280:
        x = 280
    player.setx(x)


def fire():
    global bullet_status
    if bullet_status == "ready":
        bullet_status = "fired"
        x = player.xcor()
        y = player.ycor()+10
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(obj1, obj2):
    distance = m.sqrt(m.pow(obj1.xcor()-obj2.xcor(), 2) +
                      m.pow(obj1.ycor()-obj2.ycor(), 2))
    if distance < 20:
        return True
    return False

# endregion


# region Keyboard blinding
turtle.listen()
turtle.onkeypress(move_left, ("Left"))
turtle.onkeypress(move_right, ("Right"))
turtle.onkey(fire, ("space"))
# endregion

# region score
score = 0
scoreString = "Score: %s" % score
scorePen = turtle.Turtle()
scorePen.speed(0)
scorePen.color("white")
scorePen.penup()
scorePen.setposition(-290, 280)
scorePen.write(scoreString, False, align="left", font=("Times", 14, "normal"))
scorePen.hideturtle()
# endregion

# region Main loop
while True:
    screen.update()

    # Move all alien
    for alien in aliens:
        x = alien.xcor()+alien_speed
        alien.setx(x)

        if alien.xcor() == 280 or alien.xcor() == -280:
            # Move alien down
            for alien in aliens:
                alien.sety(alien.ycor()-40)
            # Change direction
            alien_speed *= -1

        # Check collision btw bullet and alien
        if isCollision(bullet, alien):
            #Reset bullet
            bullet.hideturtle()
            bullet.sety(285)
            #Delete alien
            alien.hideturtle()
            alien.setposition(-2000,2000)
            noAliens -= 1
            #Update score
            score += 10
            scoreString = "Score: %s" % score
            scorePen.clear()
            scorePen.write(scoreString, False, align="left",
                           font=("Times", 14, "normal"))

        # Check collision btw bullet and alien
        if isCollision(player, alien):
            bullet.hideturtle()
            alien.hideturtle()
            print('Game over')
            break

    # Move bullet
    if bullet_status == "fired":
        y = bullet.ycor()+bullet_speed
        bullet.sety(y)
    # Check bullet is inside screen ?
    if bullet.ycor() > 275:
        bullet_status = "ready"
        bullet.hideturtle()

screen.mainloop()
# endregion
