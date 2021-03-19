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


alienSpeed = 0.5

# endregion

# region Player
player = turtle.Turtle()
player.shape("spaceship.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)

playerSpeed = 15
# endregion

# region Bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.shapesize(.3, .6)
bullet.speed(0)
bullet.setheading(90)
bullet.setposition(0, -1000)
bullet.hideturtle()
bulletStatus = "ready"

bulletSpeed = 7
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

# region game stats
gamePen = turtle.Turtle()
gamePen.speed(0)
gamePen.color("white")
gamePen.penup()
gamePen.setposition(0, 0)
gamePen.hideturtle()
# endregion

# region Function


def moveLeft():
    x = player.xcor() - playerSpeed
    if x < -280:
        x = -280
    player.setx(x)


def moveRight():
    x = player.xcor() + playerSpeed
    if x > 280:
        x = 280
    player.setx(x)


def fire():
    global bulletStatus
    if bulletStatus == "ready":
        bulletStatus = "fired"
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


def win(msg, score):
    winmsg = "Congratulation!!!\n All alien defeated\n Your score is {}".format(
        score)
    msg.write(winmsg, False, align="center", font=("Times", 20, "normal"))
    msg.showturtle()


def lose(msg, score):
    losemsg = "Game over mate!!!\n Your score is {}".format(score)
    msg.write(losemsg, False, align="center", font=("Times", 20, "normal"))
    msg.showturtle()
# endregion


# region Keyboard blinding
turtle.listen()
turtle.onkeypress(moveLeft, ("Left"))
turtle.onkeypress(moveRight, ("Right"))
turtle.onkey(fire, ("space"))
# endregion

# region Main loop
isRunning = True
while noAliens > 0 and isRunning:
    screen.update()

    # Move all alien
    for alien in aliens:
        x = alien.xcor()+alienSpeed
        alien.setx(x)

        if alien.xcor() == 280 or alien.xcor() == -280:
            # Move alien down
            for alien in aliens:
                alien.sety(alien.ycor()-40)
            # Change direction
            alienSpeed *= -1

        # Check collision btw bullet and alien
        if isCollision(bullet, alien):
            # Reset bullet
            bullet.hideturtle()
            bullet.sety(285)
            # Delete alien
            alien.hideturtle()
            alien.setposition(-2000, 2000)
            noAliens -= 1
            # Update score
            score += 10
            scoreString = "Score: %s" % score
            scorePen.clear()
            scorePen.write(scoreString, False, align="left",
                           font=("Times", 14, "normal"))

        # Check collision btw player and alien
        if isCollision(player, alien):
            isRunning = False
            break
    # Break the game loop
    if isRunning == False:
        break

    # Move bullet
    if bulletStatus == "fired":
        y = bullet.ycor()+bulletSpeed
        bullet.sety(y)
    # Check bullet is inside screen ?
    if bullet.ycor() > 275:
        bulletStatus = "ready"
        bullet.hideturtle()

# Notification result
if noAliens == 0:
    win(gamePen, score)
else:
    lose(gamePen, score)

screen.mainloop()
# endregion
