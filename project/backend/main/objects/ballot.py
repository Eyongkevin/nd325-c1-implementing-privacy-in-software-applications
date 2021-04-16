import jsons
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes
from backend.main.store.secret_registry import get_secret_bytes, UTF_8, overwrite_secret_str, gen_salt, get_secret_str, \
    overwrite_secret_bytes

class Ballot:
    """
    A ballot that exists in a specific, secret manner
    """
    def __init__(self, ballot_number: str, chosen_candidate_id: str, voter_comments: str):
        self.ballot_number = ballot_number
        self.chosen_candidate_id = chosen_candidate_id
        self.voter_comments = voter_comments


def generate_ballot_number(national_id: str) -> str:
    """
    Produces a ballot number. Feel free to add parameters to this method, if you feel those are necessary.

    Remember that ballot numbers must respect the following conditions:

    1. Voters can be issued multiple ballots. This can be because a voter might make a mistake when filling out one
       ballot, and therefore might need an additional ballot. However it's important that only one ballot per voter is
       counted.
    2. All ballots must be secret. Voters have the right to cast secret ballots, which means that it should be
       technically impossible for someone holding a ballot to associate that ballot with the voter.
    3. In order to minimize the risk of fraud, a nefarious actor should not be able to tell that two different ballots
       are associated with the same voter.

    :return: A string representing a ballot number that satisfies the conditions above
    """
    # TODO: Implement this! Feel free to add parameters to this method, if necessary
    expected_bytes = 32 # For AES SIV 256
    NAME_ENCRYPTION_KEY_AES_SIV = "MY_NAME_ENCRYPTION_KEY"
    PEPPER_SECRET_NAME = "Encrypt SSN"

    name_encryption_key = get_secret_bytes(NAME_ENCRYPTION_KEY_AES_SIV)

    if not name_encryption_key:
      name_encryption_key = get_random_bytes(expected_bytes * 2)
      overwrite_secret_bytes(NAME_ENCRYPTION_KEY_AES_SIV, name_encryption_key)

    nonce = get_random_bytes(expected_bytes)

    cipher = AES.new(name_encryption_key, AES.MODE_SIV, nonce=nonce)

    cipher.update(b"")
    ciphertext, tag = cipher.encrypt_and_digest(national_id.encode(UTF_8))
    json_v = [b64encode(x).decode(UTF_8) for x in (nonce, ciphertext, tag)]
    return jsons.dumps(dict(zip(['nonce','ciphertext', 'tag'], json_v)))
