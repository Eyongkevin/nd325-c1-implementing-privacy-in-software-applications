import re
import backend.main.api.registry as registry


REDACTED_PHONE_NUMBER = "[REDACTED PHONE NUMBER]"
REDACTED_NAME = "[NAME REDACTED]"
REDACTED_EMAIL = "[REDACTED EMAIL]"
REDACTED_NATIONAL_ID ="[REDACTED NATIONAL ID]"

email_redex = r"\b\S+@\S+.\S+\b" # r"[A-Z|a-z]+@[A-Z|a-z]+\.[A-Z|a-z]+"
phone_redex = r"(?<!\d)\(?\d{3}\)?\s?-?\d{3}-?\d{4}\b"
national_id_redex = r"(?<!\d)\d{3}\s?-?\d{2}\s?-?\d{4}\b"

def redact_free_text(free_text: str) -> str:
    """
    :param: free_text The free text to remove sensitive data from
    :returns: The redacted free text
    """
    # TODO: Implement this! Feel free to change the function parameters if you need to

    # redact names 
    actual_candidates = registry.get_all_candidates()
    actual_candidate_names = set([candidate.name for candidate in actual_candidates])

    for name in actual_candidates:
        free_text = re.sub(name, REDACTED_NAME , free_text, flags=re.IGNORECASE)

    # redact phone number 
    free_text = re.sub(phone_redex, REDACTED_PHONE_NUMBER, free_text)

    # redact email
    free_text = re.sub(email_redex, REDACTED_EMAIL, free_text)

    # redact national id
    free_text = re.sub(national_id_redex, REDACTED_NATIONAL_ID, free_text)

    return free_text






