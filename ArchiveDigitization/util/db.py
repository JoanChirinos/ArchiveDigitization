"""
ArchiveDigitization

Python file facilitating database management and authentication

Copyright Joan Chirinos, 2021.
"""

from typing import Tuple, List
import uuid
# import datetime

import sqlite3
from scrypt import scrypt


class DBManager:

    def __init__(self, filename: str, table_defns_filename: str) -> None:
        """
        Initialize DBManager class.

        Parameters
        ----------
        filename : str
            filename for current database
        table_defns_filename : str
            filename for file containing table definition strings

        Returns
        -------
        None

        """
        self.db_filename = filename
        self.table_defns_filename = table_defns_filename

    def create_db(self) -> None:
        """
        Create database.

        Returns
        -------
        None

        """
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        with open(self.table_defns_filename) as f:
            for defn in f.readlines():
                print(defn[:-1])
                if defn.strip() != '':
                    c.execute(defn)

        db.commit()
        db.close()

    def register_user(self, email: str, password: str,
                      first_name: str, last_name: str) -> bool:
        """
        Register new user to DB

        Parameters
        ----------
        email : str
            the user's email
        password : str
            the user's password
        first_name: str
            the user's first name
        last_name: str
            the user's last name

        Returns
        -------
        bool
            True if user got registered.
            False if user already exists.

        """
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        # Check if email is already registered
        if c.execute('SELECT first FROM users WHERE email=?',
                     (email,)).fetchone():
            print('returning false')
            return False

        # Register user
        salt = str(uuid.uuid4())

        hash = scrypt.hash(password, salt)

        c.execute('INSERT INTO users VALUES(?,?,?,?,?)',
                  (email, hash, salt, first_name, last_name))

        db.commit()
        db.close()

        return True

    def authenticate_user(self, email: str, password: str) -> bool:
        """
        Authenticate user with given password.

        Parameters
        ----------
        email : str
            the user's email.
        password : str
            the user's password.

        Returns
        -------
        bool
            True if password matches email.
            False if email doesn't exist or password doesn't match email.

        """
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute('SELECT hash, salt FROM users WHERE email=?', (email,))

        vals = c.fetchone()
        if not vals:
            return False

        hash, salt = vals

        if hash != scrypt.hash(password, salt):
            return False

        return True

    def add_file(self, id: str, category: str) -> bool:
        '''
        Add ID to DB to represent image/text files.

        Parameters
        ----------
        id : str
            the ID.
        category : str
            the category.

        Returns
        -------
        bool
            True on success.
            False on failure.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute('INSERT INTO files VALUES(?,?,?,?)',
                  (id, category,0,''))

        db.commit()
        db.close()

        return True

    def set_text(self, id: str, text: str) -> bool:
        '''
        Set the is_digitized column in files table for given id to 1.

        Parameters
        ----------
        id : str
            the ID.
        text : str
            the text.

        Returns
        -------
        bool
            True on success.
            False on failure.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute('UPDATE files SET is_digitized=? WHERE id=?',
                  (1, id))
        c.execute('UPDATE files SET image_text=? WHERE id=?',
                  (text, id))

        db.commit()
        db.close()

        return True

    def is_digitized(self, id: str) -> bool:
        '''
        Return true if file with given id has been digitized.

        Parameters
        ----------
        id : str
            the ID.

        Returns
        -------
        bool
            True, is_digitized if file exists.
            False, None otherwise.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute('SELECT is_digitized FROM files WHERE id=?',
                  (id,))

        out = c.fetchone()
        if out is None:
            return False, None

        return True, out[0]

    def get_file_ids(self, by_digitized: bool = False,
                     digitized_value: bool = False) -> Tuple[str, ...]:
        '''
        Get file IDs based on parameters.

        If is_digitized is True, only gets ids where
        is_digitized == digitized_value.

        Parameters
        ----------
        by_digitized : bool
            If true, filter values. (the default is False).
        digitized_value : bool
            Value filter for is_digitized (the default is False).

        Returns
        -------
        Tuple[str, ...]
            Description of returned object.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        if by_digitized:
            c.execute('SELECT id FROM files WHERE is_digitized=?',
                      (digitized_value,))
        else:
            c.execute('SELECT id FROM files')

        ids = c.fetchall()

        if ids is None:
            return tuple()

        return [x[0] for x in ids]

    def get_files(self, by_digitized: bool = False,
                     digitized_value: bool = False) -> Tuple[str, ...]:
        '''
        Get file IDs and categories based on parameters.

        If is_digitized is True, only gets ids where
        is_digitized == digitized_value.

        Parameters
        ----------
        by_digitized : bool
            If true, filter values. (the default is False).
        digitized_value : bool
            Value filter for is_digitized (the default is False).

        Returns
        -------
        Tuple[str, ...]
            Description of returned object.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        if by_digitized:
            c.execute('SELECT id, category, image_text FROM files WHERE is_digitized=?',
                      (digitized_value,))
        else:
            c.execute('SELECT id, category, image_text FROM files')

        ids = c.fetchall()

        if ids is None:
            return tuple()

        return ids

    def get_tag_name(self, tag_id: str) -> str:
        '''
        Get tag name from tag id.

        Parameters
        ----------
        tag_id : str
            the tag id.

        Returns
        -------
        Tuple[bool, str]
            (True, tag_name) on success.
            (False, error_msg) on failure.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute('SELECT name FROM _tags WHERE id=?',
                  (tag_id,))

        name = c.fetchone()

        if name is None:
            return False, 'Tag id does not exist'

        return True, name[0]

    def get_tag_id(self, tag_name: str) -> Tuple[bool, str]:
        '''
        Get tag id from tag name.

        Parameters
        ----------
        tag_name : str
            tag name.

        Returns
        -------
        Tuple[bool, str]
            (True, tag_id) on success.
            (False, error_msg) on failure.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute('SELECT id FROM _tags WHERE name=?',
                  (tag_name,))

        id = c.fetchone()

        if id is None:
            return False, 'Tag name does not exist'

        return True, id[0]

    def create_tag(self, tag_name: str) -> Tuple[bool, str]:
        '''
        Create tag using tag name.

        Parameters
        ----------
        tag_name : str
            the tag name.

        Returns
        -------
        Tuple[bool, str]
            (True, tag_id) on success.
            (False, error_msg) on failure.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        if this.get_tag_id(tag_name)[0]:
            return False, 'tag name already exists'

        tag_id = str(uuid.uuid4())

        c.execute('INSERT INTO _tags VALUES(?,?)',
                  (tag_id, tag_name))

        db.commit()
        db.close()

        return True, tag_id

    def get_all_tags(self) -> List[List[str]]:
        '''
        Return all tags ids and names.

        Returns
        -------
        Tuple[Tuple[str,str],...]
            Tuple of (id, name) tuples

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.exeute('SELECT id, name FROM _tags')

        tags = c.fetchall()

        return [list(tag) for tag in tags]



    def raw_command(self, command: str) -> bool:
        '''
        Run raw command.

        Parameters
        ----------
        command : str
            the command to run.

        Returns
        -------
        bool
            True on success.

        '''
        db = sqlite3.connect(self.db_filename)
        c = db.cursor()

        c.execute(command)

        db.commit()
        db.close()
