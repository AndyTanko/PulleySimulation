#Web VPython 3.2
from vpython import *
v = vector
class ObjectGroup:
    def __init__(self, objects, origin=None):
        """
        Create a group of objects that can be manipulated together.
        This is necessary because nested compounding is disallowed in vPython
        Parameters:
        *objects: VPython objects to include in the group
        origin: Optional vector to use as the reference point (defaults to first object's position)
        """
        if isinstance(objects,list):
            self.objects = objects
        else:
            self.objects = list(objects)
        
        # Set origin to the first object's position if not specified
        if origin is None and len(self.objects) > 0:
            self._origin = vector(self.objects[0].pos)
        else:
            self._origin = vector(origin) if origin else vector(0, 0, 0)
            
        # Store initial offsets of each object relative to the origin
        self.offsets = []
        for obj in self.objects:
            self.offsets.append(vector(obj.pos) - self._origin)

    def getpos(self):
        """Return the current position (origin) of the group"""
        return self._origin
    
    def setpos(self, new_pos):
        """
        Set a new position for the group, moving all objects accordingly
        """
        # Calculate the displacement vector
        #displacement = vector(new_pos) - self._origin
        
        # Update the origin
        self._origin = vector(new_pos)
        
        # Move each object by the displacement
        for i, obj in enumerate(self.objects):
            obj.pos = self._origin + self.offsets[i]

    def add(self, obj):
        """Add a new object to the group"""
        self.objects.append(obj)
        self.offsets.append(vector(obj.pos) - self._origin)
    
    def remove(self, obj):
        """Remove an object from the group"""
        if obj in self.objects:
            idx = self.objects.index(obj)
            self.objects.pop(idx)
            self.offsets.pop(idx)
    
    def rotate(self, angle, axis=None, origin=None):
        """
        Rotate all objects around an axis through the origin
        
        Parameters:
        angle: Rotation angle in radians
        axis: Axis of rotation (defaults to z-axis)
        origin: Point to rotate around (defaults to group's origin)
        """
        if axis is None:
            axis = vector(0, 0, 1)
        
        rot_origin = origin if origin is not None else self._origin
        
        for i, obj in enumerate(self.objects):
            # Update the offset vector by rotating it
            self.offsets[i] = rotate(self.offsets[i], angle=angle, axis=axis)
            
            # Update the object's position
            obj.pos = rot_origin + self.offsets[i]
            
            # Rotate the object itself if it has a rotate method
            if hasattr(obj, 'rotate'):
                obj.rotate(angle=angle, axis=axis, origin=rot_origin)



## Pulley definition
rotation_center = v(0.5,0,0)

# Create pulley design
def Pulley():
    triangle1 = pyramid(pos=v(0, -0.2, 0), axis=v(1.5, 0, 0), height = 0.2, length = 1, color=color.gray(0.4))
    triangle2 = triangle1.clone(pos=v(0,0.2,0))
    cyl1 = cylinder(pos=triangle1.pos+v(0.9,-0.1,0), axis = v(0,0.6,0),radius = 0.01)
    cyl2 = cylinder(pos=v(0.9,-0.1,0),axis=v(0,0.2,0), radius=0.4, color=color.orange)

    #Create pulley
    cekrk = compound([triangle1, triangle2, cyl1, cyl2], origin=v(0,0,0))
    return cekrk


#Create the sliding surface and the wall the pulley2 attaches to
def Environment():
    earth = box(pos=v(0,0,-0.05),size=v(10,10,0.1),texture=textures.gravel)
    wall = box(pos=v(5.05,0,2.5),size=v(0.1,10,5),texture=textures.wood)
    return ObjectGroup([earth,wall],origin=v(-5,-5,0))

def ArcExtrusion(shape, radius, center, axis, angle):
    output = extrusion(
    path = paths.arc(radius=radius,angle1=0, angle2=angle),
    color = color.black,
    shape=shape,
    )
    output.pos=center
    output.up = axis
    return output


#line1 = cylinder(radius=0.01,color=color.black, axis=v(-5,0,0),pos=cekrk2.pos+v(-0.5,0,0.4))
#line2=line1.clone(pos=line1.pos-v(0,0,0.8))
#line2.axis=v(-4,0,0)
# Measuring ztick
#box(pos=bigbox.pos+v(0,0,2.6),size=v(15,0.5,0.2), color=color.red)

def toggle_run_pause(b):
    global running
    running = not running
    # Update button text accordingly
    b.text = "Pause" if running else "Run"
def reset():
    global initial_pos
    apparatus.setpos(initial_pos)
    line1.axis=v(-4.1,0,0)
    line2.axis=v(-3.2,0,0)
    line3.pos=pulley1.pos+v(0.5,0,0)
    line3.axis=v(0,0,-0.5)
    smallbox.pos=line3.pos-v(0,0,1)
    global acceleration, vM, vm
    acceleration=0
    vM = 0
    vm=0
