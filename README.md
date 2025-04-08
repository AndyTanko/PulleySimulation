# The pulley simulation
## Using OOP to combine objects with textures:

I have created a class for storing objects in a different manner to the inbuilt composite() function in vPython, as it doesn't allow for nested compositing, or for textured objects to be composited. It is a work in progress. Currently it is impossible to replicate the behavior of a composite object in full, as decorators such as @property aren't being parsed by the web VPython, which is the focus.