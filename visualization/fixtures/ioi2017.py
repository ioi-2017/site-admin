import json
import sys
import math


def next_desk_pk():
    global desk_id
    if desk_id is not None:
        desk_id += 1
        return desk_id - 1
    return None


def generate_desks(rows_size, room_id):
    for row in range(3):
        margin = 0.1
        hor_num = row * 2 + 5
        dist = (1 - 2 * margin) / 14
        break_angle = 25 * math.pi / 180
        for index in range(rows_size[row]):
            break_x = (1 - margin) - hor_num * dist
            break_y = 0.4 + 0.25 * row
            if index < hor_num:
                x = (1 - margin) - index * dist
                y = break_y
                desk_angle = 0
            else:
                x = break_x - (index - hor_num + 1) * 1.5 * dist * math.sin(break_angle)
                y = break_y - (index - hor_num + 1) * 1.5 * dist * math.cos(break_angle)
                desk_angle = 60
            yield {
                "model": "visualization.desk",
                "pk": next_desk_pk(),
                "fields": {
                    "room": room_id,
                    "number": row * 20 + (10 if row == 0 else 0) + index,
                    "x": x,
                    "y": y,
                    "angle": desk_angle,
                }
            }


def generate_room(id, name):
    yield {
        "model": "visualization.room",
        "pk": id,
        "fields": {
            "name": name,
        }
    }


if __name__ == '__main__':
    room_name = sys.argv[1]
    rows = list(map(int, sys.argv[2:5]))
    angle = int(sys.argv[5])
    room_id = int(sys.argv[6]) if len(sys.argv) > 6 else None
    desk_id = int(sys.argv[7]) if len(sys.argv) > 7 else None
    ans = list(generate_room(room_id, room_name))
    ans += list(generate_desks(rows, room_id))
    print(json.dumps(ans))
