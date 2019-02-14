(define (domain robot)
  (:requirements :strips :negative-preconditions :typing)
  (:types PACKAGE ROOM ROOMDOOR)
  (:predicates
        (armempty)
        (rloc ?loc - ROOM)
        (in ?obj - PACKAGE ?loc - ROOM)
        (holding ?obj - PACKAGE)
        (closed ?d - ROOMDOOR)
        (door ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
)

(:task move_in_cl
		:parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
		:precondition ()
		:effect ()
	)

(:task move_in_op
		:parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
		:precondition ()
		:effect ()
	)

(:task move_p_open
		:parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
		:precondition ()
		:effect ()
	)

(:task move_p_cl
		:parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
		:precondition ()
		:effect ()
	)

(:task return_pac_cl
		:parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
		:precondition ()
		:effect ()
	)

(:method move_in_closed_room
        :parameters (?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (closed ?d))
        :task (move_in_cl)
        :subtasks (and
         (task0 (open ?loc1 ?loc2 ?d))
         (task1 (move ?loc1 ?loc2 ?d)))
		:ordering (and
		 (task0 < task1)
		))

(:method move_in_opened_room
        :parameters (?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (not (closed ?d)))
        :task (move_in_op)
        :subtasks
         (task1 (move ?loc1 ?loc2 ?d))
        ))

(:method move_pac_in_opened_room
        :parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (armempty) (rloc ?loc) (in ?obj ?loc))
        :task (move_p_open)
        :subtasks (and
         (task0 (pickup ?p ?loc1))
         (task1 (move_in_op ?loc1 ?loc2 ?d))
         (task2 (putdown ?p ?loc2))))
		:ordering (and
		 (task0 < task1)
		 (task1 < task2)
		))

(:method move_pac_in_closed_room
        :parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (armempty) (rloc ?loc) (in ?obj ?loc))
        :task (move_p_cl)
        :subtasks (and
         (task0 (pickup ?p ?loc1))
         (task1 (move_in_cl ?loc1 ?loc2 ?d))
         (task2 (putdown ?p ?loc2)))
		:ordering (and
		 (task0 < task1)
		 (task1 < task2)
		))

(:method return_pac_closed
        :parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (armempty) (rloc ?loc) (in ?obj ?loc))
        :task (return_pac_cl)
        :subtasks (and
         (task0 (move_p_cl ?loc1 ?loc2 ?d ?p))
         (task1 (move_in_op ?loc2 ?loc1 ?d)))
		:ordering (and
		 (task0 < task1)
		 (task1 < task2)
		))


(:action pickup
        :parameters (?obj - PACKAGE ?loc - ROOM)
        :task (pickup ?obj)
        :precondition (and (armempty) (rloc ?loc) (in ?obj ?loc))
        :effect (and (not (in ?obj ?loc)) (not (armempty)) (holding ?obj))
)

(:action putdown
        :parameters (?obj - PACKAGE ?loc - ROOM)
        :task (putdown)
        :precondition (and (rloc ?loc) (holding ?obj) (goal_in ?obj ?loc))
        :effect (and (not (holding ?obj)) (armempty) (in ?obj ?loc))
)

(:action move
        :parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
        :task (move)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (not (closed ?d)))
        :effect (and (rloc ?loc2) (not (rloc ?loc1)))
)

(:action open
        :parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
        :task (open)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (closed ?d))
        :effect (and (not (closed ?d)))
)


