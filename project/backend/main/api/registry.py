#
# This file is the internal-only API that allows for the population of the voter registry.
# This API should not be exposed as a REST API for election security purposes.
#
from typing import List
from backend.main.objects.voter import Voter, VoterStatus, obfuscate_national_id
from backend.main.objects.candidate import Candidate
from backend.main.store.data_registry import VotingStore

#
# Voter Registration
#


def register_voter(voter: Voter) -> bool:
    """
    Registers a specific voter for the election. This method doesn't verify that the voter is eligible to vote or any
    such legal logistics -- it simply registers them if they aren't currently registered.

    :param: voter The voter to register.
    :returns: Boolean TRUE if the registration was successful. Boolean FALSE if the voter was already registered
              (based on their National ID)
    """
    # TODO: Implement this!
    voter_obj = Voter(voter.first_name, voter.last_name, voter.national_id)

    if get_voter_status(voter.national_id) == VoterStatus.NOT_REGISTERED:
        store = VotingStore.get_instance()
        store.add_voter(
            voter_obj.get_minimal_voter().obfuscated_first_name, 
            voter_obj.get_minimal_voter().obfuscated_last_name, 
            voter_obj.get_minimal_voter().obfuscated_national_id
        )
        return True
    return False


def get_voter_status(voter_national_id: str) -> VoterStatus:
    """
    Checks to see if the specified voter is registered.

    :param: voter_national_id The sensitive ID of the voter to check the registration status of.
    :returns: The status of the voter that best describes their situation
    """
    # TODO: Implement this!
    store = VotingStore.get_instance()
    obfuscate_voter_national_id = obfuscate_national_id(voter_national_id)
    voter = store.get_voter(obfuscate_voter_national_id)


    return VoterStatus[voter.voter_status] if voter is not None else VoterStatus.NOT_REGISTERED


def de_register_voter(voter_national_id: str) -> bool:
    """
    De-registers a voter from voting. This is to be used when the user requests to be removed from the system.
    If a voter is a fraudulent voter, this should still be reflected in the system; they should not be able to
    de-registered.

    :param: voter_national_id The sensitive ID of the voter to de-register.
    :returns: Boolean TRUE if de-registration was successful. Boolean FALSE otherwise.
    """
    # TODO: Implement this!
    voter_status = get_voter_status(voter_national_id)
    if  voter_status== VoterStatus.NOT_REGISTERED.name or voter_status == VoterStatus.FRAUD_COMMITTED.name:
        return False 
    else: 
        try:
            obfuscate_voter_national_id = obfuscate_national_id(voter_national_id)
            store = VotingStore.get_instance()
            voter = store.remove_voter(obfuscate_voter_national_id)
            return True
        except:
            return False


#
# Candidate Registration (Already Implemented)
#

def register_candidate(candidate_name: str):
    """
    Registers a candidate for the election, if not already registered.
    """
    store = VotingStore.get_instance()
    store.add_candidate(candidate_name)


def candidate_is_registered(candidate: Candidate) -> bool:
    """
    Checks to see if the specified candidate is registered.

    :param: candidate The candidate to check the registration status of
    :returns: Boolean TRUE if the candidate is registered. Boolean FALSE otherwise.
    """
    store = VotingStore.get_instance()
    return store.get_candidate(candidate.candidate_id) is not None


def get_all_candidates() -> List[Candidate]:
    store = VotingStore.get_instance()
    return store.get_all_candidates()
