from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ball_x = 250
ball_y = 400

ball_dx = 2
ball_dy = -2

radius = 15

paddle_x = 180
paddle_width = 140

score = 0
game_over = False


def drawPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()


def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        return

    xinc = dx / steps
    yinc = dy / steps

    x = x1
    y = y1

    for i in range(steps + 1):
        drawPixel(round(x), round(y))
        x += xinc
        y += yinc


def circlePoints(xc, yc, x, y):
    drawPixel(xc + x, yc + y)
    drawPixel(xc - x, yc + y)
    drawPixel(xc + x, yc - y)
    drawPixel(xc - x, yc - y)
    drawPixel(xc + y, yc + x)
    drawPixel(xc - y, yc + x)
    drawPixel(xc + y, yc - x)
    drawPixel(xc - y, yc - x)


def midpointCircle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        circlePoints(xc, yc, x, y)

        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * x - 2 * y + 5
            y -= 1

        x += 1


def drawBoundary():
    dda(50, 50, 450, 50)
    dda(450, 50, 450, 450)
    dda(450, 450, 50, 450)
    dda(50, 450, 50, 50)


def drawPaddle():
    dda(paddle_x, 70, paddle_x + paddle_width, 70)
    dda(paddle_x, 80, paddle_x + paddle_width, 80)
    dda(paddle_x, 70, paddle_x, 80)
    dda(paddle_x + paddle_width, 70, paddle_x + paddle_width, 80)


def drawText(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)
    drawBoundary()

    glColor3f(0, 1, 1)
    drawPaddle()

    glColor3f(1, 0.5, 0)
    midpointCircle(ball_x, ball_y, radius)

    glColor3f(1, 1, 0)
    drawText(60, 470, "Score: " + str(score))

    if game_over:
        glColor3f(1, 0, 0)
        drawText(180, 250, "GAME OVER")
        drawText(150, 220, "Press R to Restart")

    glFlush()


def update(value):
    global ball_x, ball_y
    global ball_dx, ball_dy
    global score
    global game_over

    if game_over:
        return

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x + radius >= 450:
        ball_dx = -ball_dx

    if ball_x - radius <= 50:
        ball_dx = -ball_dx

    if ball_y + radius >= 450:
        ball_dy = -ball_dy

    if 80 <= ball_y - radius <= 90:
        if paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_dy = abs(ball_dy)
            score += 1

    if ball_y < 40:
        game_over = True
        glutPostRedisplay()
        return

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def keyboard(key, x, y):
    global paddle_x
    global ball_x, ball_y
    global ball_dx, ball_dy
    global score, game_over

    if key == b'a':
        paddle_x -= 20

    if key == b'd':
        paddle_x += 20

    if key == b'r' and game_over:
        ball_x = 250
        ball_y = 400
        ball_dx = 2
        ball_dy = -2
        score = 0
        game_over = False
        glutTimerFunc(16, update, 0)

    if paddle_x < 60:
        paddle_x = 60

    if paddle_x + paddle_width > 440:
        paddle_x = 440 - paddle_width

    glutPostRedisplay()


def init():
    glClearColor(0.05, 0.05, 0.1, 1)
    gluOrtho2D(0, 500, 0, 500)
    glPointSize(2)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Final Paddle Ball Game")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(16, update, 0)

glutMainLoop()