import time
import random
import drawSample
import math
import _tkinter
import sys
import loader
import sys
import cPickle
import os.path
import Tkinter as tk
import sys
import Tkinter as tk

from PIL import ImageFilter
import TileServer
import geoclass

debug = 0  # debug 1 or 2 means using a very simplified setup
verbose=0  # print info (can be set on command line)
versionNumber = 1.0
zoomLevel = 18
loadStateFile = 'classifier.state'  # default file for classifier data

documentation = \
"""
  This program is a stub for your COMP 417 robotics assignment.
"""




##########################################################################################
#########  Do non-stardard imports and print helpful diagnostics if necessary ############
#########  Look  for "real code" below to see where the real code goes        ############
##########################################################################################


missing = []
fix = ""

try: 
    import scipy
    from scipy import signal
except ImportError: 
    missing.append( " scipy" )
    fix = fix +  \
        """
        On Ubuntu linux you can try: sudo apt-get install python-numpy python-scipy python-matplotlib 
        On OS X you can try:  
              sudo easy_install pip
              sudo pip install  scipy
        """
try: 
    import matplotlib
    import matplotlib.pyplot as plt
except ImportError: 
    missing.append( " matplotlib" )
    fix = fix +  \
        """
        On Ubuntu linux you can try: sudo apt-get install python-matplotlib
        On OS X you can try:  
              sudo easy_install pip
              sudo pip install matplotlib
        """

try: 
    import numpy as np
except ImportError: 
     missing.append( " numpy " )
     fix = fix + \
        """
          sudo easy_install pip
          sudo pip install numpy
        """
try: 
    from sklearn.decomposition import PCA
    from sklearn.svm import SVC
except ImportError: 
     missing.append( " scikit-learn " )
     fix = fix + \
        """
          sudo easy_install pip
          sudo pip install scikit-learn
        """
try: 
    from PIL import Image
    from PIL import ImageTk
    from PIL import ImageDraw
except ImportError: 
     missing.append( " PIL (more recently known as pillow) " )
     fix = fix + \
        """
          sudo easy_install pip
          sudo pip install pillow
        """

if missing:
     print "*"*60
     print "Cannot run due to missing required libraries of modules."
     print "Missing modules: "
     for i in missing: print "    ",i
     print "*"*60
     print fix
     sys.exit(1)

version = "Greg's drone v%.1f  $HGdate: Fri, 24 Nov 2017 09:38:37 -0500 $ $Revision: f330eb3280c9 Local rev 2 $" % versionNumber

print version
print " ".join(sys.argv)
##########################################################################################
#########     Parse command-line arguments   #############################################
##########################################################################################
while len(sys.argv)>1:
    if len(sys.argv)>1 and sys.argv[1]=="-v":
        verbose = verbose+1
        del sys.argv[1]
    elif len(sys.argv)>1 and sys.argv[1]=="-load":
        if len(sys.argv)>2 and not sys.argv[2].startswith("-"):
            loadStateFile = sys.argv[2]
            del sys.argv[2]
        else:
            loadStateFile = 'classifier.state'
        del sys.argv[1]
    elif len(sys.argv)>1 and sys.argv[1] in ["-h", "-help", "--help"]: # help
        print documentation
        sys.argv[1] = "-forceusagemesasge"
    else:
        print "Unknown argument:",sys.argv[1]
        print "Usage: python ",sys.argv[0]," [-h (help)][-v]    [-f TRAININGDATADIR] [-t TESTDIR] [-load [STATEFILE]]"
        sys.exit(1)


##########################################################################################
#########  "real code" is here, at last!                                      ############
##########################################################################################
# my position
tx,ty = 0.5,0.5 # This is the translation to use to move the drone
oldp = [tx,ty]  # Last point visited

fill = "white"
image_storage = [ ] # list of image objects to avoid memory being disposed of

def autodraw():
    """ Automatic draw. """
    draw_objects()
    tkwindow.canvas.after(25, autodraw)

