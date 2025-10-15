import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import time
import sys
from matplotlib.animation import FuncAnimation, FFMpegWriter

#set paths
path_pic = '../Data/Images/Pics_Figs_6_7/houstereocamaS5.a1.'
path_data = '../Data/track'
    

def seconds_to_hhmmss(total_seconds):
    """
    Converts an integer number of seconds from midnight into an 'hhmmss' string.

    Args:
        total_seconds (int): The number of seconds elapsed since midnight.

    Returns:
        str: The time in 'HHMMSS' format.
    """

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the components with leading zeros and concatenate
    return f"{hours:02}{minutes:02}{seconds:02}"
    
    
def display_figs(date_str, tmI, data, fig, ax, save_video=False, video_filename=None):
    """
    Displays the tracked points on corresponding images or prepares frames for video.

    Args:
        date_str (str): The date string (YYYYMMDD).
        tmI (numpy.ndarray): Array of timestamps in seconds.
        data (numpy.ndarray): Array of tracked point coordinates (x, y).
        fig (matplotlib.figure.Figure): The figure object.
        ax (matplotlib.axes.Axes): The axes object.
        save_video (bool): Flag to indicate if frames should be prepared for video saving.
        video_filename (str, optional): The filename for the output video. Required if save_video is True.
    """
    
    # List to hold valid frame data (tmstr, x, y) for video
    valid_frames = []
    
    for i in range(len(tmI)):
        tmstr = seconds_to_hhmmss(int(tmI[i]))
        
        try:
            img_path = path_pic + date_str + "." + tmstr + ".jpg"
            img = plt.imread(img_path)
            
            # If not saving video, display interactively
            if not save_video:
                ax.clear()
                ax.imshow(img)
                ax.axis('off') 
                ax.set_xlim(400, 2000)
                ax.set_ylim(1600, 1000) 

                # Overlay the 'X' sign at (x, y)
                x = data[i, 0]
                y = data[i, 1]
                
                ax.scatter(x, y, marker='x', 
                           s=20,      # size of the marker
                           color='white', linewidths=2)
                # Display tmstr as title of the plot
                ax.set_title(date_str+"-"+tmstr, fontsize=14)

                # Draw the updated plot
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.show()

                print(f"Displaying frame {i+1}/{len(tmI)}: {tmstr}")
                time.sleep(1)
            else:
                # Store data for animation function if saving video
                valid_frames.append({'tmstr': tmstr, 'img': img, 'x': data[i, 0], 'y': data[i, 1]})
                
        except FileNotFoundError:
            print(f"Skipping frame {i+1}: Image not found at {tmstr}")
            continue # Move to the next iteration
        except Exception as e:
            print(f"An error occurred at frame {i+1}: {e}")
            break
            
    if save_video and valid_frames:
        print("\nPreparing to save video...")
        
        # Setup the axes once for the animation
        def init_func():
            ax.clear()
            ax.axis('off') 
            ax.set_xlim(400, 2000)
            ax.set_ylim(1600, 1000)
            return ax,

        # Function to draw each frame
        def animate(i):
            frame_data = valid_frames[i]
            
            ax.clear()
            ax.imshow(frame_data['img'])
            ax.axis('off') 
            ax.set_xlim(400, 2000)
            ax.set_ylim(1600, 1000) 

            # Overlay the 'x' sign at (x, y)
            ax.scatter(frame_data['x'], frame_data['y'], marker='x', 
                       s=20, color='white', linewidths=2)
            
            # Display tmstr as title of the plot
            ax.set_title(date_str + "-" + frame_data['tmstr'], fontsize=14)
            
            print(f"Processing frame {i+1}/{len(valid_frames)} for video: {frame_data['tmstr']}")
            return ax,
        
        # Create the animation object
        # The interval is set to 1000ms (1 second) to match the interactive display's time.sleep(1)
        anim = FuncAnimation(fig, animate, init_func=init_func, 
                             frames=len(valid_frames), interval=1000, 
                             blit=False, repeat=False)

        # Set up the FFMpeg writer
        Writer = FFMpegWriter(fps=1, metadata=dict(artist='Me'), bitrate=-1)
        
        try:
            # Save the animation to the video file
            anim.save(video_filename, writer=Writer)
            print(f"\nSuccessfully saved video to {video_filename}")
        except ValueError as e:
            print(f"\nError saving video. Ensure FFMpeg is installed and in your system's PATH. Error: {e}")
            print(f"Attempted to write to: {video_filename}")
        except Exception as e:
            print(f"\nAn unexpected error occurred while saving the video: {e}")
    

##################################################################
def main():
    #check input arguments
    if (len(sys.argv)<2):
        print('Usage: show_tracked_pts.py <YYYYMMDD> [save_video]')
        print('e.g. python show_tracked_pts.py 20220622')
        print('e.g. python show_tracked_pts.py 20220622 save_video')
        sys.exit();
               
    # Determine if video saving is requested
    save_video = len(sys.argv) > 2 and sys.argv[2].lower() == 'save_video'
   
    #load data
    date_str = sys.argv[1]  # date, for example 20220622
    mat = scipy.io.loadmat(path_data+date_str+'.mat')  
    data = mat['data']
    tmI = mat['tmI']

    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 5))
    
    video_filename = date_str + "_tracked_pts.mp4"
    
    if not save_video:
        plt.ion() # Turn on interactive mode for live display
        display_figs(date_str, tmI, data, fig, ax, save_video=False)
        plt.ioff() # Turn off interactive mode
        plt.close(fig) # Close the figure
    else:
        display_figs(date_str, tmI, data, fig, ax, save_video=True, video_filename=video_filename)
        plt.close(fig) # Close the figure after saving the video
    
main()
