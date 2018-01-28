import cv2
import os
import time
from PIL import Image
from multiprocessing import Process, Queue

def dhash(image, hash_size = 8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = list(image.getdata())

    # Compare adjacent pixels.
    difference = []
    for row in xrange(hash_size):
        for col in xrange(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

def mp4tojpg(filename):
    if os.path.isfile(("/home/hubeen/Prjct/CoMpOvie/mp4/" + str(filename) + ".mp4")):
        vid = cv2.VideoCapture('/home/hubeen/Prjct/CoMpOvie/mp4/' + str(filename) + ".mp4")
        suc, img = vid.read()
        cnt = 0
        suc = True
    
        try:
            os.chdir("/home/hubeen/Prjct/CoMpOvie/jpg")
            os.mkdir(filename)
            
            while suc:
                suc, img = vid.read()
                if img is not None:
                    cv2.imwrite(os.path.join(filename, "frame%d.jpg" % cnt), img)
                    cnt += 1

        except:
            print "wtf"
            return False
    
        print filename + " End" 

    else:
        print "0x90"

def compare(oripath, chagpath):
    ori = Image.open(oripath)
    chag = Image.open(chagpath)
    return (dhash(ori) == dhash(chag))
 
def ls(path='./'):
    stk = []
    if os.path.isdir(path):
        rpath = os.path.join(os.path.abspath(path))
        for files in os.listdir(rpath):
            stk.append(os.path.join(rpath,files))

    return stk

def the_world(orist, chagst, oristt, oried, chagstt, chaged, ret):
    cnt = 0
    a = orist
    b = chagst
    for x in range(oristt, oried):
        for y in range(chagstt, chaged):
            if compare(a[x],b[y]):
                cnt += 1
    ret.put(cnt)
    return

def Analyze(orist,chagst,ret):
    a = orist
    b = chagst
    arsz = len(a)
    brsz = len(b)
    if arsz+brsz >= 2000:
        asz = arsz/1000
        bsz = brsz/1000
        for x in range(0,1000):
            exec("pr" + str(x) + " = Process(target=the_world, args=(a, b, asz*" + str(x)+", asz*"+ str(x+1) + ", bsz*" +str(x)+", bsz*"+str(x+1)+", ret))")
        # start
        for y in range(0,1000):
            exec("pr"+ str(y) +".start()")

        for z in range(0, 1000):
            exec("pr" + str(z) + ".join()")
        ret.put('stop')
    else:
        asz = arsz/100
        bsz = brsz/100
        for x in range(0,100):
            exec("pr" + str(x) + " = Process(target=the_world, args=(a, b, asz*" + str(x)+", asz*"+ str(x+1) + ", bsz*" +str(x)+", bsz*"+str(x+1)+", ret))")
        # start
        for y in range(0,100):
            exec("pr"+ str(y) +".start()")

        for z in range(0, 100):
            exec("pr" + str(z) + ".join()")        
        
        ret.put('stop')
    
    per = 0
    while True:
        tmp = ret.get()
        if tmp == 'stop':
            break
        else:
            per += tmp
    if per >= 10:
        return True
    else:
        return False


ret = Queue()
print "Run ..."
print ""
print "Step 1. jpg file extract in mp4 file"
mp4tojpg("ani_ori")
mp4tojpg("ani_chag")

print "extract done!"
a = sorted(ls('ani_ori'))
b = sorted(ls('ani_chag'))

print "ani_ori.mp4 is frame(" + str(len(a)) + ")"
print "ani_chag.mp4 is frame(" + str(len(b)) + ")"
print ""
print "Step 2. Image Compare"
print "Analyze(ani_ori.mp4, ani_chag.mp4)"

s_time = time.time()

if Analyze(a,b,ret):
    print "Matches."
else:
    print "It does not match."


print 'time = ', time.time()-s_time

