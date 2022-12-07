import pygame
pygame.init()

# Размеры окон
dis_width, dis_height = 800, 800

# RGB цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 214, 120)
blue = (0, 191, 255)

omega_x = 0.1  # Начальная угловая скорость по оси X
omega_y = 0.1  # Начальная угловая скорость по оси Y
omega_z = 0.1  # Начальная угловая скорость по оси Z
fi_x = 0.1  # Начальный угол отклонения по оси X
fi_y = 0.1  # Начальный угол отклонения по оси Y
fi_z = 0.1  # Начальный угол отклонения по оси Z

I_x = 6  # Момент инерции относительно оси X
I_y = 4  # Момент инерции относительно оси Y
I_z = 2  # Момент инерции относительно оси Z

Mom_x = 5  # Момент сил по оси X
Mom_y = 5  # Момент сил по оси Y
Mom_z = 5  # Момент сил по оси Z

q_x = I_x / Mom_x
q_y = I_y / Mom_y
q_z = I_z / Mom_z

t = 0  # Начальный момент времени
dt = 0.01  # Шаг по времени

rele_om_x = 0.1  # Зона нечувствительности для угловой скорости по оси X
rele_om_y = 0.1  # Зона нечувствительности для угловой скорости по оси X
rele_om_z = 0.1  # Зона нечувствительности для угловой скорости по оси X

rele_fi_x = 0.03  # Зона нечувствительности для угла по оси X
rele_fi_y = 0.03  # Зона нечувствительности для угла по оси Y
rele_fi_z = 0.03  # Зона нечувствительности для угла по оси Z

x_min_x, x_max_x, y_min_x, y_max_x = 0, dis_width / 2, 0, dis_height / 2  # Ограничения окна для OX
x_min_y, x_max_y, y_min_y, y_max_y = 0, dis_width / 2, dis_height / 2, dis_height  # Ограничения окна для OX
x_min_z, x_max_z, y_min_z, y_max_z = dis_width / 2, dis_width, 0, dis_height / 2  # Ограничения окна для OX

center_x_x, center_y_x = dis_width / 2 / 2, dis_height / 2 / 2
center_x_y, center_y_y = dis_width / 2 / 2, dis_height / 2 * 3 / 2
center_x_z, center_y_z = dis_width / 2 * 3 / 2, dis_height / 2 / 2
center_x_xyz, center_y_xyz = dis_width / 2 * 3 / 2, dis_height / 2 * 3 / 2

error = 0.01  # Максимальная доля отклонения от фазовой траектории

mashtab = 300  # Масштабирование


def phase_portrait_area(fi, omega, Mom, I=5):
    '''Определяем область фазового портрета, в которой находится КЛА
    LOU - На области слева сверху
    LOD - На области слева снизу
    LU - Область над стационарной траекторией слева от оси OY
    LI - Область внутри стационарной траекторией слева от оси OY
    LD - Область под стационарной траекторией слева от оси OY
    ROU - На области справа сверху
    ROD - На области справа снизу
    RU - Область над стационарной траекторией слева от оси OY
    RI - Область внутри стационарной траекторией слева от оси OY
    RD - Область под стационарной траекторией слева от оси OY'''

    q = I / Mom
    if fi >= 0:
        faze = fi - q * omega ** 2 / 2
        if abs(faze) <= error and omega <= 0:
            if omega >= 0:
                return 'ROU'
            else:
                return 'ROD'
    else:
        faze = fi + q * omega ** 2 / 2
        if abs(faze) <= error and omega >= 0:
            if omega >= 0:
                return 'LOU'
            else:
                return 'LOD'

    if fi >= 0:
        faze = fi - q * omega ** 2 / 2
        if faze > 0:
            return 'RI'
        else:
            if omega >= 0:
                return 'RU'
            else:
                return 'RD'
    else:
        faze = fi + q * omega ** 2 / 2
        if faze < 0:
            return 'LI'
        else:
            if omega >= 0:
                return 'LU'
            else:
                return 'LD'


def draw_phazes(dis, q, mashtab, center_x1, center_y1, a, b, x_min, x_max, y_min, y_max):
    FI = []
    OM = []
    for i in range(a, b):
        om = i / 50
        OM.append(om)
        fi = q * om ** 2 / 2
        FI.append(fi)
    for i in range(len(FI)):
        x = mashtab * FI[i] + center_x1
        y = mashtab * OM[i] + center_y1
        if x_min <= x <= x_max and y_min <= y <= y_max:
            pygame.draw.circle(dis, black, (x, y), 2)


