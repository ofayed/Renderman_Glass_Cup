
import prman
import math
import sys
import sys, os.path, subprocess
import argparse

ri = prman.Ri()  

def make_cuboid(x,y,z):

    points = [
        -x,
        -x,
        -z,

        x,
        -x,
        -z,

        -x,
        -y,
        -z,

        x, 
        -y,
        -z,

        -x,
        -x,
        z,

        x,
        -x,
        z,

        -x,
        -y,
        z,

        x,
        -y,
        z,
    ]
    npolys = [4, 4, 4, 4, 4, 4]
    nvertices = [0, 2, 3, 1, 0, 1, 5, 4, 0, 4, 6, 2, 1, 3, 7, 5, 2, 6, 7, 3, 4, 5, 7, 6]
    ri.PointsPolygons(npolys, nvertices, {ri.P: points})


def build_table_legs(x,radius,leg_height):
    ri.TransformBegin()
    length = 2 * x
    
    ri.Rotate(90, 1, 0, 0)

    ri.Translate(length, 0, 0)
    ri.Cylinder(radius, 0.0, 1, 360) 
    ri.Translate(0, length, 0)
    ri.Cylinder(radius, 0.0, 1, 360) 
    ri.Translate(-length, 0, 0)
    ri.Cylinder(radius, 0.0, 1, 360) 

    ri.Translate(0, -length, 0)
    ri.Cylinder(radius, 0.0, 1, 360) 
    ri.TransformEnd()

def circle_pattern(n, radius, height, sweep_angle, tilt_angle, cylinder_radius): 
    for i in range(n):
        theta = (2 * math.pi / n) * i
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)


        tilt_x = -math.sin(theta)
        tilt_y = math.cos(theta)

        ri.AttributeBegin()


        ri.Translate(x, y, 0)


        ri.Rotate(tilt_angle, tilt_x, tilt_y, 0)


        rotation_angle = math.degrees(theta)  - (sweep_angle / 2)
        ri.Rotate(rotation_angle, 0, 0, 1)

        # ri.Rotate(180, 1, 0, 0)

        ri.Cylinder(cylinder_radius, 0, height, sweep_angle)

        ri.AttributeEnd()

def sphere_circle_pattern(n, radius, height, sweep_angle, tilt_angle, cylinder_radius): 
    for i in range(n):
        theta = (2 * math.pi / n) * i
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)


        tilt_x = -math.sin(theta)
        tilt_y = math.cos(theta)

        ri.AttributeBegin()


        ri.Translate(x, y, 0)


        ri.Rotate(tilt_angle, tilt_x, tilt_y, 0)


        rotation_angle = math.degrees(theta)  - (sweep_angle / 2)
        ri.Rotate(rotation_angle, 0, 0, 1)


        ri.Rotate(90, 0, 1, 0)
        ri.Rotate(45, 1, 0, 0)
        # new_rad = math.sqrt((cylinder_radius*cylinder_radius) + (cylinder_radius*cylinder_radius) )
        # print(new_rad)  
        # print(cylinder_radius)
        ri.Sphere(cylinder_radius, -cylinder_radius, cylinder_radius, sweep_angle)

        ri.AttributeEnd()


def Hyperboloid_circle_pattern(n, min_radius, max_radius, height, sweep_angle): 

    ri.Rotate(180, 1, 0, 0)
    for i in range(n):

        theta = (2 * math.pi / n) * i
 

 
        x = radius * math.cos(theta)
        
        y = radius * math.sin(theta)
        
        tilt_x = -math.sin(theta)
        tilt_y = math.cos(theta)



        ri.AttributeBegin()
        

        ri.Translate(x, y, 0)

        
        ri.Rotate(-90, tilt_x, tilt_y, 0)


        rotation_angle = math.degrees(theta)  - (sweep_angle / 2)

        ri.Rotate(rotation_angle, 0, 0, 1)
   

        ri.Hyperboloid([min_radius, 0.0, height], [max_radius, 0.0, 0], sweep_angle) 

        ri.AttributeEnd()



def Create_Lid(n, radius, min_radius, max_radius, hyper_length, cylinder_length, sweep_angle):
    for i in range(n):
        theta = (2 * math.pi / n) * i
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)


        tilt_x = -math.sin(theta)
        tilt_y = math.cos(theta)

        ri.AttributeBegin()


        ri.Translate(x, y, 0)


        # ri.Rotate(tilt_angle, tilt_x, tilt_y, 0)


        rotation_angle = math.degrees(theta)  - (90 / 2)
        ri.Rotate(rotation_angle, 0, 0, 1)


        ri.Rotate(135, 0, 0, -1)




        ri.TransformBegin()
        ri.Translate(0.175, 0, max_radius)
        ri.Rotate(90, 0, 1, 0)
        ri.Rotate(45, 0, 0, -1)

        ri.Hyperboloid([min_radius, 0.0, hyper_length], [max_radius, 0.0, 0], sweep_angle)
        ri.TransformEnd()

        ri.TransformBegin()
        ri.Translate(0.175, 0, max_radius)
        ri.Rotate(135, 0, 0, 1)

        ri.Cylinder(max_radius, 0, cylinder_length, sweep_angle)

        ri.TransformEnd()

        ri.TransformBegin()

        ri.Translate(0.1, 0, 0)
        ri.Translate(0.075, 0, 0.075)
        ri.Rotate(90, 1, 0, 0)
        ri.Rotate(180, 0, 0, 1)

        ri.Sphere(max_radius, -max_radius, max_radius, sweep_angle)
        ri.TransformEnd()


        ri.AttributeEnd()


