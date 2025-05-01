import re
import math
import matplotlib.pyplot as plt

# Path to your VCD file
vcd_file_path = "mechanical-display.vcd"  # Change this to your actual filename

# Timescale (we'll extract this from the file or set it manually)
timescale = 10e-6  # Default to 10 µs if not found

# Lists to store transitions
transitions = []
timescale = 10 * 10e-6
# Retrieve transitions
with open(vcd_file_path, "r") as f:
    for line in f:
        line = line.strip()

        # Parse signal transitions (e.g., "#5290 1!")
        if line.startswith("#"):
            current_time = int(line[1:line.find(' ')])
            value = int(line[line.find(' ')+1:-1])
            # print(current_time, "  :  ", value)
            transitions.append((current_time, value))
print(transitions[:10])

# Get the all '1' times 
up_trans = transitions[0]
up_times = []
for t in transitions[1:]:
    # front montant
    if t[1] == 1:
        up_trans = t
    # front descendant
    else:
        up_times.append(t[0] - up_trans[0])
print(up_times[:10])

# Retrieve angles
min_t = 60  # 0 or -90
max_t = 240 # 180 or +90*
angles = []
for t in up_times: # t is 60 to 240
    t = math.ceil(t/10)*10
    angle = t-60-90
    angles.append(angle)
    print(t, " : ", angle)
print(angles[:10])

# Retrieve character
chars = [
    (-90, '0'),
    (-80, '1'),
    (-70, '2'),
    (-60, '3'),
    (-50, '4'),
    (-40, '5'),
    (-30, '6'),
    (-20, '7'),
    (-10, '8'),
    (  0, '9'),
    ( 10, 'A'),
    ( 20, 'B'),
    ( 30, 'C'),
    ( 40, 'D'),
    ( 50, 'F'),
    ( 60, 'S'),
    ( 70, '{'),
    ( 80, '}'),
    ( 90, '_')
]
for a in angles:
    count = 0
    for c in chars:
        if abs(c[0]-(a)) <= 4:
            print(c[1], end='')
            break
        elif count == 18:
            # print(f"error no char found for {a} !")
            pass
        count += 1

# FCSC{S3C937_13601AS_913AS3_5B72D3C7}