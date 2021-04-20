#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from typing import List

from backend.main.objects.candidate import Candidate
from backend.main.objects.voter import Voter, VoterStatus


class VotingStore:
    """
    A singleton class that encapsulates the interface between the stores and the databases.

    To use, simply do:

    >>> voting_store = VotingStore.get_instance()   # this will create the stores, if they haven't been created
    >>> voting_store.add_candidate(...)  # now, you can call methods that you need here
    """

    voting_store_instance = None

    @staticmethod
    def get_instance():
        if not VotingStore.voting_store_instance:
            VotingStore.voting_store_instance = VotingStore()

        return VotingStore.voting_store_instance

    @staticmethod
    def refresh_instance():
        """
        DO NOT MODIFY THIS METHOD
        Only to be used for testing. This will only work if the sqlite connection is :memory:
        """
        if VotingStore.voting_store_instance:
            VotingStore.voting_store_instance.connection.close()
        VotingStore.voting_store_instance = VotingStore()

    def __init__(self):
        """
        DO NOT MODIFY THIS METHOD
        DO NOT call this method directly - instead use the VotingStore.get_instance method above.
        """
        self.connection = VotingStore._get_sqlite_connection()
        self.create_tables()

    @staticmethod
    def _get_sqlite_connection() -> Connection:
        """
        DO NOT MODIFY THIS METHOD
        """
        return sqlite3.connect(":memory:", check_same_thread=False)

    def create_tables(self):
        """
        Creates Tables
        """
        self.connection.execute(
            """CREATE TABLE candidates (candidate_id integer primary key autoincrement, name text)""")
        # TODO: Add additional tables here, as you see fit
        self.connection.execute(
            """CREATE TABLE voters (national_id varchar primary key, first_name varchar, last_name varchar, voter_status varchar)"""
        )
        self.connection.commit()

    def add_candidate(self, candidate_name: str):
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        self.connection.execute("""INSERT INTO candidates (name) VALUES (?)""", (candidate_name, ))
        self.connection.commit()

    def get_candidate(self, candidate_id: str) -> Candidate:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id=?""", (candidate_id,))
        candidate_row = cursor.fetchone()
        candidate = Candidate(candidate_id, candidate_row[1]) if candidate_row else None
        self.connection.commit()

        return candidate

    def get_all_candidates(self) -> List[Candidate]:
        """
        Gets ALL the candidates from the database
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates""")
        all_candidate_rows = cursor.fetchall()
        all_candidates = [Candidate(str(candidate_row[0]), candidate_row[1]) for candidate_row in all_candidate_rows]
        self.connection.commit()

        return all_candidates

    # TODO: If you create more tables in the create_tables method, feel free to add more methods here to make accessing
    #       data from those tables easier. See get_all_candidates, get_candidates and add_candidate for examples of how
    #       to do this.
    def add_voter(self, first_name: str, last_name: str, national_id: str, voter_status: str = VoterStatus.REGISTERED_NOT_VOTED.name):
        """
        Adds a voter into the voter table, returning FALSE if already exist, else TRUE.
        """
        self.connection.execute("""INSERT INTO voters (national_id, first_name, last_name, voter_status) VALUES (?, ?, ?, ?)""", 
        (national_id, first_name, last_name, voter_status))

        self.connection.commit()

    def get_voter(self, national_id: str) -> Voter:
        """
        Returns the voter specified, if that voter is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM voters WHERE national_id=?""", (national_id,))
        voter_row = cursor.fetchone()
        voter = Voter(voter_row[1], voter_row[2], national_id, voter_row[3]) if voter_row else None
        self.connection.commit()

        return voter

    def remove_voter(self, national_id: str) -> bool:
        """
        Remove voter from the database
        """
        cursor = self.connection.cursor()
        cursor.execute("""DELETE FROM voters WHERE national_id=?""", (national_id,))