def update_M(s):
    global M
    try:
        M = float(s.text)
        if M <= 0:
            M = 0.1  # Prevent division by zero
            s.text = str(M)
        status_label.text = f"Current values: M = {M} kg, m = {m} kg, μ = {mu}"
        reset()  # Reset simulation with new parameters
    except ValueError:
        status_label.text = "Please enter a valid number for M"

def update_m(s):
    global m
    try:
        m = float(s.text)
        if m < 0:
            m = 0
            s.text = str(m)
        status_label.text = f"Current values: M = {M} kg, m = {m} kg, μ = {mu}"
        reset()  # Reset simulation with new parameters
    except ValueError:
        status_label.text = "Please enter a valid number for m"

def update_mu(s):
    global mu
    try:
        mu = float(s.text)
        if mu < 0:
            mu = 0
            s.text = str(mu)
        status_label.text = f"Current values: M = {M} kg, m = {m} kg, μ = {mu}"
        reset()  # Reset simulation with new parameters
    except ValueError:
        status_label.text = "Please enter a valid number for μ"

def make_caption_layout():
    # Create a two-column layout
    scene.caption = "<div style='display: flex; width: 100%;'>"
    
    # Left column - inputs
    scene.caption += "<div style='flex: 1;'>"
    scene.caption += "<h2>Physics Simulation Controls</h2>"
    
    # Run/pause and reset buttons
    pause_button = button(text="Pause", bind=toggle_run_pause)
    button(text="Reset", bind=reset)
    scene.append_to_caption("<br><br>")
    
    # Input for big box mass (M)
    scene.append_to_caption("<b>Big box mass (M):</b> ")
    M_input = winput(text=str(M), bind=update_M)
    scene.append_to_caption(" kg<br>")
    
    # Input for small box mass (m)
    scene.append_to_caption("<b>Small box mass (m):</b> ")
    m_input = winput(text=str(m), bind=update_m)
    scene.append_to_caption(" kg<br>")
    
    # Input for friction coefficient (mu)
    scene.append_to_caption("<b>Friction coefficient (μ):</b> ")
    mu_input = winput(text=str(mu), bind=update_mu)
    scene.append_to_caption("<br><br>")
    
    # Status label for current values and notifications
    status_label = wtext(text=f"Current values: M = {M} kg, m = {m} kg, μ = {mu}")
    scene.append_to_caption("</div>")
    
    # Right column - camera controls
    scene.append_to_caption("<div style='flex: 1;'>")
    scene.append_to_caption("""
    <h3>Camera Controls:</h3>
    <ul>
        <li>W/A/S/D - Move camera up/left/down/right</li>
        <li>Arrow keys - Rotate camera view</li>
        <li>Q/E - Roll camera</li>
    </ul>
    """)
    scene.append_to_caption("</div></div>")
    
    return status_label, pause_button

#Implement camera controls
move_step = 0.5       # How far the camera moves per key press
rotate_step = 0.1     # Radian rotation step
def control_camera(evt):
    global move_step, rotate_step
    
    # Calculate camera's current directions
    forward = norm(scene.camera.axis)                        # Viewing direction
    right = norm(cross(forward, scene.up))                     # Right vector
    up = norm(scene.up)                                        # Up vector

    # --- Move Camera (WASD: relative to camera orientation) ---
    if evt.key == 'w':
        scene.camera.pos += move_step * up              # Move forward
    elif evt.key == 's':
        scene.camera.pos -= move_step * up              # Move backward
    elif evt.key == 'a':
        scene.camera.pos -= move_step * right                # Move left
    elif evt.key == 'd':
        scene.camera.pos += move_step * right                # Move right

    # --- Rotate Camera (Arrow keys for pitch and yaw) ---
    # Pitch: Up/Down arrows (rotate around the camera's right vector)
    if evt.key == 'down':
        scene.camera.axis = rotate(scene.camera.axis, angle=-rotate_step, axis=right)
        scene.up = rotate(scene.up, angle=-rotate_step, axis=right)
    elif evt.key == 'up':
        scene.camera.axis = rotate(scene.camera.axis, angle=rotate_step, axis=right)
        scene.up = rotate(scene.up, angle=rotate_step, axis=right)

    # Yaw: Left/Right arrows (rotate around the camera's up vector)
    elif evt.key == 'right':
        scene.camera.axis = rotate(scene.camera.axis, angle=-rotate_step, axis=up)
        # For yaw, we typically keep the up vector fixed
    elif evt.key == 'left':
        scene.camera.axis = rotate(scene.camera.axis, angle=rotate_step, axis=up)
    
    # --- Roll Camera (Q/E keys: roll around the camera's forward vector) ---
    if evt.key == 'q':
        scene.up = rotate(scene.up, angle=-rotate_step, axis=forward)
    elif evt.key == 'e':
        scene.up = rotate(scene.up, angle=rotate_step, axis=forward)



