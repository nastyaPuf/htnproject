(define
 (:problem prob1)
 (:domain robot)
	(:objects
		p p1 - PACKAGE
		r1 r2 - ROOM
		d12 - ROOMDOOR
	)
 (:init
     (rloc r1)
     (armempty)
     (in p r1)
     (door r1 r2 d12)
     (door r2 r1 d12)
     (not closed d12)
     (in p1 r1)
     (not in p r2)
     (not in p2 r2)
)

 (:goal
    (move_2_packs d12 p p1 r1 r2))