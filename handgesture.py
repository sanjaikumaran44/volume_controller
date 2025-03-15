{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "# Imports\n",
    "import numpy as np\n",
    "import cv2\n",
    "\n",
    "import math\n",
    "import pyautogui"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "# Open Camera\n",
    "capture = cv2.VideoCapture(0)\n",
    "\n",
    "while capture.isOpened():\n",
    "    \n",
    "    # Capture frames from the camera\n",
    "    ret, frame = capture.read()\n",
    "    \n",
    "    # Get hand data from the rectangle sub window   \n",
    "    cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)\n",
    "    crop_image = frame[100:300, 100:300]\n",
    "    \n",
    "    # Apply Gaussian blur\n",
    "    blur = cv2.GaussianBlur(crop_image, (3,3), 0)\n",
    "    \n",
    "    # Change color-space from BGR -> HSV\n",
    "    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)\n",
    "    \n",
    "    # Create a binary image with where white will be skin colors and rest is black\n",
    "    mask2 = cv2.inRange(hsv, np.array([2,0,0]), np.array([20,255,255]))\n",
    "    \n",
    "    # Kernel for morphological transformation    \n",
    "    kernel = np.ones((5,5))\n",
    "    \n",
    "    # Apply morphological transformations to filter out the background noise\n",
    "    dilation = cv2.dilate(mask2, kernel, iterations = 1)\n",
    "    erosion = cv2.erode(dilation, kernel, iterations = 1)    \n",
    "       \n",
    "    # Apply Gaussian Blur and Threshold\n",
    "    filtered = cv2.GaussianBlur(erosion, (3,3), 0)\n",
    "    ret,thresh = cv2.threshold(filtered, 127, 255, 0)\n",
    "\n",
    "    # Find contours\n",
    "    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )\n",
    "    \n",
    "    \n",
    "    try:\n",
    "        # Find contour with maximum area\n",
    "        contour = max(contours, key = lambda x: cv2.contourArea(x))\n",
    "        \n",
    "        # Create bounding rectangle around the contour\n",
    "        x,y,w,h = cv2.boundingRect(contour)\n",
    "        cv2.rectangle(crop_image,(x,y),(x+w,y+h),(0,0,255),0)\n",
    "        \n",
    "        # Find convex hull\n",
    "        hull = cv2.convexHull(contour)\n",
    "        \n",
    "        # Draw contour\n",
    "        drawing = np.zeros(crop_image.shape,np.uint8)\n",
    "        cv2.drawContours(drawing,[contour],-1,(0,255,0),0)\n",
    "        cv2.drawContours(drawing,[hull],-1,(0,0,255),0)\n",
    "        \n",
    "        # Fi convexity defects\n",
    "        hull = cv2.convexHull(contour, returnPoints=False)\n",
    "        defects = cv2.convexityDefects(contour,hull)\n",
    "        \n",
    "        # Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger \n",
    "        # tips) for all defects\n",
    "        count_defects = 0\n",
    "        \n",
    "        for i in range(defects.shape[0]):\n",
    "            s,e,f,d = defects[i,0]\n",
    "            start = tuple(contour[s][0])\n",
    "            end = tuple(contour[e][0])\n",
    "            far = tuple(contour[f][0])\n",
    "\n",
    "            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)\n",
    "            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)\n",
    "            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)\n",
    "            angle = (math.acos((b**2 + c**2 - a**2)/(2*b*c))*180)/3.14\n",
    "            \n",
    "            # if angle >= 90 draw a circle at the far point\n",
    "            if angle <= 90:\n",
    "                count_defects += 1\n",
    "                cv2.circle(crop_image,far,1,[0,0,255],-1)\n",
    "\n",
    "            cv2.line(crop_image,start,end,[0,255,0],2)\n",
    "\n",
    "        # Press SPACE if condition is match\n",
    "        if count_defects >= 4:\n",
    "            pyautogui.press('space')\n",
    "            cv2.putText(frame,\"JUMP\", (115,80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)\n",
    "\n",
    "    except:\n",
    "        pass\n",
    "\n",
    "    # Show required images\n",
    "    cv2.imshow(\"Gesture\", frame)\n",
    "     \n",
    "    # Close the camera if 'q' is pressed\n",
    "    if cv2.waitKey(1) == ord('q'):\n",
    "        break       \n",
    "\n",
    "capture.release()\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#no"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}