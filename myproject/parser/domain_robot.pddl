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

(:task move_in_room
		:parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
		:precondition ()
		:effect ()
	)

(:task move_pac_in_room
		:parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
		:precondition ()
		:effect ()
	)

(:task ret_pac
		:parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
		:precondition ()
		:effect ()
	)

(:task move_2_packs
		:parameters (?d - ROOMDOOR ?p1 - PACKAGE ?p2 - PACKAGE ?loc1 - ROOM ?loc2 - ROOM)
		:precondition ()
		:effect ()
	)

(:method move_in_closed_room
        :parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (closed ?d))
        :task (move_in_room)
        :subtasks (and
         (task0 (open ?d ?loc1 ?loc2))
         (task1 (move ?d ?loc1 ?loc2)))
		:ordering (and
		 (task0 < task1)
		))

(:method move_in_opened_room
        :parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (not (closed ?d))
        :task (move_in_room)
        :subtasks
         (task1 (move ?d ?loc1 ?loc2))
        ))

(:method move_pac
        :parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (armempty) (rloc ?loc1) (in ?p ?loc1) (not (closed ?d)) (door ?loc1 ?loc2 ?d))
        :task (move_pac_in_room)
        :subtasks (and
         (task0 (pickup ?p ?loc1))
         (task1 (move_in_room ?d ?loc1 ?loc2))
         (task2 (putdown ?p ?loc2))))
		:ordering (and
		 (task0 < task1)
		 (task1 < task2)
		))

(:method return_pac
        :parameters (?p - PACKAGE ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
        :precondition (and (armempty) (rloc ?loc1) (in ?p ?loc1) (closed ?d) (door ?loc1 ?loc2 ?d))
        :task (ret_pac)
        :subtasks (and
         (task0 (move_pac_in_room ?p ?loc1 ?loc2 ?d))
         (task1 (move_in_room ?d ?loc2 ?loc1)))
		:ordering (and
		 (task0 < task1)
		 (task1 < task2)
		))

(:method move_two_pacs
        :parameters (?d - ROOMDOOR ?p1 - PACKAGE ?p2 - PACKAGE ?loc1 - ROOM ?loc2 - ROOM)
        :precondition (and (armempty) (rloc ?loc1) (in ?p1 ?loc1) (in ?p2 ?loc1) (closed ?d) (door ?loc1 ?loc2 ?d))
        :task (move_2_packs)
        :subtasks (and
         (task0 (move_pac_in_room ?p1 ?loc1 ?loc2 ?d))
         (task1 (move_in_room ?d ?loc2 ?loc1))
         (task2 (move_pac_in_room ?p2 ?loc1 ?loc2 ?d)))
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
        :precondition (and (rloc ?loc) (holding ?obj))
        :effect (and (not (holding ?obj)) (armempty) (in ?obj ?loc))
)

(:action move
        :parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
        :task (move)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (not (closed ?d)) )
        :effect (and (rloc ?loc2) (not (rloc ?loc1)))
)

(:action open
        :parameters (?d - ROOMDOOR ?loc1 - ROOM ?loc2 - ROOM)
        :task (open)
        :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (closed ?d))
        :effect (and (not (closed ?d)))
)
