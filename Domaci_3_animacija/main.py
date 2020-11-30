from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import numpy as np
import ppgr_domaci_3 as funkcije

# Inicijalizacija potrebnih indikatora
TIMER_INTERVAL = 20
time = 25
t = 0
TIMER_ID = 0

# Indikator da li se animacija izvrsava
animation_ongoing = False
m = []
m1 = []
m2 = []

# Funkcija koja racuna ugao izmedju dva kvaterniona
def angle_between_Q(q1, q2):
    cos = list(map(lambda x, y: x*y, q1, q2))
    z = 0
    for i in range(len (cos)):
        z = cos[i] + z

    if z < 0:
        q1 = list(map(lambda x: (-1)*x, q1))
        # cos = (-1)*cos

    angle = math.acos(z)

    return angle, q1, q2, z

def slerp(q1, q2, tm, t):
    angle, q1m, q2m, cos = angle_between_Q(q1, q2)
    if cos <=0.95:
        im = math.sin(angle)
        m1 = math.sin(angle*(1-t/tm))/im
        m2 = math.sin(angle*t/tm)/im

        res = list(map(lambda x, y: m1*x + m2*y, q1m, q2m))
    else:
        res = q1m

    return res

# Pocetni i krajnji uglovi
angles1 = [math.pi / 2, 2 * math.pi / 3, math.pi / 4]
angles2 = [math.pi / 5, math.pi / 4, 2 * math.pi / 3]

# Koordinate centra startnog polozaja
center1 = [9, -5, -7]
# Koordinate centra zavrsnog polozaja
center2 = [-1, 6, -4]

# Funkcija koja kreira kvaternion
def make_Q(angles):
    A = funkcije.Euler2A(angles[0], angles[1], angles[2])
    p, angle = funkcije.AxisAngle(A)
    return funkcije.AngleAxis2Q(p, angle)

def main():
    # Inicijalizacija glavnog prozora
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)

    glutCreateWindow("PPGR_Domaci_3(SLERP animacija)")

    glLineWidth(1)

    # Registruju se komande sa tastature
    glutKeyboardFunc(keyboard)

    glutDisplayFunc(display)

    # Postavlja se boja pozadine
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

    if animation_ongoing:
        glutTimerFunc(TIMER_INTERVAL, timer, TIMER_ID)

    global m1
    global m2

    m1 = make_Q(angles1)
    m2 = make_Q(angles2)

    glutMainLoop()
    return


# Funkcija za crtanje koordinatnog sistema
def draw_axis(size):
    glBegin(GL_LINES)

    glColor3f(255, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(size, 0, 0)

    glColor3f(0, 255, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, size, 0)

    glColor3f(0, 0, 255)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, size)

    glEnd()

# Iscrtavanje proizvoljnog polozaja position sa uglovima angles
def draw_position(position, angles):
    glPushMatrix()

    glColor3f(255, 255, 255)
    glTranslatef(position[0], position[1], position[2])

    A = funkcije.Euler2A(angles[0], angles[1], angles[2])
    p, angle = funkcije.AxisAngle(A)

    glRotatef(angle / math.pi * 180, p[0], p[1], p[2])

    draw_axis(3)

    glPopMatrix()

# Pokretanje animacije preko tastature(s pokreni, g stani)
def keyboard(key, x, y):
    global animation_ongoing

    if ord(key) == 27:
        sys.exit(0)

    if ord(key) == ord('p'):
        if not animation_ongoing:
            glutTimerFunc(TIMER_INTERVAL, timer, TIMER_ID)
            animation_ongoing = True
        animation_ongoing = True

    if ord(key) == ord('o'):
        animation_ongoing = False

# Timer f-ja
def timer(value):
    # Ukoliko nije u pitanju ovaj konkretan tajmer prekini izvrsavanje
    if value != TIMER_ID:
        return

    global t
    global time
    global animation_ongoing
    global m

    # brzina kretanja objekta
    t += 0.1

    # kada stigne do zadate tacke animacija staje
    if t >= time:
        t = 0
        animation_ongoing = False
        return

    glutPostRedisplay()

    if animation_ongoing:
        glutTimerFunc(TIMER_INTERVAL, timer, TIMER_ID)


def animate():
    global m
    global t
    global time

    glPushMatrix()
    glColor3f(255, 255, 255)

    position = []

    position.append((1 - t / time) * center1[0] + (t / time) * center2[0])
    position.append((1 - t / time) * center1[1] + (t / time) * center2[1])
    position.append((1 - t / time) * center1[2] + (t / time) * center2[2])

    glTranslatef(position[0], position[1], position[2])

    m = slerp(m1, m2, time, t)

    p, angle = funkcije.Q2AngleAxis(m)

    glRotatef(angle / math.pi * 180, p[0], p[1], p[2])

    glLineWidth(1)
    draw_axis(3)

    glPopMatrix()

def display():
    global m

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    window_width = 700
    window_height = 600

    glViewport(0, 0, window_width, window_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(window_width) / window_height, 1, 250)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # tacka pogleda
    gluLookAt(15, 10, 17, 0, 0, 0, 0, 1, 0)

    draw_axis(15)

    # Iscrtava sa pocetna pozicija
    draw_position(center1, angles1)
    # Iscrtava se krajnja pozicija
    draw_position(center2, angles2)

    # Pokrece se animacija
    animate()

    glutSwapBuffers()

if __name__ == '__main__':
    main()