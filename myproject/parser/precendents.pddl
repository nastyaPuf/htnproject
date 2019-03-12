name:
move_pac_in_room p r1 r2 d12

initial state:
rloc r1
armempty
in p r1
door r1 r2 d12
door r2 r1 d12
in p1 r1
not closed d12
not in p r2
not in p2 r2

effects:
door r1 r2 d12
door r2 r1 d12
in p1 r1
rloc r2
armempty
in p r2
not closed d12
not in p2 r2
not in p r1
not rloc r1
not holding p

tasks:
pickup p r1
move d12 r1 r2
putdown p r2




name:
ret_pac p r1 r2 d12

initial state:
rloc r1
armempty
in p r1
door r1 r2 d12
door r2 r1 d12
in p1 r1
not closed d12
not in p r2
not in p2 r2

effects:
door r1 r2 d12
door r2 r1 d12
in p1 r1
armempty
in p r2
rloc r1
not closed d12
not in p2 r2
not in p r1
not holding p
not rloc r2

tasks:
pickup p r1
move d12 r1 r2
putdown p r2
move d12 r2 r1





name:
move_2_packs d12 p p1 r1 r2

initial state:
rloc r1
armempty
in p r1
door r1 r2 d12
door r2 r1 d12
in p1 r1
not closed d12
not in p r2
not in p2 r2

effects:
door r1 r2 d12
door r2 r1 d12
in p r2
rloc r2
armempty
in p1 r2
not closed d12
not in p2 r2
not in p r1
not holding p
not in p1 r1
not rloc r1
not holding p1

tasks:
pickup p r1
move d12 r1 r2
putdown p r2
move d12 r2 r1
pickup p1 r1
move d12 r1 r2
putdown p1 r2




