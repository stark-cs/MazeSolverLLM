from collections import Counter

import numpy as np
import pygame


def to_id(row, col) -> int:
    return row * 4 + col


def to_loc(id) -> tuple[int, int]:
    return np.unravel_index(id, (4, 4))


def run_pygame():
    # 初始化pygame
    pygame.init()

    # 设置窗口大小
    screen_width, screen_height = 640, 640
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 设置颜色
    white = (255, 255, 255)
    black = (0, 0, 0)

    # 设置颜色
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)  # 绿色
    blue = (0, 0, 128)  # 蓝色

    # 棋盘大小
    board_size = 4
    wall_thickness = 5

    # 棋盘格子的宽度和高度
    cell_width_height = screen_width // board_size

    # 定义不需要绘制线条的格子位置 wall
    wall_lines = [(0, 1), (1, 5), (2, 3), (6, 10), (7, 11), (8, 9), (9, 13), (13, 14), (14, 15)]

    # 设置字体和大小
    font = pygame.font.Font(None, 72)  # 选择一个合适的字体和大小

    text_start = font.render("Start", True, blue)
    text_start_rect = text_start.get_rect()
    text_start_rect.center = (cell_width_height / 2, cell_width_height / 2)  # 将文本居中

    text_end = font.render("End", True, green)
    text_end_rect = text_end.get_rect()
    text_end_rect.center = (screen_width - cell_width_height / 2, screen_height - cell_width_height / 2)  # 将文本居中

    # 游戏循环标志
    running = True

    # 游戏主循环
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 填充屏幕背景色
        screen.fill(white)

        # 绘制边框
        pygame.draw.rect(screen, black, (0, 0, screen_width, screen_height), wall_thickness)

        point_list = []
        for a, b in wall_lines:
            a_x, a_y = to_loc(a)
            b_x, b_y = to_loc(b)

            print(f"({a} | {b})")
            print(f"({a_x}, {a_y}) | ({b_x}, {b_y})")

            a_x = a_x * cell_width_height
            a_y = a_y * cell_width_height
            b_x = b_x * cell_width_height
            b_y = b_y * cell_width_height

            # important: pygame: the point coordinate is x-y coordinate, not y-x coordinate (wall data is y-x coordinate)
            # pygame.draw.line(screen, black, (320,0), (320,320), 1)
            # print("vertical")
            # add wall

            point_list.append((b_y, b_x))
            if a_x == b_x:
                # vertical
                pygame.draw.line(screen, black, (b_y, b_x), (b_y, b_x + cell_width_height), wall_thickness)
                point_list.append((b_y, b_x + cell_width_height))
                # print(f'(b_y, b_x) -> (b_y, b_x + cell_width_height)')
                print("vertical")
            elif a_y == b_y:
                # horizontal
                pygame.draw.line(screen, black, (b_y, b_x), (b_y + cell_width_height, b_x), wall_thickness)
                point_list.append((b_y + cell_width_height, b_x))
                print("horizontal")
            else:
                print("Error")

                exit()

            # break

        # 绘制文本
        screen.blit(text_start, text_start_rect)
        screen.blit(text_end, text_end_rect)

        # turn corner

        point_count = Counter(point_list)
        print(point_count)
        for coord, count in point_count.items():
            if count == 2:
                print(f"corner: {coord}")
                pygame.draw.rect(
                    screen,
                    black,
                    (coord[0] - wall_thickness // 2, coord[1] - wall_thickness // 2, wall_thickness, wall_thickness),
                )

                # pygame.draw.circle(screen, black, coord, wall_thickness//2)

        # pygame.draw.circle(screen, black, (cell_width_height, cell_width_height), 2.5)
        # pygame.draw.rect(screen, black, (cell_width_height - square_size // 2, cell_width_height - square_size // 2, square_size, square_size))

        # 更新屏幕显示
        pygame.display.flip()

        # pygame.image.save(screen, "maze.png")

        # exit()
        # 暂停一段时间，例如暂停5秒钟
        # pygame.time.wait(5000)

    # 退出pygame
    pygame.quit()


if __name__ == "__main__":
    run_pygame()
