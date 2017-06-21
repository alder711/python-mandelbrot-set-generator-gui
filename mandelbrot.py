#!/usr/bin/python3
#
# mandelbrot_v2.py
# 
# AUTHOR
# Trevor Bautista
# 
# VERSION
# Created: 31 May 2017
# Version 2.0 as of 2 June 2017
#
# PURPOSE
# The purpose of this program is to calculate and plot the
# Mandelbrot set or subsets of it, depending on the user's
# choice.
#
# TO DO
# Make calculation a background process




#imports
import tkinter as tk                 #toolkit interface for GUI elements
from tkinter import messagebox as mb #dialog box functionality
import numpy as np                   #tools for n-dimensional vectors
import matplotlib.pyplot as plt      #tools for plotting
import threading as th               #for multithreading


"""class App"""
class App:
	"""Default values"""
	defaultXMin = -2.25    #lower boundary of real axis
	defaultXMax = 0.75     #upper boundary of real axis
	defaultYMin = -1.5     #lower boundary of imaginary axis
	defaultYMax = 1.5      #upper boundary of imaginary axis
	defaultThreshold = 120 #number of iterations for each point
	defaultDensity = 1000  #pixel density of plot
	defaultLimit = 4       #boundary to determine boundedness

	"""Miscellaneous variables"""
	genReady = "Generate!"     #text for generate button when ready
	genBusy = "Calculating..." #text for generate button when busy

	"""Constructor method creates window"""
	def __init__(self, root):
		"""notifyGridCheck logs the checking of the grid checkbox"""
		def notifyGridCheck():
			#if box is checked,
			if (self.gridState.get() == 1):
				#notify that box is checked
				log("[I] Grid enabled")
			#if box is unchecked,
			elif (self.gridState.get() == 0):
				#notify that box is unchecked
				log("[I] Grid disabled")
			else:
				pass

		"""log appends text to the log textbox"""
		def log(text):
			#make textbox editable
			self.logs.config(state=tk.NORMAL)
			#add text
			self.logs.insert(tk.INSERT, text + "\n")
			#make textbox uneditable
			self.logs.config(state=tk.DISABLED)
			#update GUI
			root.update_idletasks()

		"""set_defaults method sets default parameters"""
		def set_defaults(event):
			log("[I] Using default values.")
			#set default value for x lower bound
			set_text(self.xLowerEntry,self.defaultXMin)
			#set default value for x upper bound
			set_text(self.xUpperEntry,self.defaultXMax)
			#set default value for y lower bound
			set_text(self.yLowerEntry,self.defaultYMin)
			#set default value for y upper bound
			set_text(self.yUpperEntry,self.defaultYMax)
			#set default value for threshold
			set_text(self.thresholdEntry,self.defaultThreshold)
			#set default value for density
			set_text(self.densityEntry,self.defaultDensity)
			#set default value for limit
			set_text(self.limitEntry,self.defaultLimit)

		"""set_text is a helper method for setting text
		into an entry box"""
		def set_text(entry, text):
			entry.delete(0,tk.END)
			entry.insert(0,text)

		"""mandelbrot(c, threshold, limit)
		given a complex number c and number of iterations to test 
		boundedness (threshold), the number of iterations taken 
		for z to become unbounded is returned, where the formula
		for z is z[i+1] = z[i]^2 + c"""
		def mandelbrot(c, threshold,limit):
		    #z is the complex number (0i+0j)
		    z = complex(0, 0)
		    #for each iteration of <threshold> iterations,
		    for iteration in range(threshold):
		        #compute the next z value
		        z = (z*z) + c

		        #if the absolute value of z is unbounded,
		        if abs(z) > limit:
		            #break out of iteration loop
		            break
		    #return the number of iterations z took to become unbounded
		    return iteration

		"""mandelbrot_set(threshold, density)
		creates the Mandelbrot set/subset from iteration formula"""
		def mandelbrot_set(threshold,density,limit,xLower,xUpper,yLower,yUpper):
		    #log status
		    log("[I] Generating, please wait..." +
		    	"\n    real bounds: [ " + str(xLower) + ", " + str(xUpper) + " ]" +
		    	"\n    imag bounds: [ " + str(yLower) + ", " + str(yUpper) + " ]" +
		    	"\n    threshold: " + str(threshold) +
		    	"\n    density: " + str(density) +
		    	"\n    limit: " + str(limit))
		    #define real axis vector (points)
		    realAxis = np.linspace(xLower, xUpper, density)
		    #define imaginary axis vector (points)
		    imaginaryAxis = np.linspace(yLower, yUpper, density)
		    #define number of points defined on real axis
		    realAxisLen = len(realAxis)
		    #define number of points on imaginary axis
		    imaginaryAxisLen = len(imaginaryAxis)

		    #define a 2-D array to represent mandelbrot atlas (will
		    #represent all points and their colorized values later,
		    #right now each point is 'empty')
		    atlas = np.empty((realAxisLen, imaginaryAxisLen))

		    #for each point's real component,
		    for ix in range(realAxisLen):
		        #for each point's imaginary component,
		        for iy in range(imaginaryAxisLen):
		            #define point's real component value
		            cx = realAxis[ix]
		            #define point's imaginary component value
		            cy = imaginaryAxis[iy]
		            #define complex number c using the point coordinates
		            c = complex(cx, cy)

		            #assign color value to point
		            atlas[ix, iy] = mandelbrot(c, threshold, limit)

		    #create new figure
		    plt.figure()
		    #plot mandelbrot set
		    #optional: add as parameter: 'cmap="hot"' for color changes
		    #to do: use 'extent=[xmin, xmax, ymin, ymax]' for axes ticks
		    plt.imshow(atlas.T, interpolation="nearest", cmap="jet", origin="lower", extent=(xLower,xUpper,yLower,yUpper))
		    #if grid state is checked,
		    if (self.gridState.get() == 1):
			    #create grid
			    plt.grid(color='w', linestyle='-', linewidth=1)
		    #plot colorbar (colors representing number of iterations)
		    plt.colorbar()
		    #log status
		    log("[I] Done generating.")
		    #display mandelbrot set
		    plt.show()

		"""generate generates the image from the 
		parameters given"""
		def generate(event):
			#try to:
			try:
				#change button text for status and disable button
				#self.generateButton.config(text=self.genBusy,state=tk.DISABLED)
				
				#calculate set
				mandelbrot_set(
					int(self.thresholdEntry.get()),
					int(self.densityEntry.get()),
					int(self.limitEntry.get()),
					float(self.xLowerEntry.get()),
					float(self.xUpperEntry.get()),
					float(self.yLowerEntry.get()),
					float(self.yUpperEntry.get()))
				#log status
				log("[I] Done generating.")
				#change button text for status and enable button
				#self.generateButton.config(text=self.genReady,state=tk.NORMAL)
			#if value or type error,
			except (ValueError, TypeError):
				#notify user
				log("[E] Please enter values that are either integers or floats.")
				errorWindow = mb.showerror(title="Error",message="Invalid data, please enter correct values.")

		#create title frame to put in window
		titleFrame = tk.Frame(root)
		#put title frame in 'root' window
		titleFrame.pack()

		#create title label
		self.titleLabel = tk.Label(titleFrame,text="Mandelbrot Generator\nv2.0",font="bold 20").grid(row=0)

		#create content pane
		contentFrame = tk.Frame(root)
		#put content frame in 'root' window
		contentFrame.pack()

		#create subframe for input
		inputFrame = tk.Frame(contentFrame)
		#put subframe in 'root' window
		inputFrame.pack(side=tk.LEFT)

		#create label for lower x axis limit
		self.xLowerLabel = tk.Label(inputFrame,text="Real Axis Lower Limit").grid(row=1,column=0)
		#create and arrage entry for lower x axis limit
		self.xLowerEntry = tk.Entry(inputFrame)
		self.xLowerEntry.grid(row=1,column=1)
		#create label for upper x axis limit
		self.xUpperLabel = tk.Label(inputFrame,text="Real Axis Upper Limit").grid(row=2,column=0)
		#create and arrange entry for upper x axis limit
		self.xUpperEntry = tk.Entry(inputFrame)
		self.xUpperEntry.grid(row=2,column=1)

		#create label for lower y axis limit
		self.yLowerLabel = tk.Label(inputFrame,text="Imaginary Axis Lower Limit").grid(row=3,column=0)
		#create and arrange entry for lower y axis limit
		self.yLowerEntry = tk.Entry(inputFrame)
		self.yLowerEntry.grid(row=3,column=1)
		#create label for upper y axis limit
		self.yUpperLabel = tk.Label(inputFrame,text="Imaginary Axis Upper Limit").grid(row=4,column=0)
		#create and arrange entry for upper y axis limit
		self.yUpperEntry = tk.Entry(inputFrame)
		self.yUpperEntry.grid(row=4,column=1)

		#create label for resolution
		self.densityLabel = tk.Label(inputFrame,text="Resolution/Density").grid(row=5,column=0)
		#create and arrange entry for resolution
		self.densityEntry = tk.Entry(inputFrame)
		self.densityEntry.grid(row=5,column=1)
		
		#create label for limit (to determine boundedness)
		self.limitLabel = tk.Label(inputFrame,text="Limit Determining Boundedness").grid(row=6,column=0)
		#create and arrange entry for resolution
		self.limitEntry = tk.Entry(inputFrame)
		self.limitEntry.grid(row=6,column=1)

		#create label for threshold
		self.thresholdLabel = tk.Label(inputFrame,text="Threshold/Iterations").grid(row=7,column=0)
		#create and arrange entry for threshold
		self.thresholdEntry = tk.Entry(inputFrame,text="5")
		self.thresholdEntry.grid(row=7,column=1)

		#create the right sub-frame (the left one is 'inputFrame')
		inputFrameTwo=tk.Frame(contentFrame)
		inputFrameTwo.pack(side=tk.RIGHT)

		#create 'boolean' variable corresponding to grid checkbox
		self.gridState = tk.IntVar()
		#create grid checkbox
		self.gridCheckButton = tk.Checkbutton(inputFrameTwo,text="Grid", variable=self.gridState,command=notifyGridCheck)
		self.gridCheckButton.grid(row=0, column=0)

		#create textbox frame (for scrollbar)
		logFrame = tk.Frame(inputFrameTwo)
		logFrame.grid(row=1,column=0)

		#create a textbox to hold logs
		self.logs = tk.Text(logFrame,state=tk.DISABLED,width=25,height=8,relief=tk.SUNKEN,foreground="black",wrap=tk.NONE)
		#create scrollbar for vertical direction of logs
		self.scrollY = tk.Scrollbar(logFrame)
		#pack scrollbar
		self.scrollY.pack(side=tk.RIGHT, fill=tk.Y)
		#configure scrollbar to scroll for logs
		self.scrollY.config(command=self.logs.yview)
		#configure logs to accept the scrollbar's command
		self.logs.config(yscrollcommand=self.scrollY.set)
		#create scrollbar for horizontal direction of logs
		self.scrollX = tk.Scrollbar(logFrame)
		#pack scrollbar
		self.scrollX.pack(side=tk.BOTTOM, fill=tk.X)
		#configure scrollbar to scroll for logs
		self.scrollX.config(command=self.logs.xview,orient=tk.HORIZONTAL)
		#configure logs to accept the scrollbar's command
		self.logs.config(xscrollcommand=self.scrollX.set)
		#pack canvas AFTER scrollbars
		self.logs.pack(side=tk.TOP,fill=tk.BOTH,expand=tk.TRUE)

		#create subframe for buttons
		butFrame = tk.Frame(root)
		#put subframe in 'root' window
		butFrame.pack()

		#create button for default settings, giving it function binding
		#and arrangement
		self.defaultsButton = tk.Button(butFrame,text="Defaults",width=15)
		self.defaultsButton.bind('<Button-1>', set_defaults)
		self.defaultsButton.grid(row=0,column=0)
		#create button to generate image, giving it function binding
		#and arrangement
		self.generateButton = tk.Button(butFrame,text=self.genReady, width=15)
		self.generateButton.bind('<Button-1>', generate)
		self.generateButton.grid(row=0,column=1)
		#create button to quit, giving it function binding
		#and arrangement
		self.quitButton = tk.Button(butFrame,text="Quit", width=15, command=quit)
		self.quitButton.bind('<Button-1>', quit)
		self.quitButton.grid(row=0,column=2)



#create root widget (window)
root = tk.Tk()
#give window a title
root.title("Mandelbrot Calculator")
#create "App" object (frames for window)
app = App(root)
#show window
root.mainloop()