def change_pos(dis, event, center_x, center_y):
    fi, omega = event.pos
    fi = fi / mashtab - center_x / mashtab
    omega = omega / mashtab - center_y / mashtab
    dis.fill(white)
    draw_all_phazes_and_axes_and_centers(dis)
    pygame.display.update()
    return fi, omega


def draw_trajectory(dis, fi, rele_fi, omega, omega2, omega3, rele_om, I, dI, Mom, x_min, x_max, y_min, y_max, center_x, center_y):
    if 0 <= abs(fi) < rele_fi and 0 <= abs(omega) < rele_om:
        omega += dI*omega2*omega3/I * dt
        fi += omega * dt
        x = mashtab * fi + center_x
        y = mashtab * omega + center_y
        if x_min <= x <= x_max and y_min <= y <= y_max:
            pygame.draw.circle(dis, red, (x, y), 2)
        pygame.display.update()
    else:
        area = phase_portrait_area(fi, omega, Mom, I)
        if area in ['LOU', 'LU', 'RU', 'ROU', 'RI']:
            M = -Mom
        else:
            M = Mom
        omega += dI*omega2*omega3/I * dt + M / I * dt
        fi += omega * dt
        x = mashtab * fi + center_x
        y = mashtab * omega + center_y
        if x_min <= x <= x_max and y_min <= y <= y_max:
            pygame.draw.circle(dis, red, (x, y), 2)
        pygame.display.update()
    return fi, omega


def draw_axes(dis, color, dis_width, dis_height):
    center_x1, center_y1 = dis_width / 2 / 2, dis_height / 2 / 2
    center_x2, center_y2 = dis_width / 2 / 2, dis_height / 2 * 3 / 2
    center_x3, center_y3 = dis_width / 2 * 3 / 2, dis_height / 2 / 2

    center_x, center_y = dis_width / 2, dis_height / 2

    pygame.draw.aaline(dis, blue, [center_x, 0], [center_x, dis_height])
    pygame.draw.aaline(dis, blue, [0, center_y], [dis_width, center_y])

    pygame.draw.aaline(dis, color, [center_x1, 0], [center_x1, dis_height])
    pygame.draw.aaline(dis, color, [0, center_y1], [dis_width, center_y1])
    pygame.draw.aaline(dis, color, [center_x3, 0], [center_x3, dis_height])
    pygame.draw.aaline(dis, color, [0, center_y2], [dis_width, center_y2])


def message(dis, msg, color, x, y):
    font_style = pygame.font.Font(r'C:\Windows\Fonts\times.ttf', 20)
    mes = font_style.render(msg, True, black, white)
    dis.blit(mes, [x, y])

def draw_all_phazes_and_axes_and_centers(dis):
    pygame.draw.circle(dis, white, (center_x_x, center_y_x), 2)
    pygame.draw.circle(dis, white, (center_x_y, center_y_y), 2)
    pygame.draw.circle(dis, white, (center_x_z, center_y_z), 2)
    pygame.draw.circle(dis, white, (center_x_xyz, center_y_xyz), 2)

    draw_phazes(dis, q_x, mashtab, center_x_x, center_y_x, -10000, 0, x_min_x, x_max_x, y_min_x, y_max_x)
    draw_phazes(dis, -q_x, mashtab, center_x_x, center_y_x, 0, 10000, x_min_x, x_max_x, y_min_x, y_max_x)

    draw_phazes(dis, q_y, mashtab, center_x_y, center_y_y, -10000, 0, x_min_y, x_max_y, y_min_y, y_max_y)
    draw_phazes(dis, -q_y, mashtab, center_x_y, center_y_y, 0, 10000, x_min_y, x_max_y, y_min_y, y_max_y)

    draw_phazes(dis, q_z, mashtab, center_x_z, center_y_z, -10000, 0, x_min_z, x_max_z, y_min_z, y_max_z)
    draw_phazes(dis, -q_z, mashtab, center_x_z, center_y_z, 0, 10000, x_min_z, x_max_z, y_min_z, y_max_z)

    draw_axes(dis, green, dis_width, dis_height)