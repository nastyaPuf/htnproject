(define
 (:problem prob1)
 (:domain robot)
	(:objects
		p - PACKAGE
		r0 r1 r2 - ROOM
		d12 d01 d02 - ROOMDOOR
	)
 (:init
     (rloc c)
     (armempty)
     (in o1 r01)
     (door r0 r1 d01)
     (door r0 r2 d02)
     (door r1 r2 d12)
)

 (:goal
    (move_in_cl r0 r1 d01)
 )