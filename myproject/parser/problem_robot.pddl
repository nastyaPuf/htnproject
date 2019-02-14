(define
 (:problem prob1)
 (:domain robot)
	(:objects
		p - PACKAGE
		r1 r2 - ROOM
		d12 - ROOMDOOR
	)
 (:init
     (rloc r0)
     (armempty)
     (in o1 r01)
     (door r1 r2 d12)
)

 (:goal
    (move_in_cl r0 r1 d01)
 )
 )