def draw_objects():
    """ Draw target balls or stuff on the screen. """
    global tx, ty, maxdx, maxdy, unmoved, brownian
    global oldp
    global grid,last_grid_center,dist_to_goal,objective
    global objectId
    global ts # tileServer
    global actual_pX, actual_pY
    global fill
    global scalex, scaley  # scale factor between out picture and the tileServer
    global road
    global stop,distance,newtiles,totaltiles,maxdistance

    if stop: return #end of simulation
    v=20
    brownian=1 #brownian or smart algorithm
    max_distance=25000
    #tkwindow.canvas.move( objectId, int(tx-MYRADIUS)-oldp[0],int(ty-MYRADIUS)-oldp[1] )
    if unmoved: 
        # initialize on first time we get here
        unmoved=0
        tx,ty = 0,0
        last_grid_center=[10,10]
        objective=[sx+10,sy+10]
        dist_to_goal=100
        road=[]
        distance =0
        totaltiles=0

    else: 
        # draw the line showing the path
        tkwindow.polyline([oldp,[oldp[0]+tx,oldp[1]+ty]], style=5, tags=["path"]  )
        tkwindow.canvas.move( objectId, tx,ty )

    #save the previous drone position
    oldposx=int(oldp[0]*scalex/256)
    oldposy=int(oldp[1] *scaley/ 256)
    # update the drone position
    oldp = [oldp[0]+tx,oldp[1]+ty]
    grid_posx= int(oldp[0]*scalex/256)
    grid_posy = int(oldp[1] *scaley/ 256)

    #count the number of tiles visited
    if not(oldposx==grid_posx and oldposy==grid_posy):
        totaltiles+=1

    #Only run the classification on new cells
    if grid[grid_posx,grid_posy]==0:
        # map drone location back to lat, lon
        # This transforms pixels to WSG84 mapping, to lat,lon
        lat,lon = ts.imagePixelsToLL( actual_pX, actual_pY, zoomLevel,  oldp[0]/(256/scalex), oldp[1]/(256/scaley) )

        # get the image tile for our position, using the lat long we just recovered
        im, foox, fooy, fname = ts.tiles_as_image_from_corr(lat, lon, zoomLevel, 1, 1, 0, 0)

        # Use the classifier here on the image "im"
        im_patch = np.asarray(im, dtype=np.float32).flatten()
        type=geoclass.classifyOne(pca, clf, im_patch,classnames)
        grid[grid_posx, grid_posy]=type[0]+1
        # This is the drone, let's move it around
        tkwindow.canvas.itemconfig(objectId, tag='userball', fill=fill)
        tkwindow.canvas.drawn = objectId

        #  Take the tile and shrink it to go in the right place
        im = im.resize((int(im.size[0]/scalex),int(im.size[1]/scaley)))
        im.save(r"C:\Users\nikit\OneDrive\Documents\Mcgill\COMP 417\asst4\tmp\locationtile.gif")
        photo = tk.PhotoImage(file=r"C:\Users\nikit\OneDrive\Documents\Mcgill\COMP 417\asst4\tmp\locationtile.gif" )
        tkwindow.image = tkwindow.canvas.create_image( 256/scalex*int(oldp[0]/(256/scalex)), 256/scalex*int(oldp[1]/(256/scalex)), anchor=tk.NW, image=photo, tags=["tile"] )
        image_storage.append( photo ) # need to save to avoid garbage collection

        # This arrenges the stuff being shown
        tkwindow.canvas.lift( objectId )
        tkwindow.canvas.tag_lower( "tile" )
        tkwindow.canvas.tag_lower( "background" )
        tkwindow.canvas.pack()

    # Code to move the drone can go here
    # Move a small amount by changing tx,ty


    #######################################
    #Brownian algorithm
    #######################################
    if brownian:
        urban = 1
        #Check if current cell is urban. If it is go back
        if grid[grid_posx, grid_posy] == 3:
            draw = ImageDraw.Draw(bigpic)
            xt, yt = grid_posx, grid_posy
            tkwindow.canvas.create_rectangle(256 / scalex * xt, 256 / scalex * yt, 256 / scalex * (xt + 1),
                                             256 / scalex * (yt + 1), fill='red',stipple='gray25')
            tx = -1.1 * tx
            ty = -1.1 * ty
            distance += np.sqrt(tx ** 2 + ty ** 2)
            urban=0

        #choose a random direction and check if the destination is urban
        #if it is choose an other destination
        while urban:
            theta = np.random.uniform(0, 2 * np.pi)
            tx = v * np.cos(theta)
            ty = v * np.sin(theta)
            grid_posx = int((oldp[0] + tx) / 256 * scalex)
            grid_posy = int((oldp[1] + ty) / 256 * scaley)
            if grid[grid_posx, grid_posy] == 3:
                urban = 1
            else:
                urban = 0
        distance += np.sqrt(tx ** 2 + ty ** 2)
        if distance >max_distance:
            stop=1
    else:
    #######################################
    # Curious algorithm
    #######################################

        # Check if current cell is urban. If it is go back
        if grid[grid_posx,grid_posy]==3:
            xt,yt = grid_posx,grid_posy
            tkwindow.canvas.create_rectangle(256 / scalex * xt, 256 / scalex * yt, 256 / scalex * (xt + 1),
                                           256 / scalex * (yt + 1), fill='red',stipple='gray25')
            objective=last_grid_center
            road=[]
        else:
            #remember last non-urban cell
            last_grid_center=[(grid_posx+0.5)* 256/scalex,(grid_posy+0.5)* 256/scaley]

        #if objective achieved choose next objective.
        #  If the road is empty-> destination achieved->run search
        if dist_to_goal<2*v:

            if road==[]:
                start=[grid_posx,grid_posy]
                road=find_objective(grid_posx,grid_posy)
            objective=[(road[-1][0]+0.5)*256/scalex,(road[-1][1]+0.5)*256/scaley]
            road.pop(-1)

        #move towards the objective
        lx=objective[0]-oldp[0]
        ly=objective[1]-oldp[1]
        dist_to_goal= np.sqrt(ly**2+lx**2)
        lx=lx/dist_to_goal
        ly=ly/dist_to_goal
        tx=v*lx
        ty=v*ly
        distance+=np.sqrt(tx**2+ty**2)

    #stop when no more empty cells or max distance reached
    if stop:
        tx=0
        ty=0
        statistics()

