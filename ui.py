# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries

# HENRY HANLIN ZHENG
# HHZHENG1@UCI.EDU
# 19204536

from Profile import Profile, Post, DsuFileError, DsuProfileError
from pathlib import Path
import shlex
import ds_client
from OpenWeather import OpenWeather
from LastFM import LastFM

PORT = 2021
current_profile = None
current_file_path = None


def run():
    print("Welcome to the Journal App!")
    print("Press enter to continue to the journal menu...")

    user_input = input()
    if user_input == "admin":
        admin_mode()
    else:
        friendly_mode()


# ========================================================================
#                             FRIENDLY MODE
# ========================================================================

def friendly_mode():
    global current_profile, current_file_path

    print("--- JOURNAL MENU ---")

    weather_api = OpenWeather(zip="92697", ccode="US")
    weather_api.set_apikey("YOUR_OPENWEATHER_API_KEY") 
    
    lastfm_api = LastFM()
    lastfm_api.set_apikey("YOUR_LASTFM_API_KEY") 
    
    try:
        print("Loading API data...")
        weather_api.load_data()
        lastfm_api.load_data()
    except Exception as e:
        print(f"Warning: Could not load API data. ({e})")
        print("Keywords will not be transcluded.")

    while True:
        if current_profile:
            print(f"\nCurrent Profile: {current_profile.username}")
            print("1. Add a post")
            print("2. View all posts")
            print("3. Edit bio")
            print("4. Close profile")
            print("Q. Quit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                print("\nNote: You can use the following keywords:")
                print("  @weather - Adds the current weather")
                print("  @lastfm  - Adds the current top tracks")
                
                content = input("Enter post content: ")
                if not content:
                    print("Post content cannot be empty.")
                    continue

                current_profile.add_post(Post(content))
                save_current()
                print("Post added locally!")

                content = weather_api.transclude(content)
                content = lastfm_api.transclude(content)

                prompt = "Do you want to post this to the server? (y/n): "
                online = input(prompt).strip().lower()
                if online == 'y':
                    print("Posting to server...")
                    success = ds_client.send(
                        current_profile.dsuserver,
                        PORT,
                        current_profile.username,
                        current_profile.password,
                        content
                    )
                    if success:
                        print("Post successfully sent to server!")
                    else:
                        print("Failed to send post to server.")

            elif choice == '2':
                posts = current_profile.get_posts()
                if not posts:
                    print("No posts yet!")
                else:
                    for idx, post in enumerate(posts):
                        print()
                        print(f"ID {idx}: {post.get_entry()}")

            elif choice == '3':
                print()
                new_bio = input("Enter new bio: ")
                if not new_bio:
                    print("Bio cannot be empty.")
                    continue

                current_profile.bio = new_bio
                save_current()
                print("Bio updated locally!")

                prompt = "Update your bio on the server? (y/n): "
                online = input(prompt).strip().lower()
                if online == 'y':
                    print("Posting to server...")
                    success = ds_client.send(
                        current_profile.dsuserver,
                        PORT,
                        current_profile.username,
                        current_profile.password,
                        None,
                        new_bio
                    )
                    if success:
                        print("Bio successfully updated on server!")
                    else:
                        print("Failed to update bio on server.")

            elif choice == '4':
                close_profile()
                print("Profile closed.")

            elif choice == 'Q':
                print("Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")
        else:
            print("No profile saved. Starting profile wizard...")
            print("1. Create new profile")
            print("2. Load existing journal")
            print("Q. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                p_dir = input("Enter directory to save new profile: ").strip()
                p_name = input("Enter filename (without .dsu): ").strip()
                profile = create_dsu_file(p_dir, p_name)
                if profile:
                    current_profile = profile
                    path_obj = Path(p_dir)
                    if not p_name.lower().endswith('.dsu'):
                        p_name += '.dsu'
                    current_file_path = str(path_obj / p_name)
            elif choice == '2':
                p_path = input("Enter path to existing .dsu file: ").strip()
                profile = open_dsu_file(p_path)
                if profile:
                    current_profile = profile
                    current_file_path = p_path
            elif choice == 'Q':
                print("Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")


def save_current():
    global current_profile, current_file_path
    if current_profile and current_file_path:
        current_profile.save_profile(current_file_path)


def close_profile():
    global current_profile, current_file_path
    current_profile = None
    current_file_path = None
    print("Journal closed.")


# ========================================================================
#                              ADMIN MODE
# ========================================================================

def admin_mode():
    '''
    L - List the contents of the user specified directory.
    Q - Quit the program.
    C - Create a new file in the specified directory.
    D - Delete the file.
    R - Read the contents of a file.
    O - Open an existing file of type DSU
    E - Edit the DSU file loaded by C or O commands
    P - Print data stored in the DSU file loaded by C or O commands
    '''
    while True:
        try:
            user_input = input()
        except EOFError:
            break

        parsed = parse_input(user_input)
        if not parsed:
            if user_input.strip():
                print("ERROR")
            continue

        cmd, path_str, options = parsed

        cmd = cmd.upper()
        if cmd not in ("L", "Q", "C", "D", "R", "O", "E", "P"):
            print("ERROR")
            continue

        if not validate_options(cmd, options):
            print("ERROR")
            continue

        if cmd == "L":
            L_cmd(path_str, options)
        elif cmd == "C":
            C_cmd(path_str, options)
        elif cmd == "D":
            D_cmd(path_str)
        elif cmd == "R":
            R_cmd(path_str)
        elif cmd == "O":
            O_cmd(path_str)
        elif cmd == "E":
            E_cmd(options)
        elif cmd == "P":
            P_cmd(options)
        elif cmd == "Q":
            return


def parse_input(cmds):
    if not cmds:
        return None
    try:
        parts = shlex.split(cmds)
    except ValueError:
        return None

    if not parts:
        return None

    command = parts[0]
    split_index = len(parts)

    for i in range(1, len(parts)):
        if parts[i].startswith('-'):
            split_index = i
            break

    path_str = ' '.join(parts[1:split_index])
    options = parts[split_index:]

    return command, path_str, options


def option_value(options, flag):
    if flag in options:
        idx = options.index(flag)
        if idx + 1 < len(options):
            return options[idx + 1]
    return None


def validate_options(command, options):
    """Return True if all options are valid for command, else False."""
    allowed = {
        'L': {'-r': False, '-f': False, '-s': True, '-e': True},
        'C': {'-n': True},
        'D': {},
        'R': {},
        'Q': {},
        'O': {},
        'E': {
            '-usr': True, '-pwd': True, '-bio': True,
            '-addpost': True, '-delpost': True
        },
        'P': {
            '-usr': False, '-pwd': False, '-bio': False,
            '-posts': False, '-post': True, '-all': False
        }
    }
    cmd = command.upper()
    if cmd not in allowed:
        return False

    i = 0
    while i < len(options):
        opt = options[i]

        if opt not in allowed[cmd]:
            return False

        requires_value = allowed[cmd][opt]

        # flags that require a value
        if requires_value:
            if i + 1 >= len(options):
                return False
            if options[i + 1].startswith('-'):
                return False
            i += 2
        else:
            i += 1
    return True


def L_cmd(path_str, options):
    '''
    -r Output directory content recursively.
    -f Output only files, excluding directories in the results.
    -s Output only files that match a given file name.
    -e Output only files that match a given file extension.
    '''
    my_path = Path(path_str)
    if not my_path.exists():
        print("ERROR")
        return

    target_file = option_value(options, "-s")
    target_ext = option_value(options, "-e")
    recursive = "-r" in options
    files_only = "-f" in options

    # Helper to check if a file matches filter criteria
    def should_print_file(item):
        if files_only and not item.is_file():
            return False
        if target_file and item.name != target_file:
            return False
        if target_ext and item.suffix.lstrip('.') != target_ext.lstrip('.'):
            return False
        return True

    def recursive_list(directory):
        try:
            # Sort items to ensure deterministic output
            items = sorted(directory.iterdir())
        except OSError:
            # Handle permission errors or missing paths gracefully
            return

        files = [i for i in items if i.is_file()]
        dirs = [i for i in items if i.is_dir()]

        # 1. Print Files First
        for f in files:
            if should_print_file(f):
                print(f)

        # 2. Process Directories
        for d in dirs:
            # Determine if we should print the directory name itself
            should_show_dir = not files_only and not target_file and not target_ext

            if recursive:
                if should_show_dir:
                    print(d)
                recursive_list(d)
            else:
                # Non-recursive listing of the directory
                if should_show_dir:
                    print(d)

    # Start the listing
    if recursive:
        recursive_list(my_path)
    else:
        try:
            items = sorted(my_path.iterdir())
        except OSError:
            print("ERROR")
            return
        files = [i for i in items if i.is_file()]
        dirs = [i for i in items if i.is_dir()]

        for f in files:
            if should_print_file(f):
                print(f)
        for d in dirs:
            if not files_only and not target_file and not target_ext:
                print(d)


def C_cmd(path_str, options):
    '''
    -n Specify the name of the file to be created.
    '''
    global current_profile, current_file_path

    if "-n" not in options:
        print("ERROR")
        return

    name = option_value(options, "-n")
    if name is None:
        print("ERROR")
        return

    name = Path(name).name

    profile = create_dsu_file(path_str, name)

    if profile:
        current_profile = profile
        my_path = Path(path_str)
        if not name.lower().endswith('.dsu'):
            name += '.dsu'
        current_file_path = str(my_path / name)


def D_cmd(path_str):
    my_path = Path(path_str)
    if not my_path.exists() or not my_path.is_file():
        print("ERROR")
        return
    if my_path.suffix.lower() != '.dsu':
        print("ERROR")
        return
    try:
        my_path.unlink()
        print(f"{my_path} DELETED")
    except OSError:
        print("ERROR")
    return


def R_cmd(path_str):
    my_path = Path(path_str)
    if not my_path.exists() or not my_path.is_file():
        print("ERROR")
        return
    if my_path.suffix.lower() != '.dsu':
        print("ERROR")
        return
    try:
        with my_path.open('r') as file:
            contents = file.read()
            if contents == "":
                print("EMPTY")
            else:
                print(contents, end='')
    except OSError:
        print("ERROR")
    return


def O_cmd(path_str):
    global current_profile, current_file_path

    profile = open_dsu_file(path_str)

    if profile:
        current_profile = profile
        current_file_path = path_str


def E_cmd(options):
    """
    -usr [USERNAME]
    -pwd [PASSWORD]
    -bio [BIO]
    -addpost [NEW POST]
    -delpost [ID]
    """
    global current_profile, current_file_path

    if not current_profile or not current_file_path:
        print("ERROR")
        return

    i = 0
    while i < len(options):
        opt = options[i]
        val = options[i+1]

        if opt == "-usr":
            if ' ' in val:
                print("ERROR")
                return
            current_profile.username = val
        elif opt == "-pwd":
            if ' ' in val:
                print("ERROR")
                return
            current_profile.password = val
        elif opt == "-bio":
            current_profile.bio = val
        elif opt == "-addpost":
            if val.strip():
                current_profile.add_post(Post(val))
        elif opt == "-delpost":
            try:
                idx = int(val) - 1
                if idx < 0:
                    print("ERROR")
                    return
                if not current_profile.del_post(idx):
                    print("ERROR")
                    return
            except ValueError:
                print("ERROR")
                return

        i += 2

    try:
        current_profile.save_profile(current_file_path)
        print(f"Profile updated and saved to {current_file_path}")
    except Exception:
        print("ERROR")


def P_cmd(options):
    """
    -usr       Prints the username stored in the profile object
    -pwd       Prints the password stored in the profile object
    -bio       Prints the bio stored in the profile object
    -posts     Prints all posts stored in the profile object
    -post [ID] Prints post identified by ID
    -all       Prints all content stored in the profile object
    """
    global current_profile

    if not current_profile:
        print("ERROR")
        return

    i = 0
    while i < len(options):
        opt = options[i]

        if opt == '-usr':
            print(f"Username: {current_profile.username}")
            i += 1
        elif opt == '-pwd':
            print(f"Password: {current_profile.password}")
            i += 1
        elif opt == '-bio':
            print(f"Bio: {current_profile.bio}")
            i += 1
        elif opt == '-posts':
            posts = current_profile.get_posts()
            for idx, post in enumerate(posts):
                print(f"ID {idx + 1}: {post.get_entry()}")
            i += 1
        elif opt == '-post':
            try:
                idx = int(options[i + 1]) - 1
                posts = current_profile.get_posts()
                if 0 <= idx < len(posts):
                    print(f"ID {idx + 1}: {posts[idx].get_entry()}")
                else:
                    print("ERROR")
            except ValueError:
                print("ERROR")
            i += 2
        elif opt == '-all':
            print(f"Username: {current_profile.username}")
            print(f"Password: {current_profile.password}")
            print(f"Bio: {current_profile.bio}")
            posts = current_profile.get_posts()
            for idx, post in enumerate(posts):
                print(f"ID {idx + 1}: {post.get_entry()}")
            i += 1


# ========================================================================
#                            HELPER FUNCTIONS
# ========================================================================

def collect_profile_info():
    """
    Collect username, password, bio from user for new profile
    Returns tuple (username, password, bio, server)
    """
    print("Let's create your profile!")

    username = input("Enter a username (no spaces): ").strip()
    while ' ' in username or not username:
        print("Invalid username. Please enter a username with no spaces.")
        username = input("Enter a username (no spaces): ").strip()

    password = input("Enter a password (no spaces): ").strip()
    while ' ' in password or not password:
        print("Invalid password. Please enter a password with no spaces.")
        password = input("Enter a password (no spaces): ").strip()

    bio = input("Enter a bio: ").strip()

    server = input("Enter the DSP server address: ").strip()

    return username, password, bio, server


def open_dsu_file(path_str):
    """
    Open existing DSU file.
    """
    my_path = Path(path_str)

    if not my_path.exists() or not my_path.is_file():
        print("ERROR")
        return None
    if my_path.suffix != '.dsu':
        print("ERROR")
        return None

    profile = Profile()
    try:
        profile.load_profile(str(my_path))
        print(f"Successfully loaded user {profile.username} from {my_path}")
        if profile.bio:
            print(f"Bio: {profile.bio}")
        return profile
    except DsuFileError as e:
        print(f"ERROR: {e}")
        return None
    except DsuProfileError as e:
        print(f"ERROR: {e}")
        return None


def create_dsu_file(path_str, name):
    """
    Create DSU file with user profile info.
    """
    my_path = Path(path_str)
    if not my_path.exists() or not my_path.is_dir():
        print("ERROR")
        return
    if not name.lower().endswith('.dsu'):
        name += '.dsu'
    new_file_path = my_path / name

    if new_file_path.exists():
        print(f"File {new_file_path} already exists. Opening existing...")
        return open_dsu_file(str(new_file_path))

    username, password, bio, server = collect_profile_info()
    profile = Profile(dsuserver=server, username=username, password=password)
    profile.bio = bio

    try:
        new_file_path.touch()
        profile.save_profile(str(new_file_path))
        print(f"{new_file_path}")
        return profile
    except DsuFileError as e:
        print(f"ERROR: {e}")
        return None
    except Exception:
        print("ERROR")
        return None
