import tkinter as tk
import random
import math

WIDTH = 900
HEIGHT = 500
GROUND_Y = 400

root = tk.Tk()
root.title("Tkinter Crash Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

# --------------------------------------------------
# 게임 상태
# --------------------------------------------------

player_x = 100.0
player_y = 300.0

vx = 0.0
vy = 0.0

camera_x = 0.0

gravity = 0.45

keys = set()

# 충돌 연출
shake_x = 0
shake_y = 0
shake_count = 0

hit_stop = 0

# 장애물 위치
obstacles = [
    [700, 350, 750, 400],
    [1300, 320, 1360, 400],
    [1900, 340, 1960, 400],
    [2600, 300, 2670, 400],
]

# --------------------------------------------------
# 키보드
# --------------------------------------------------

def key_down(event):
    keys.add(event.keysym)


def key_up(event):
    keys.discard(event.keysym)


root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

# --------------------------------------------------
# 충돌
# --------------------------------------------------

def collision():
    global vx, vy
    global shake_count
    global hit_stop

    # 강하게 튕김
    vx *= -0.7
    vy = -8

    # 화면 흔들림
    shake_count = 12

    # 약 5프레임 정지
    hit_stop = 5


# --------------------------------------------------
# 업데이트
# --------------------------------------------------

def update():
    global player_x, player_y
    global vx, vy
    global camera_x
    global shake_x, shake_y
    global shake_count
    global hit_stop

    # ----------------------------------------------
    # Hit Stop
    # ----------------------------------------------

    if hit_stop > 0:
        hit_stop -= 1

        draw()

        root.after(16, update)
        return

    # ----------------------------------------------
    # 플레이어 조작
    # ----------------------------------------------

    if "Right" in keys:
        vx += 0.5

    if "Left" in keys:
        vx -= 0.5

    if "space" in keys:

        # 땅에 있을 때만 점프
        if player_y >= GROUND_Y - 30:
            vy = -10

    # ----------------------------------------------
    # 최대 속도
    # ----------------------------------------------

    max_speed = 15

    if vx > max_speed:
        vx = max_speed

    if vx < -max_speed:
        vx = -max_speed

    # 마찰
    vx *= 0.99

    # 중력
    vy += gravity

    # 이동
    player_x += vx
    player_y += vy

    # ----------------------------------------------
    # 바닥
    # ----------------------------------------------

    if player_y > GROUND_Y - 30:

        player_y = GROUND_Y - 30
        vy = 0

    # ----------------------------------------------
    # 장애물 충돌
    # ----------------------------------------------

    player_left = player_x - 15
    player_right = player_x + 15

    player_top = player_y - 15
    player_bottom = player_y + 15

    for obstacle in obstacles:

        ox1, oy1, ox2, oy2 = obstacle

        if (
            player_right > ox1
            and player_left < ox2
            and player_bottom > oy1
            and player_top < oy2
        ):
            collision()

            # 장애물 내부로 계속 들어가는 것 방지
            if vx < 0:
                player_x = ox2 + 20
            else:
                player_x = ox1 - 20

            break

    # ----------------------------------------------
    # 카메라
    # ----------------------------------------------

    # 플레이어가 화면 가운데보다 조금 왼쪽에 위치하도록
    target_camera = player_x - 300

    # 부드러운 카메라 이동
    camera_x += (target_camera - camera_x) * 0.12

    # ----------------------------------------------
    # 화면 흔들림
    # ----------------------------------------------

    if shake_count > 0:

        shake_x = random.randint(-12, 12)
        shake_y = random.randint(-8, 8)

        shake_count -= 1

    else:

        shake_x = 0
        shake_y = 0

    # ----------------------------------------------

    draw()

    root.after(16, update)


# --------------------------------------------------
# 그리기
# --------------------------------------------------

def draw():

    canvas.delete("all")

    # ----------------------------------------------
    # 배경
    # ----------------------------------------------

    canvas.create_rectangle(
        0,
        GROUND_Y,
        WIDTH,
        HEIGHT,
        fill="darkgreen",
        outline=""
    )

    # ----------------------------------------------
    # 속도선
    # ----------------------------------------------

    speed = abs(vx)

    if speed > 8:

        for i in range(15):

            x = random.randint(0, WIDTH)
            y = random.randint(50, 350)

            length = int(speed * 3)

            canvas.create_line(
                x,
                y,
                x - length,
                y,
                fill="white",
                width=2
            )

    # ----------------------------------------------
    # 장애물
    # ----------------------------------------------

    for obstacle in obstacles:

        ox1, oy1, ox2, oy2 = obstacle

        screen_x1 = ox1 - camera_x + shake_x
        screen_x2 = ox2 - camera_x + shake_x

        screen_y1 = oy1 + shake_y
        screen_y2 = oy2 + shake_y

        canvas.create_rectangle(
            screen_x1,
            screen_y1,
            screen_x2,
            screen_y2,
            fill="red",
            outline="black",
            width=3
        )

    # ----------------------------------------------
    # 플레이어
    # ----------------------------------------------

    screen_x = player_x - camera_x + shake_x
    screen_y = player_y + shake_y

    canvas.create_oval(
        screen_x - 15,
        screen_y - 15,
        screen_x + 15,
        screen_y + 15,
        fill="yellow",
        outline="black",
        width=3
    )

    # 이동 방향 표시
    if vx != 0:

        direction = 1 if vx > 0 else -1

        canvas.create_line(
            screen_x,
            screen_y,
            screen_x + direction * 25,
            screen_y,
            width=4,
            arrow=tk.LAST
        )

    # ----------------------------------------------
    # UI
    # ----------------------------------------------

    canvas.create_text(
        10,
        10,
        anchor="nw",
        text=f"Speed : {vx:.1f}",
        font=("Arial", 16, "bold")
    )

    canvas.create_text(
        10,
        40,
        anchor="nw",
        text=f"World X : {player_x:.0f}",
        font=("Arial", 14)
    )

    canvas.create_text(
        WIDTH - 10,
        10,
        anchor="ne",
        text="← → 이동    SPACE 점프",
        font=("Arial", 14, "bold")
    )


# --------------------------------------------------
# 게임 시작
# --------------------------------------------------

update()

root.mainloop()