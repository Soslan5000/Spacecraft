from Consts_and_funcs import *

pygame.init()

dis = pygame.display.set_mode((dis_width, dis_height))
dis.fill(white)
pygame.display.set_caption('Фазовые портреты')

clock = pygame.time.Clock()

draw_all_phazes_and_axes_and_centers(dis)

pygame.display.update()

game_over = False
paused = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                paused = True
                t = 0
            elif event.key == pygame.K_w:
                paused = False
                dis.fill(white)
                draw_all_phazes_and_axes_and_centers(dis)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                t = 0
                x, y = event.pos
                if x_min_x <= x <= x_max_x and y_min_x <= y <= y_max_x:
                    fi_x, omega_x = change_pos(dis, event, center_x_x, center_y_x)
                elif x_min_y <= x <= x_max_y and y_min_y <= y <= y_max_y:
                    fi_y, omega_y = change_pos(dis, event, center_x_y, center_y_y)
                elif x_min_z <= x <= x_max_z and y_min_z <= y <= y_max_z:
                    fi_z, omega_z = change_pos(dis, event, center_x_z, center_y_z)
                x = mashtab * fi_x + center_x_x
                y = mashtab * omega_x + center_y_x
                pygame.draw.circle(dis, red, (x, y), 2)
                x = mashtab * fi_y + center_x_y
                y = mashtab * omega_y + center_y_y
                pygame.draw.circle(dis, red, (x, y), 2)
                x = mashtab * fi_z + center_x_z
                y = mashtab * omega_z + center_y_z
                pygame.draw.circle(dis, red, (x, y), 2)
                message(dis, 'φx = ' + str(round(fi_x, 6)) + ' рад', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz - dis_height / 2 / 2 + 5)
                message(dis, 'ωx = ' + str(round(omega_x, 6)) + ' рад/c', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz - dis_height / 2 / 2 + 30 + 5)
                message(dis, 'φy = ' + str(round(fi_y, 6)) + ' рад', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz + 5)
                message(dis, 'ωy = ' + str(round(omega_y, 6)) + ' рад/c', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz + 30 + 5)
                message(dis, 'φz = ' + str(round(fi_z, 6)) + ' рад', white, center_x_xyz + 5, center_y_xyz - dis_height / 2 / 2 + 5)
                message(dis, 'ωz = ' + str(round(omega_z, 6)) + ' рад/c', white, center_x_xyz + 5, center_y_xyz - dis_height / 2 / 2 + 30 + 5)
                message(dis, 't = ' + str(round(t, 6)) + 'c', white, center_x_xyz + 5, center_y_xyz + 5)
                pygame.display.update()

    if not paused:
        fi_x, omega_x = draw_trajectory(dis, fi_x, rele_fi_x, omega_x, omega_y, omega_z, rele_om_x, I_x, (I_y-I_z), Mom_x, x_min_x, x_max_x, y_min_x, y_max_x, center_x_x, center_y_x)
        fi_y, omega_y = draw_trajectory(dis, fi_y, rele_fi_y, omega_y, omega_x, omega_z, rele_om_y, I_y, (I_z-I_x), Mom_y, x_min_y, x_max_y, y_min_y, y_max_y, center_x_y, center_y_y)
        fi_z, omega_z = draw_trajectory(dis, fi_z, rele_fi_z, omega_z, omega_x, omega_y, rele_om_z, I_z, (I_x-I_y), Mom_z, x_min_z, x_max_z, y_min_z, y_max_z, center_x_z, center_y_z)
        message(dis, 'φx = ' + str(round(fi_x, 6)) + ' рад', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz - dis_height / 2 / 2 + 5)
        message(dis, 'ωx = ' + str(round(omega_x, 6)) + ' рад/c', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz - dis_height / 2 / 2 + 30 + 5)
        message(dis, 'φy = ' + str(round(fi_y, 6)) + ' рад', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz + 5)
        message(dis, 'ωy = ' + str(round(omega_y, 6)) + ' рад/c', white, center_x_xyz - dis_width / 2 / 2 + 5, center_y_xyz + 30 + 5)
        message(dis, 'φz = ' + str(round(fi_z, 6)) + ' рад', white, center_x_xyz + 5, center_y_xyz - dis_height / 2 / 2 + 5)
        message(dis, 'ωz = ' + str(round(omega_z, 6)) + ' рад/c', white, center_x_xyz + 5, center_y_xyz - dis_height / 2 / 2 + 30 + 5)
        message(dis, 't = ' + str(round(t, 6)) + ' c', white, center_x_xyz+5, center_y_xyz+5)
        input_box = pygame.Rect(50, 50, 140, 32)
        t += dt

    clock.tick()
