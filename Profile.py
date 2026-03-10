# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to load or save Profile objects to
    file the system.
    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to deserialize a dsu file to a
    Profile object.
    """
    pass


class Post(dict):
    """
    The Post class is responsible for working with individual user posts. It
    currently supports two features: A timestamp property that is set upon
    instantiation and when the entry object is set and an entry property that
    stores the post message.
    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry

    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU
    server. You will need to use this class to manage the information provided
    by each new user created within your program for a2.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''             # OPTIONAL
        self._posts = []          # OPTIONAL

    def add_post(self, post: Post) -> None:
        """
        add_post accepts a Post object as parameter and appends it to the
        posts list.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
        del_post removes a Post at a given index and returns True if successful
        and False if an invalid index was supplied.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
        get_posts returns the list object containing all posts that have been
        added to the Profile object
        """
        return self._posts

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance
        of Profile to the file system.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error attempting to process DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data
        stored in a DSU file.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
