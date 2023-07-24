import time
import psutil
import pygetwindow
import ctypes

# Windows API constants
GWL_HWNDPARENT = -8
WM_GETTEXTLENGTH = 0x000E
WM_GETTEXT = 0x000D
BUFFER_SIZE = 255

def get_active_browser_pid():
    for process in psutil.process_iter(['pid', 'name']):
        if 'chrome' in process.info['name'].lower():
            return process.info['pid']
    return None

def get_active_tab_title_and_url(pid):
    try:
        browser = pygetwindow.getWindowsWithTitle('Google Chrome')[0]
        if browser.isActive:
            active_tab_title = browser.title
            active_tab_url = get_url_from_window_handle(browser._hWnd)
            return active_tab_title, active_tab_url
        return None, None
    except IndexError:
        return None, None

def get_url_from_window_handle(hwnd):
    buffer = ctypes.create_unicode_buffer(BUFFER_SIZE)
    hwnd_parent = ctypes.windll.user32.GetParent(hwnd)
    url_length = ctypes.windll.user32.SendMessageW(hwnd_parent, WM_GETTEXTLENGTH, 0, 0)
    ctypes.windll.user32.SendMessageW(hwnd_parent, WM_GETTEXT, url_length + 1, buffer)
    return buffer.value

def monitor_activity(log_file):
    active_site_start_time = None
    while True:
        active_browser_pid = get_active_browser_pid()

        if active_browser_pid is not None:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            active_tab_title, active_tab_url = get_active_tab_title_and_url(active_browser_pid)

            if active_tab_title:
                if active_site_start_time is None:
                    active_site_start_time = time.time()

                with open(log_file, 'a') as f:
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Website URL: {active_tab_url}\n")
                    f.write(f"Page Title: {active_tab_title}\n")
                    
                # Calculate the total time duration users stay on the site
                active_site_duration = time.time() - active_site_start_time
                with open(log_file, 'a') as f:
                    f.write(f"Total time duration users stay on each site: {active_site_duration:.2f} seconds\n")
                    f.write("\n")

        else:
            active_site_start_time = None

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    log_file = "activity_log.txt"
    monitor_activity(log_file)
