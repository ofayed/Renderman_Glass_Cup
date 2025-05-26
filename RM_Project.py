
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



ri.Format(2160, 1440, 1)
ri.Hider("raytrace", {"int incremental": [10]})
ri.ShadingRate(10)
ri.PixelVariance(0.1)
ri.Integrator("PxrPathTracer", "integrator", {})
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 48})


ri.Translate(-0.25, -0.35, 0.75)


ri.WorldBegin()

#########################LIGHTING################################
ri.TransformBegin()
ri.AttributeBegin()

ri.Identity()
ri.Declare('domeLight' ,'string')
ri.Rotate(-90,1,0,0)
ri.Rotate(100,0,0,1)
ri.Light( 'PxrDomeLight', 'domeLight', { 
          'string lightColorMap'  : 'crab.tex'
  })


ri.AttributeEnd()
ri.TransformEnd()
#######################################################################



################ STRAW ####################################

ri.AttributeBegin()
ri.Attribute("identifier", {"name": "straw"})

ri.Attribute("visibility", {"int transmission": [1]})
ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})

ri.Pattern("scratches", "scratches", {
    "float frequency": [4.0],
    "float scratch_width": [0.001],  
    "float depth": [-0.002],
    "float noise_factor": [0.5]    
})


ri.Attribute("displacementbound", {"sphere": [0.2]})

ri.Bxdf(
    "PxrSurface",
    "glassstraw",
    {
        "color refractionColor": [1, 1, 1],
        "float diffuseGain": 0,
        "color specularEdgeColor": [1, 1, 1],
        "float refractionGain": [1.2],
        "float reflectionGain": [1.2],
        "float glassRoughness": [0.01],
        "float glassIor": [1.5],
   
    },
)


ri.Displace("PxrDisplace", "lidDisplacement", {
    "float dispAmount": [1],
    "reference float dispScalar": ["scratches:disp"]

})



ri.TransformBegin()

ri.Translate(0.25, 0.5,0) 
ri.Scale(0.08, 0.08, 0.08)   


ri.TransformBegin()



ri.Translate(-0.448, 0, 0)    


ri.TransformEnd()

ri.TransformBegin()

ri.Rotate(90,1,0,0)

ri.TransformBegin()

ri.Cylinder(0.09, 0.0, 3.25, 360) #longer Straw
ri.Cylinder(0.055, 0.0, 3.25, 360) #longer Straw
ri.TransformEnd()


ri.TransformBegin()
ri.Translate(0.0, 0.0, -0.75)

ri.Torus(0.065, 0.025, 180.0, 360, 360) #Tip 
ri.TransformEnd()

ri.Translate(0, 0, -0.75)
ri.Cylinder(0.09, 0.0, 0.75, 360) #Shorter Straw
ri.Cylinder(0.055, 0.0, 0.75, 360) #Shorter Straw

ri.TransformEnd()
ri.TransformEnd()
ri.AttributeEnd()

#################################################################


################ CUP BASE ####################################

ri.AttributeBegin()
ri.Scale(0.1, 0.1, 0.1)
ri.Translate(3, 4, 0)
ri.Translate( -0.5,0,0)

ri.Attribute("identifier", {"name": "cup"})

ri.Attribute("visibility", {"int transmission": [1]})
ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
ri.Attribute("displacementbound", {"sphere": [0.2]})


ri.Pattern("ripple", "ripple", {
    "float frequency": [62.0],  
    "float amplitude": [0.1],  
})
ri.Pattern("noise", "noise", {
    "float frequency": [30.0],
    "float amplitude": [0.2],  
    "float offset": [0.1]    
})
ri.Bxdf(
    "PxrSurface",
    "glasscup",
    {

        "color refractionColor": [1, 1, 1],
        "float diffuseGain": 0,
        "color specularEdgeColor": [1, 1, 1],
        "float refractionGain": [2],
        "float reflectionGain": [1.5],
        "reference float glassRoughness": ["noise:outRoughness"],
        "float glassIor": [1.5],

    },
)






ri.TransformBegin()
ri.Rotate(90,1,0,0)




