import tkinter as tk
import math

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
        
        # Load all idle directional frames
        self.idle_frames = {}
        directions = ['', '_left', '_right', '_up', '_down', '_up_left', '_up_right', '_down_left', '_down_right']
        for d in directions:
            self.idle_frames[d] = [
                tk.PhotoImage(file=f'idle{d}_1.png'),
                tk.PhotoImage(file=f'idle{d}_2.png'),
                tk.PhotoImage(file=f'idle{d}_3.png'),
                tk.PhotoImage(file=f'idle{d}_4.png')
            ]
            
        self.pet = [
            tk.PhotoImage(file='pet_1.png'),
            tk.PhotoImage(file='pet_2.png'),
            tk.PhotoImage(file='pet_3.png'),
            tk.PhotoImage(file='pet_4.png')
        ]
        
        self.frame_index = 0
        self.state = 'idle'
        self.direction = ''
        
        # Create a label to show the image, with magenta background
        self.label = tk.Label(self.window, bd=0, bg='magenta')
        self.label.pack()
        
        # Bind mouse hover events
        self.label.bind('<Enter>', self.on_enter)
        self.label.bind('<Leave>', self.on_leave)
        
        # Bind triple left-click to close the app
        self.label.bind('<Triple-Button-1>', self.close_app)
        
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
        self.x = screen_width - width - 20
        self.y = screen_height - height - 50 
        
        self.window.geometry(f'{width}x{height}+{self.x}+{self.y}')
        
        # Store center coordinates for eye tracking
        self.center_x = self.x + width // 2
        self.center_y = self.y + height // 2
        
    def on_enter(self, event):
        self.state = 'pet'
        self.frame_index = 0
        
    def on_leave(self, event):
        self.state = 'idle'
        self.frame_index = 0
        
    def close_app(self, event):
        self.window.destroy()
        
    def get_eye_direction(self):
        mx = self.window.winfo_pointerx()
        my = self.window.winfo_pointery()
        
        dx = mx - self.center_x
        dy = my - self.center_y
        dist = math.hypot(dx, dy)
        
        if dist > 600: # Tracking range in pixels
            return ''
            
        # Determine direction based on angle
        angle = math.degrees(math.atan2(dy, dx))
        
        # angle goes from -180 to 180. 0 is right, 90 is down, -90 is up.
        if -22.5 <= angle < 22.5: return '_right'
        if 22.5 <= angle < 67.5: return '_down_right'
        if 67.5 <= angle < 112.5: return '_down'
        if 112.5 <= angle < 157.5: return '_down_left'
        if angle >= 157.5 or angle < -157.5: return '_left'
        if -157.5 <= angle < -112.5: return '_up_left'
        if -112.5 <= angle < -67.5: return '_up'
        if -67.5 <= angle < -22.5: return '_up_right'
        
        return ''

    def update_frame(self):
        # Choose animation frames based on state
        if self.state == 'idle':
            self.direction = self.get_eye_direction()
            frames = self.idle_frames[self.direction]
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
