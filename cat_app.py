import tkinter as tk
import random

class Pet:
    def __init__(self):
        self.window = tk.Tk()
        
        # Make the background color magenta
        self.window.config(bg='magenta')
        
        # Set magenta as the transparent color so it's invisible
        self.window.wm_attributes('-transparentcolor', 'magenta')
        
        # Keep window always on top of other apps
        self.window.attributes('-topmost', True)
        
        # Remove borders and title bar
        self.window.overrideredirect(True)
        
        # Load the generated PNG images
        self.idle = [
            tk.PhotoImage(file='idle_1.png'),
            tk.PhotoImage(file='idle_2.png'),
            tk.PhotoImage(file='idle_3.png'),
            tk.PhotoImage(file='idle_4.png')
        ]
        self.pet = [
            tk.PhotoImage(file='pet_1.png'),
            tk.PhotoImage(file='pet_2.png'),
            tk.PhotoImage(file='pet_3.png'),
            tk.PhotoImage(file='pet_4.png')
        ]
        
        self.frame_index = 0
        self.state = 'idle'
        
        # Create a label to show the image, with magenta background
        self.label = tk.Label(self.window, bd=0, bg='magenta')
        self.label.pack()
        
        # Bind mouse hover events
        self.label.bind('<Enter>', self.on_enter)
        self.label.bind('<Leave>', self.on_leave)
        
        # Calculate screen resolution and position cat in bottom right corner
        self.position_window()
        
        # Start animation loop
        self.window.after(0, self.update_frame)
        self.window.mainloop()
        
    def position_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # The cat image is 160x160 pixels (32x32 scaled by 5)
        width = 160
        height = 160
        
        # Position above the Windows taskbar (typically 40-50px) and a bit off the right edge
        x = screen_width - width - 20
        y = screen_height - height - 50 
        
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_enter(self, event):
        self.state = 'pet'
        self.frame_index = 0
        
    def on_leave(self, event):
        self.state = 'idle'
        self.frame_index = 0
        
    def update_frame(self):
        # Choose animation frames based on state
        if self.state == 'idle':
            frames = self.idle
            delay = 500  # Slower tail wagging
        else:
            frames = self.pet
            delay = 300  # Faster happy animation
            
        # Update image
        self.label.config(image=frames[self.frame_index])
        
        # Advance frame
        self.frame_index = (self.frame_index + 1) % len(frames)
        
        # Schedule next frame
        self.window.after(delay, self.update_frame)

if __name__ == '__main__':
    Pet()