ri.TransformBegin()
ri.Translate(0, 0, -0.5)
ri.Scale(1, 1, 1.15)
ri.AttributeBegin()
ri.Displace("PxrDisplace", "rippleDisplacement", {
    "float dispAmount": [-0.1],
    "reference float dispScalar": ["ripple:disp"]

})
ri.Hyperboloid([0.6, 0.0, 3], [0.79, 0.0, 0], 360.0) #Cup Body
ri.AttributeEnd()
ri.TransformEnd()
ri.Attribute("visibility", {"int transmission": [1]})
ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
ri.Bxdf(
    "PxrSurface",
    "glasscup",
    {

        "color refractionColor": [1, 1, 1],
        "float diffuseGain": 0,
        "color specularEdgeColor": [1, 1, 1],
        "float refractionGain": [2],
        "float reflectionGain": [2],
        "reference float glassRoughness": ["noise:outRoughness"],
        "float glassIor": [1.5],

    },
)


ri.Translate(0, 0, -0.49)
ri.Torus(0.752, 0.06, 300, 360.0, 360.0) #Cup Top

ri.Translate(0,0,2.95)
ri.Disk(0.2, 0.61, 360)#Cup Bottom
ri.Translate(0,0,0.26)
ri.Disk(0.2, 0.5, 360)#Cup Bottom
ri.Translate(0,0,0.2)
ri.Torus(0.53, 0.06, 0, 180.0, 360.0) #Cup Top

ri.Translate(0, 0, -0.1)
ri.Rotate(180,1,0,0)
# ri.Torus(0.42, 0.15, 0, 360.0, 360.0) #Cup Top

ri.TransformEnd()


#################################################################

ri.AttributeBegin()
# ri.Pattern("scratches", "scratches", {
#     "float frequency": [100.0],
#     "float scratch_width": [0.01],  
#     "float depth": [-0.002],
#     "float noise_factor": [0.2]    
# })


ri.Attribute("visibility", {"int transmission": [1]})
ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
ri.Attribute("displacementbound", {"sphere": [0.2]})


ri.Pattern("noise", "noise", {
    "float frequency": [10.0],
    "float amplitude": [0.07],  
    "float offset": [0.1]    
})


# ri.Bxdf(
#     "PxrSurface",
#     "glasslid",
#     {
       

#         "color refractionColor": [1, 1, 1],
#         "float diffuseGain": 0,
#         "color specularEdgeColor": [1, 1, 1],
#         "float refractionGain": [1.0],
#         "float reflectionGain": [1.0],
#         "reference float glassRoughness": ["noise:outRoughness"],
#         "float glassIor": [1.5],

#     },
# )

# ri.Displace("PxrDisplace", "lidDisplacement", {
#     "float dispAmount": [-0.1],
#     "reference float dispScalar": ["scratches:disp"]

# })

ri.Bxdf(
    "PxrSurface",
    "glasslid",
    {

        "color refractionColor": [1, 1, 1],
        "float diffuseGain": 0,
        "color specularEdgeColor": [1, 1, 1],
        "float refractionGain": [1],
        "float reflectionGain": [1],
        "reference float glassRoughness": ["noise:outRoughness"],
        "float glassIor": [1.5],

    },
)



ri.Rotate(90,1,0,0)
ri.Translate(0, 0, -0.5)

ri.TransformBegin()
ri.Translate(0, 0, -0.1)
n = 48
radius = 1
min_radius = 0.02
max_radius = 0.075
hyper_length = 0.75
sweep_angle = 90
cylinder_length = 0.25

Create_Lid(n, radius, min_radius, max_radius, hyper_length, cylinder_length, sweep_angle)
ri.Translate(0, 0, 0.125)
ri.Torus(0.9, 0.2, 100, 110.0, 360.0) #Cup Top

ri.TransformEnd()
ri.AttributeEnd()
ri.AttributeEnd()

#################################################################





################ TABLE TOP ####################################


ri.TransformBegin()
# ri.Scale(5, 5, 5)
ri.Translate(0.3, 0.5, 0.3)


ri.Pattern("PxrTexture", "colormap", {"string filename": "bright_wood.tex", "int invertT": [0]})


ri.Pattern("PxrNormalMap", "normalmap", {"filename": "bright_wood_normals.tex"})

ri.Bxdf("PxrSurface", "surf", {
    "reference color diffuseColor": ["colormap:resultRGB"],
    "reference color bumpNormal": ["normalmap:resultN"]
})

make_cuboid(0.5,0.4,0.5)



ri.TransformEnd()   

# #################################################################

# ri.AttributeEnd()


ri.WorldEnd()





ri.End()
