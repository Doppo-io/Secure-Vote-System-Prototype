import hashlib
from app.models.voter_model import Voter

# Shared voter database
voters_db = [
    Voter(voter_id="V001", fingerprint_hash=hashlib.sha256("fingerprint1".encode()).hexdigest()),
    Voter(voter_id="V002", fingerprint_hash=hashlib.sha256("fingerprint2".encode()).hexdigest()),
    Voter(voter_id="V003", fingerprint_hash=hashlib.sha256("fingerprint3".encode()).hexdigest()),
    Voter(voter_id="V004", fingerprint_hash=hashlib.sha256("fingerprint4".encode()).hexdigest()),
    Voter(voter_id="V005", fingerprint_hash=hashlib.sha256("fingerprint5".encode()).hexdigest()),
    Voter(voter_id="V006", fingerprint_hash=hashlib.sha256("fingerprint6".encode()).hexdigest()),
    Voter(voter_id="V007", fingerprint_hash=hashlib.sha256("fingerprint7".encode()).hexdigest()),
    Voter(voter_id="V008", fingerprint_hash=hashlib.sha256("fingerprint8".encode()).hexdigest()),
    Voter(voter_id="V009", fingerprint_hash=hashlib.sha256("fingerprint9".encode()).hexdigest()),
    Voter(voter_id="V010", fingerprint_hash=hashlib.sha256("fingerprint10".encode()).hexdigest()),
    Voter(voter_id="V011", fingerprint_hash=hashlib.sha256("fingerprint11".encode()).hexdigest()),
    Voter(voter_id="V012", fingerprint_hash=hashlib.sha256("fingerprint12".encode()).hexdigest()),

    ]

# Shared token store
token_store = {}

# Shared vote ledger
votes_ledger = []