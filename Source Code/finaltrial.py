import sys 
import mysql.connector 
import getopt
import imutils
import cv2
import numpy as np

conn = mysql.connector.connect (host="localhost",user="root", password='root')

def connection():
	if conn.is_connected():
		return True
	else:
		return False
print("starting")

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread('rfoot.jpeg',0)

ret, thresh = cv2.threshold(image,235,255,0)

im2, contours, hierarchy= cv2.findContours(thresh,1,2)
N=len(contours)
print(N)

for cnts in contours:
    cnts = contours[16]
    print(cnts)

    M=cv2.moments(cnts)
    print (M)
    rect=cv2.minAreaRect(cnts)
    print(rect)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    print(box[1])
    print(box[2])
    #print(box[1])
    x,y,w,h=cv2.boundingRect(cnts)
    
    image=cv2.drawContours(image, [box], 0, (0,255,0), 2)

# determine the most extreme points along the contour 
    extLeft = tuple(cnts[cnts[:, :, 0].argmin()][0])
    extRight = tuple(cnts[cnts[:, :, 0].argmax()][0])
    extTop = tuple(cnts[cnts[:, :, 1].argmin()][0])
    extBottom = tuple(cnts[cnts[:, :, 1].argmax()][0])
    
    distance = np.sqrt( (extTop[0] - extBottom[0]**2) + (extTop[1]-extBottom[1]**2 ))
    x,y,w,h = cv2.boundingRect (cnts)
    
    #centx = np.sqrt( ((extTop[0] + extBottom[0])**2))
    #centy = np.sqrt( ((extTop[1] + extBottom[1])**2))
    #print(centx,centy)
    print(distance)

# draw the outline of the object, then draw each of the
# extreme points, where the left-most is red, right-most
# is green, top-most is blue, and bottom-most is teal
    #font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.drawContours(image, [cnts], -1, (0, 255, 255), 2)
    cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
    cv2.circle(image, extRight, 8, (0, 255, 0), -1)
    cv2.circle(image, extTop, 8, (255, 0, 0), -1)
    cv2.circle(image, extBottom, 8, (255, 255, 0), -1)
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    #cv2.putText(image,'Distance: '+str(distance),(10,30), font, 1, (0,0,0),2, cv2.LINE_AA)
 
def insert_values():
		db_conn=mysql.connector.connect(host="localhost",db="FootwearSizes",user="root",password='root')
		if db_conn.is_connected():
			mycursor= db_conn.cursor()

			query = "INSERT INTO Size(slno, size) VALUES (%s,%s) "
			slno = input("\n Enter slno:\n")
			size = input("\n Enter size:\n")
			value=(slno,size)
			mycursor.execute(query,value)
			db_conn.commit()
			print("sucessfully inserted")

		else:
			print("Couldn't connect to mysql server")
		db_conn.close()

def insert_values1():
		db_conn=mysql.connector.connect(host="localhost",db="FootwearSizes",user="root",password='root')
		if db_conn.is_connected():
				mycursor= db_conn.cursor()

				query = "INSERT INTO STD_SIZE(id, size, ussize,uksize, eurosize) VALUES (%s,%s,%s,%s,%s)"
				id= input("\n Enter id:\n")
				size = input("\n Enter size:\n")
				ussize= input("\n Enter the ussize\n")
				uksize= input("\n Enter the uksize\n")
				eurosize= input("\n Enter the eurosize\n")
				value=(id,size,ussize,uksize,eurosize)
				mycursor.execute(query,value)
				db_conn.commit()
				print("sucessfully inserted")
		else:
				print("Couldn't connect to mysql server")
		db_conn.close()

#insert_values()
#insert_values1()


def display_values():
	db_conn=mysql.connector.connect(host="localhost",db="FootwearSizes",user="root",password='root')
	if db_conn.is_connected():
		mycursor= db_conn.cursor()

		query="SELECT * FROM Size"
		query="SELECT * FROM STD_SIZE"

		mycursor.execute(query)
		
		result=mycursor.fetchall()
		for x in result:
			print(x)
		
	else:
		print("Couldn't connect to mysql server")
	db_conn.close()

display_values();
cv2.imshow("image",image)
cv2.imshow("thershold",thresh)
cv2.waitKey(0)



