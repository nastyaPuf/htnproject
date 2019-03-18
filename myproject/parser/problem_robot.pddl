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
     (in p r1)
     (in p1 r1)
     (armempty)
     (door r1 r2 d12)
     (door r2 r1 d12)
     (closed d12)
)

 (:goal
    (move_2_packs d12 p p1 r1 r2))