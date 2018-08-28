define terminator-laser ranger
	(
	sensor(
    		range [ 0.0  2.0 ]
		fov 360
		samples 1081
	)
	
	block(
		points 4
		point[0] [0 1]
		point[1] [1 1] 
		point[2] [1 0]
		point[3] [0 0]
		z [0 1]
	)
	
  	# generic model properties
  	color "black"
  	size [ 0.05 0.05 0.01 ]
)	

define terminator position
(
	#Shape of robot
	block
	(
		points 3
		point[0] [1 0.5]
		point[1] [0 1]
		point[2] [0 0]				
		z [0 1]
	)
	#fit shape to this size in meters
	color "green"
	size [0.2 0.2 0.1]
	terminator-laser(pose [-0.04 0.0 0.0 0])
)
