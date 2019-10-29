name:
move_pac_in_room p r1 r2 d12

initial state:
rloc r1
in p r1
armempty
door r1 r2 d12
door r2 r1 d12
closed d12

effects:
door r1 r2 d12
door r2 r1 d12
rloc r2
armempty
in p r2
not in p r1
not closed d12
not rloc r1
not holding p

tasks:
pickup p r1
open d12 r1 r2
move d12 r1 r2
putdown p r2






name:
move_pac_in_room p r2 r1 d12

initial state:
rloc r2
in p r2
armempty
door r1 r2 d12
door r2 r1 d12
closed d12

effects:
armempty
door r1 r2 d12
door r2 r1 d12
not in p r2
not closed d12
not rloc r2
not holding p

tasks:
move_pac_in_room p r2 r1 d12


name:
move_2_packs d12 p p1 r1 r2

initial state:
rloc r1
in p r1
in p1 r1
armempty
door r1 r2 d12
door r2 r1 d12
closed d12

effects:
door r1 r2 d12
door r2 r1 d12
in p r2
rloc r2
armempty
in p1 r2
not in p r1
not closed d12
not holding p
not in p1 r1
not rloc r1
not holding p1

tasks:
move_pac_in_room p r1 r2 d12
move d12 r2 r1
pickup p1 r1
move d12 r1 r2
putdown p1 r2






name:
move_2_packs d12 p p1 r1 r2

initial state:
rloc r1
in p r1
in p1 r1
armempty
door r1 r2 d12
door r2 r1 d12
closed d12

effects:
armempty
door r1 r2 d12
door r2 r1 d12
in p r2
rloc r2
in p1 r2
not in p r1
not closed d12
not holding p
not in p1 r1
not rloc r1
not holding p1

tasks:
move_2_packs d12 p p1 r1 r2






