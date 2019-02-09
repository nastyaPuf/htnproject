(define
    (:problem pfile01)
	(:domain  domain_htn)
	(:objects
		package_0 package_1 - package
		city_loc_0 city_loc_1 city_loc_2 - location
		truck_0 - vehicle
	)
	(:init
		(road city_loc_0 city_loc_1)
		(road city_loc_1 city_loc_0)
		(road city_loc_1 city_loc_2)
		(road city_loc_2 city_loc_1)
		(at package_0 city_loc_1)
		(at package_1 city_loc_1)
		(at truck_0 city_loc_2)
	)
	(:goal
	    (in city_loc_0 package_0)
	    (in city_loc_2 package_1)
	)
)