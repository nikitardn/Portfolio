import sys
import PIL
import PIL.Image

# binarize image.
# map everything below 200 to zero
def remap(v): 
  if v>254: return 255
  return 0


def inRect(p,rect,dilation):
   """ Return 1 in p is inside rect, dilated by dilation (for edge cases). """
   if p[0]<rect[0]-dilation: return 0
   if p[1]<rect[1]-dilation: return 0
   if p[0]>rect[2]+dilation: return 0
   if p[1]>rect[3]+dilation: return 0
   return 1

def imageToRects(imagename):
    """ Read an image and return the size and a list of rectangles that cover it. 
        The rectangles might overlap one another.
        Returns:  ( (sizex,sizey), rectlist )
        Scan across the domain. Once we find we are in an obstacle, start growing a rectangle until
        we are in free space again.
    """
    obstacles = []
    im = PIL.Image.open(imagename).convert("L")
    XMAX = im.size[0]
    YMAX = im.size[1]

    im = im.point( remap )
    obdata = list( im.getdata() )

    print "Converting image to obstacle map."
    im = im.point( remap )
    # Convert an image into a set of rectangular obstacles
    y=0
    while y<YMAX:
       x=0
       if y%25==0: print "%.1f"%(float(y)/YMAX*100),"%.....     \r",
       sys.stdout.flush()
       while x<XMAX:
          # see if point already in some rectangle
          skip=0
          for o in obstacles:
              if inRect((x,y),o,0): 
                  skip=1
                  break
          if skip:
              x = x+1
              continue
          if obdata[x+y*XMAX] != 255:  # dtart with a non-white point
              dx=0
              dy=0
              ok_dx = dx
              ok_dy = dy
              xy = 0
              bad = 0
              while 1:
                  # incrementally grow a rectangle until it contains a white point
                  # we grow a bit in the x direction, then a bit in the y, back and forth.
                  # if we find white, we back up and try the other axis.
                  e = im.crop( (x,y,x+dx,y+dy) ).getextrema()
                  if e and e[1] == 255:
                     bad = bad + 1
                     # revert to last good state
                     dx = ok_dx
                     dy = ok_dy
                     if bad > 1: break
                  else:
                     # acceptable
                     bad = 0
                     ok_dx = dx
                     ok_dy = dy
                     #obstacles.append( [ x,y,x+ok_dx+1,y+ok_dy+1 ] )
                     #redraw()
                     #canvas.events()
                  if xy: dx=dx+1
                  else: dy=dy+1
                  if not bad: xy = not xy
              obstacles.append( [ x,y,x+ok_dx+1,y+ok_dy+1 ] )
              x = x+ok_dx
          x = x+1
       y = y+1
    print "Converting image to obstacle map, done."
    return ( im.size, obstacles )


if __name__ == '__main__':
    import sys
    s,rects = imageToRects(sys.argv[1])
    for r in rects:
        print r