ri.Begin("__render")

ri.Display("glass.exr", "it", "rgba")
# ri.Format(3840, 2160, 1)



ri.Format(1080, 720, 1)
ri.Hider("raytrace", {"int incremental": [1]})
ri.ShadingRate(10)
ri.PixelVariance(0.1)
ri.Integrator("PxrPathTracer", "integrator", {})
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 48})


# ri.Rotate(-30, 1, 0, 0)


ri.Translate(-0.25, -0.35, 0.6)

# ri.Translate(-0.25, -0.1, 1.5)

# ri.Translate(-0.25, 0, 0)

# ri.Rotate(90, 1, 0, 0)

ri.WorldBegin()
#######################################################################
# Lighting 
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
# ri.Declare("dayLight", "string")

# ri.Light("PxrEnvDayLight", "dayLight", {"int month": 6, "int day": 20, "float hour": 10})

ri.Identity()
ri.Declare('domeLight' ,'string')
ri.Rotate(-90,1,0,0)
ri.Rotate(100,0,0,1)
ri.Light( 'PxrDomeLight', 'domeLight', { 
          'string lightColorMap'  : 'room.tex'
  })#


ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################


ri.AttributeBegin()
ri.Attribute("identifier", {"name": "straw"})

ri.Attribute("visibility", {"int transmission": [1]})
ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
ri.Bxdf(
    "PxrSurface",
    "glassstraw",
    {
        "color refractionColor": [1, 1, 1],
        "float diffuseGain": 0,
        "color specularEdgeColor": [1, 1, 1],
        "float refractionGain": [1.0],
        "float reflectionGain": [1.0],
        "float glassRoughness": [0.01],
        "float glassIor": [1.5],
        "color extinction": [0.0, 0.2, 0.0],
    },
)

# ri.Paraboloid(0.1, 0.1, 0.2, 180)

# ri.TransformBegin()
# # ri.Translate(-0.5, -1, 0)
# ri.Rotate(180, 0, 1, 0)
# ri.Scale(0.1, 0.1, 0.1)


# ri.Translate(-3, 4, 0)
# ri.Translate( -0.5,0,0)

# ri.Rotate(15,0,0,1)


ri.TransformBegin()

ri.Translate(0.25, 0.5,0) 
ri.Scale(0.1, 0.1, 0.1)   
# ri.Rotate(15,0,0,-1)
################ STRAW ####################################
ri.TransformBegin()



ri.Translate(-0.448, 0, 0)    
ri.Torus(0.45, 0.09, 0.0, 360, 20) #Link Straw
# ri.Torus(0.45, 0.055, 0.0, 360, 20) #Link Straw

ri.TransformEnd()

ri.TransformBegin()

ri.Rotate(90,1,0,0)

ri.TransformBegin()
ri.Translate(0.005, 0, 0)
ri.Cylinder(0.09, 0.0, 3.25, 360) #longer Straw
ri.Cylinder(0.055, 0.0, 3.25, 360) #longer Straw
ri.TransformEnd()


ri.Rotate(20,0,1,0)

ri.TransformBegin()
ri.Translate(0.03, 0.0, -0.9)
# ri.Translate(-0.08, 0, -0.2)
ri.Torus(0.065, 0.025, 180.0, 360, 360) 
ri.TransformEnd()

ri.Translate(0.03, 0, -0.9)
ri.Cylinder(0.09, 0.0, 0.75, 360) #Shorter Straw
ri.Cylinder(0.055, 0.0, 0.75, 360) #Shorter Straw

ri.TransformEnd()
ri.TransformEnd()
ri.AttributeEnd()

#################################################################



ri.AttributeBegin()
ri.Scale(0.1, 0.1, 0.1)
ri.Translate(3, 4, 0)
ri.Translate( -0.5,0,0)

ri.Attribute("identifier", {"name": "cup"})

ri.Attribute("visibility", {"int transmission": [1]})
ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
ri.Pattern("scratches", "scratches", {})

ri.Bxdf(
    "PxrSurface",
    "glasscup",
    {
        "color refractionColor": [1, 1, 1],
        "float diffuseGain": 0,
        "color specularEdgeColor": [1, 1, 1],
        "float refractionGain": [1.0],
        "float reflectionGain": [1.0],
        "float glassRoughness": [0.15],
        "float glassIor": [1.45],
        "color extinction": [0.0, 0.2, 0.0],
        # "reference color bumpNormal": ["scratches:out_scratches"]
    
    },
)

################ CUP BASE ####################################

