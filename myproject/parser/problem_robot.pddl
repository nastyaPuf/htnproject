(define
 (:problem prob1)
 (:domain robot)
	(:objects
		p - PACKAGE
		r1 r2 - ROOM
		d12 - ROOMDOOR
	)
 (:init
     (rloc r1)
     (armempty)
     (in p r1)
     (door r1 r2 d12)
     (door r2 r1 d12)
     (closed d12)
     (not in p r2))
)

 (:goal
    (move_p_cl p r1 r2 d12)))