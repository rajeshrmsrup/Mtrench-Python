import time
import psutil
import pygetwindow

def get_active_browser_pid():
    for process in psutil.process_iter(['pid', 'name']):
        if 'chrome' in process.info['name'].lower():
            return process.info['pid']
    return None

def get_active_tab_title(pid):
    try:
        browser = pygetwindow.getWindowsWithTitle('Google Chrome')[0]
        if browser.isActive:
            return browser.title
        return None
    except IndexError:
        return None

def monitor_activity(log_file):
    while True:
        active_browser_pid = get_active_browser_pid()

        if active_browser_pid is not None:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            active_tab_title = get_active_tab_title(active_browser_pid)

            if active_tab_title:
                with open(log_file, 'a') as f:
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Website URL: N/A (Not available for this implementation)\n")
                    f.write(f"Page Title: {active_tab_title}\n")
                    # Additional implementation is needed to get the URL and total time duration.
                    f.write("Total time duration users stay on each site: N/A (Not available for this implementation)\n")
                    f.write("\n")

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    log_file = "activity_log.txt"
    monitor_activity(log_file)