def statistics():
    """Count the number of tiles for each type of terrain and draw them on the map"""
    global grid,totaltiles,distance

    urban=0
    arable=0
    water=0
    desert=0
    undiscovered=0
    discovered=0
    for i in range(tilesX):
        for j in range(tilesY):
            if grid[i,j]==1:
                arable+=1
                tkwindow.canvas.create_rectangle(256 / scalex * i, 256 / scalex * j, 256 / scalex * (i + 1),
                                                 256 / scalex * (j + 1), fill='green', stipple='gray25')
            elif grid[i,j]==4:
                water+=1
                tkwindow.canvas.create_rectangle(256 / scalex * i, 256 / scalex * j, 256 / scalex * (i + 1),
                                                 256 / scalex * (j + 1), fill='blue', stipple='gray25')
            elif grid[i,j]==3:
                urban+=1
            elif grid[i,j]==2:
                desert+=1
                tkwindow.canvas.create_rectangle(256 / scalex * i, 256 / scalex * j, 256 / scalex * (i + 1),
                                                 256 / scalex * (j + 1), fill='yellow', stipple='gray25')
            elif grid[i,j]==0:
                undiscovered+=1
            discovered=tilesX*tilesY-undiscovered

    arable =float(arable)/discovered
    water = float(water) / discovered
    urban = float(urban)/ discovered
    desert = float(desert) / discovered

    print("arable :", arable,)
    print("water :", water,)
    print("urban :", urban,)
    print("desert :", desert,)
    print("undiscovered :", undiscovered)
    print("discovered :", discovered)
    print("total tiles", totaltiles)
    print("total distance", distance)


def find_objective(startx, starty):
    """Breadth search first algorithm looking for the closest empty cell"""
    global grid
    global stop

    parents = [[[-1,-1] for x in range(tilesX)] for y in range(tilesY)]
    visited = np.zeros((tilesX, tilesY))
    queue=[]
    queue.append([startx,starty])
    goal=[-1,-1]

    visited[startx,starty]=1
    parents[startx][starty][0]=startx
    parents[startx][starty][1] =starty
    iter=0

    while not queue==[]:
        #Add node to the queue if it is not urban and not yet visited.
        #if it is unknown (grid==0) then it becomes the goal.
        #push the drone down by first looking at the cell under the current
        node=queue[0]
        visited[node[0],node[1]]=1
        queue.pop(0)
        down = grid[node[0], node[1] + 1]
        right = grid[node[0]+1, node[1]]
        left = grid[node[0]-1, node[1]]
        up = grid[node[0], node[1]-1]

        if down==0:
            parents[node[0]][node[1] + 1]=node
            goal=[node[0], node[1] + 1]
            break
        elif not down==3 and not visited[node[0], node[1] + 1]:
            queue.append([node[0], node[1] + 1])
            parents[node[0]][node[1] + 1] = node
        if right==0:
            parents[node[0]+1][node[1]]=node
            goal=[node[0]+1, node[1]]
            break
        elif not right == 3 and not visited[node[0]+1, node[1]]:
            queue.append([node[0]+1, node[1]])
            parents[node[0] + 1][node[1]] = node
        if left==0:
            parents[node[0]-1][node[1]]=node
            goal=[node[0]-1, node[1]]
            break
        elif not left == 3 and not visited[node[0]-1, node[1]]:
            queue.append([node[0]-1, node[1]])
            parents[node[0] - 1][node[1]] = node
        if up==0:
            parents[node[0]][node[1]-1]=node
            goal=[node[0], node[1]-1]
            break
        elif not up==3 and not visited[node[0], node[1] - 1]:
            queue.append([node[0], node[1] - 1])
            parents[node[0]][node[1] - 1] = node
        iter+=1
        if iter>10000:
            break
    if goal==[-1,-1]:
        print("no empty cell found")
        goal=[startx,starty]
        stop=1

    node=goal
    path=[goal]
    parent=parents[goal[0]][goal[1]]
    iter=0

    #find the path to the goal
    while not (parent[0]==node[0] and parent[1]==node[1]):
        node=parents[node[0]][node[1]]
        path.append(node)
        parent=parents[node[0]][node[1]]
        iter+=1
        if iter>200:
            print("path not found")
            stop=1
            break
    return path