ri.TransformBegin()
ri.Translate(0, -2.3, 0)
ri.Rotate(90,1,0,0)


ri.Translate(0, 0, 0.22)

ri.TransformBegin()

ri.Scale(1, 1, 1)
ri.Torus(0.56, 0.05, 0.0, 360.0, 360.0) #Cup Bottom

ri.TransformEnd()   

ri.Translate(0, 0, -0.2)
ri.Disk(0.2, 0.5, 360)  #Cup Bottom
ri.TransformEnd()

ri.TransformBegin()
ri.Rotate(90,1,0,0)


ri.TransformBegin()
ri.Translate(0, 0, -0.5)
# ri.Hyperboloid([0.6, 0.0, 3], [0.79, 0.0, 0], 360.0) #Cup Body
ri.TransformEnd()
ri.Translate(0, 0, -0.49)
ri.Torus(0.752, 0.06, 300, 360.0, 360.0) #Cup Top

ri.Translate(0,2.5,0)


ri.TransformEnd()


#################################################################
ri.Rotate(90,1,0,0)
ri.Translate(0, 0, -0.5)

ri.TransformBegin()
ri.Translate(0, 0, -0.2)
n = 50
radius = 1
min_radius = 0.02
max_radius = 0.075
hyper_length = 0.75
sweep_angle = 90
cylinder_length = 0.25

Create_Lid(n, radius, min_radius, max_radius, hyper_length, cylinder_length, sweep_angle)

ri.TransformEnd()

################ LID TOP PATTERN ####################################
ri.Rotate(90,1,0,0)

ri.TransformBegin()
ri.Translate(0, 0, -0.075)
# ri.Rotate(90, 1, 0, 0)
# ri.Rotate(5, 0, 1, 0)
n = 4
radius =0.85
min_radius = 0.02
max_radius = 0.075
sweep_angle = 90
height = 0.775
# Hyperboloid_circle_pattern(n, min_radius, max_radius, height, sweep_angle)

# ri.Translate(0, 0.775,0)
# ri.Translate(0, 0, 0.075)
# ri.Rotate(90, 1, 0, 0)
# ri.Rotate(90, 0, 1,0)

ri.TransformBegin()
ri.Translate(0.775, 0,0)
ri.Translate(0, 0, 0.075)
ri.Rotate(90, 1, 0, 0)
# ri.Rotate(90, 0, 1,0)

ri.TransformEnd()

ri.TransformBegin()

ri.Translate(0, 0.85,0)
ri.Translate(-0.075/2, 0,0)
ri.Translate(0, 0, 0.075)
ri.Rotate(90, 1, 0, 0)
ri.Rotate(90, 0, 1,0)



ri.TransformEnd()

ri.TransformEnd()   
#################################################################

################ LID SIDE PATTERN ####################################

ri.TransformBegin()
ri.Translate(0, 0, -0.1)
# ri.Rotate(180, 0, 0, 1)
n = 4
radius =0.85
cylinder_height = 0.25
cylinder_radius = 0.075
tilt_angle = 0
sweep_angle = 90
# circle_pattern(n, radius, cylinder_height, sweep_angle, tilt_angle, cylinder_radius )


ri.Translate(0,0 , 0.075/4)
radius =0.8075
# sphere_circle_pattern(n, radius + cylinder_radius/2   , height, sweep_angle, tilt_angle, cylinder_radius)

# ri.Sphere(cylinder_radius/2, -cylinder_radius/2, cylinder_radius/8, 180)
ri.TransformEnd()

################################################################   

################ CUP PATTERN ####################################
ri.Rotate(90,-1,0,0)

n = 62
radius =0.75
tilt_angle = -3.7
cylinder_height = 3
cylinder_radius = 0.06
sweep_angle = 80
circle_pattern(n, radius, cylinder_height, sweep_angle, tilt_angle, cylinder_radius, )

ri.AttributeEnd()


################ TABLE LEGS ####################################


# ri.Pattern("PxrTexture", "ratGrid", {"string filename": "bright_wood.tex", "int invertT": [0]})

# ri.Bxdf("PxrDiffuse", "diffuse", {"reference color diffuseColor": ["ratGrid:resultRGB"]})

# ri.AttributeBegin()
# radius = 0.04
# table_length = 0.3
# leg_height = 1
# build_table_legs(table_length,radius,leg_height)



# ################################################################

# ################ TABLE TOP ####################################


# ri.TransformBegin()

# ri.Translate(0.3, 0.5, 0.3)


# ri.Pattern("PxrTexture", "colormap", {"string filename": "bright_wood.tex", "int invertT": [0]})


# ri.Pattern("PxrNormalMap", "normalmap", {"filename": "bright_wood_normals.tex"})

# ri.Bxdf("PxrSurface", "surf", {
#     "reference color diffuseColor": ["colormap:resultRGB"],
#     "reference color bumpNormal": ["normalmap:resultN"]
# })

# make_cuboid(0.5,0.4,0.5)



# ri.TransformEnd()   

# #################################################################

# ri.AttributeEnd()

# end our world
ri.WorldEnd()
# and finally end the rib file




ri.End()