if __name__ == "__main__":
    scene = canvas(background=v(0.6,0.6,0.6), width=800, height = 600)
    scene.bind('keydown', control_camera)
    # Lighting settings
    scene.lights = []  # Remove default lights
    # Simulate diffuse lighting using multiple soft distant lights
    for i in (-1,1):
        for j in (-1,1):
            for k in (-1,1):
                distant_light(direction=v(i,j,k), color=color.white * 0.3)
    scene.caption = "<h2>Physics Simulation Controls</h2>"
    # Simulation parameters:
    g=9.81
    dt=0.01
    M = 100 #kg
    m = 1 #kg
    mu = 0.05 # friction coefficient
    running = True #simulation stoppage
    acceleration = 0
    vM = 0
    vm = 2*vM
# Run/pause and reset buttons
    
    status_label, pause_button = make_caption_layout()
    scene.append_to_caption("<br><br>")

    
    # Create the run/pause button
    button(text="Pause", bind=toggle_run_pause)
    button(text= 'Reset', bind=reset)
    scene.append_to_caption("\n\n")  # Optional: add spacing
    #Create pulley
    pulley1 = Pulley()
    #Create the second pulley and invert it
    pulley2 = pulley1.clone(pos=v(5,0,4.5))
    pulley2.rotate(axis=v(0,0,1), angle=pi)
    env = Environment() # ObjectGroup object
    bigbox = box(pos=env.getpos()+v(2.5,5,2.5),size=v(5,5,5), axis=v(1,0,0), texture=textures.granite)
    pulley1.pos=bigbox.pos+v(2.5,0,1.2)
    arc1 = ArcExtrusion(shape=shapes.circle(radius=0.01),radius=0.4,center=pulley1.pos+v(0.9,0,0),axis=v(0,1,0), angle=pi/2)
    apparatus = ObjectGroup([arc1,bigbox,pulley1])
    arc2 = ArcExtrusion(shape=shapes.circle(radius=0.01),radius=0.4,center=pulley2.pos-v(0.9,0,0),axis=v(0,1,0),angle=pi)
    initial_pos = apparatus.getpos()
    arc1.rotate(angle=pi,axis=v(0,1,0))
    arc2.rotate(angle=-pi/2,axis=v(0,1,0))
    line1 = cylinder(pos=pulley2.pos-v(0.9,0,-0.4),axis=v(-4.1,0,0),radius=0.01, color=color.black)
    line2 = cylinder(pos=pulley2.pos-v(0.9,0,0.4),axis=v(-3.6,0,0),radius=0.01, color=color.black)
    line3 = cylinder(pos=pulley1.pos+v(0.5,0,0),axis=v(0,0,-0.5),radius=0.01, color=color.black)
    smallbox = box(pos=line3.pos-v(0,0,1),color=color.gray(0.2))
    bigbox_label = label(pos=bigbox.pos+v(0,0,2.5), text=f"M = {M} kg", height=16, box=False, opacity=0)
    smallbox_label = label(pos=smallbox.pos+v(0,0,-0.5), text=f"m = {m} kg", height=16, box=False, opacity=0)
    
    # Add velocity labels
    bigbox_vel_label = label(pos=bigbox.pos+v(0,2,2.5), text=f"v = 0 m/s", height=16, box=False, opacity=0, color=color.red)
    smallbox_vel_label = label(pos=smallbox.pos+v(0,0,-0.8), text=f"v = 0 m/s", height=16, box=False, opacity=0, color=color.red)
  

    while(True):
        rate(30)
        if(running):

            if smallbox.pos.z>0.5:
                bigbox_label.text = f"M = {M} kg"
                bigbox_label.pos = bigbox.pos + v(0,0,2.5)
                
                smallbox_label.text = f"m = {m} kg"
                smallbox_label.pos = smallbox.pos + v(0,0,-0.5)
                
                # Update velocity labels
                bigbox_vel_label.text = f"v = {vM:.2f} m/s"
                bigbox_vel_label.pos = bigbox.pos + v(0,2,2.5)
                
                smallbox_vel_label.text = f"v = {vm:.2f} m/s"
                smallbox_vel_label.pos = smallbox.pos + v(0,0,-0.8)
                force = m*g
                friction = mu*m*acceleration
                tension = force-2*m*acceleration-friction
                acceleration = 2*tension/(M+m)
                # Calculate speeds
                vM = vM + acceleration*dt
                vm = 2*vM
                line3.pos=line3.pos+v(vM*dt,0,0) #move in x direction
                line3.axis=line3.axis-v(0,0,vm*dt) #move in -z direction
                line2.axis=line2.axis+v(vM*dt,0,0)
                apparatus.setpos(apparatus.getpos()+v(vM*dt,0,0))
                smallbox.pos = smallbox.pos+v(vM*dt,0,-vm*dt)
            else:
                toggle_run_pause(pause_button)