# MAIN CODE. NO REAL NEED TO CHANGE THIS

ts = TileServer.TileServer()

# Top-left corner of region we can see

lat, lon = 45.44203, -73.602995    # verdun

# Size of region we can see, measure in 256-goepixel tiles.  Geopixel tiles are what
# Google maps, bing, etc use to represent the earth.  They make up the atlas.
#
tilesX = 20
tilesY = 20
tilesOffsetX = 0
tilesOffsetY = 0
grid=np.zeros((tilesX+2, tilesY+2))
for i in range(tilesX+2):
    grid[i,tilesY]=3
    grid[i,tilesY+1]=3
for i in range(tilesY+2):
    grid[tilesX,i]=3
    grid[tilesX+1,i]=3
# Get tiles to cover the whole map (do not really need these at this point, be we cache everything 
# at the beginning this way, and can draw it all.
# using 1,1 instead of tilesX, tilesY to see just the top left image as a check
#
#actual, actual_pX, actual_pY, fname = ts.tiles_as_image_from_corr(lat, lon, zoomLevel, 1, 1, tilesOffsetX, tilesOffsetY)
actual, actual_pX, actual_pY, fname = ts.tiles_as_image_from_corr(lat, lon, zoomLevel, tilesX, tilesY, tilesOffsetX, tilesOffsetY)


# Rather than draw the real data, we can use a white map to see what is unexplored.
bigpic = Image.new("RGB", (256*tilesX, 256*tilesY), "white")
bigpic.paste(actual, (0,0))  # paste the actual map over the pic.

# How to draw a rectangle.
# You should delete or comment out the next 3 lines.
#draw = ImageDraw.Draw(bigpic)
#xt,yt = 0,0
#draw.rectangle(((xt*256-1, yt*256-1), (xt*256+256+1, yt*256+256+1)), fill="red")

# put in image

# Size of our on-screen drawing is arbitrarily small
myImageSize = 1024
scalex = bigpic.size[0]/myImageSize  # scale factor between our picture and the tileServer
scaley = bigpic.size[1]/myImageSize  # scale factor between our picture and the tileServer
im = bigpic.resize((myImageSize,myImageSize))
im = im.filter(ImageFilter.BLUR)
im = im.filter(ImageFilter.BLUR)

im.save("mytemp.gif") # save the image as a GIF and re-load it does to fragile nature of Tk.PhotoImage
tkwindow  = drawSample.SelectRect(xmin=0,ymin=0,xmax=1024 ,ymax=1024, nrects=0, keepcontrol=0 )#, rescale=800/1800.)
root = tkwindow.root
root.title("Drone simulation")

# Full background image
photo = tk.PhotoImage(file="mytemp.gif")
tkwindow.imageid = tkwindow.canvas.create_image( 0, 0, anchor=tk.NW, image=photo, tags=["background"] )
image_storage.append( photo )
tkwindow.canvas.pack()

tkwindow.canvas.pack(side = "bottom", fill = "both",expand="yes")


MYRADIUS = 7
MARK="mark"

# Place our simulated drone on the map
sx,sy=600,640 # over the river
#sx,sy = 220,280 # over the canal in Verdun, mixed environment
oldp = [sx,sy]
objectId = tkwindow.canvas.create_oval(int(sx-MYRADIUS),int(sy-MYRADIUS), int(sx+MYRADIUS),int(sy+MYRADIUS),tag=MARK)
unmoved = 1
stop=0

# initialize the classifier
# We can use it later using these global variables.
#
pca, clf, classnames = geoclass.loadState( loadStateFile, 1.0)

# launch the drawing thread
autodraw()

#Start the GUI
root.mainloop()
