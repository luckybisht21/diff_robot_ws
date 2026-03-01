import csv
import os
from collections import defaultdict

def extract_data():
    csv_file = os.path.expanduser('~/diff_robot_ws/lidar_data.csv')

    if not os.path.exists(csv_file):
        print('No data file found! Run the robot first.')
        return

    room_stats = defaultdict(lambda: {
        'front': [], 'left': [], 'back': [],
        'right': [], 'closest': [], 'count': 0
    })

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            room = int(row['room'])
            room_stats[room]['front'].append(float(row['front']))
            room_stats[room]['left'].append(float(row['left']))
            room_stats[room]['back'].append(float(row['back']))
            room_stats[room]['right'].append(float(row['right']))
            room_stats[room]['closest'].append(float(row['closest_dist']))
            room_stats[room]['count'] += 1

    room_names = {
        1: 'Room 1 - Bottom Left  [RED objects]',
        2: 'Room 2 - Bottom Right [GREEN objects]',
        3: 'Room 3 - Top Left     [BLUE objects]',
        4: 'Room 4 - Top Right    [YELLOW objects]'
    }

    print('\n' + '='*55)
    print('         LIDAR DATA EXTRACTION REPORT')
    print('='*55)

    for room_num in sorted(room_stats.keys()):
        data = room_stats[room_num]
        if data['count'] == 0:
            continue

        def stat(arr):
            return f'min={min(arr):.2f} max={max(arr):.2f} avg={sum(arr)/len(arr):.2f}'

        print(f'\n📍 {room_names[room_num]}')
        print(f'   Total readings : {data["count"]}')
        print(f'   Front (m)      : {stat(data["front"])}')
        print(f'   Left  (m)      : {stat(data["left"])}')
        print(f'   Back  (m)      : {stat(data["back"])}')
        print(f'   Right (m)      : {stat(data["right"])}')
        print(f'   Closest (m)    : {stat(data["closest"])}')
        print(f'   Nearest object : {min(data["closest"]):.2f}m')

    print('\n' + '='*55)
    print(f'Data source: {csv_file}')
    print('='*55 + '\n')

if __name__ == '__main__':
    extract_data()
