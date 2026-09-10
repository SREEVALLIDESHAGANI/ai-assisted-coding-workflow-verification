# Task 10: OAuth2 PKCE Flow with Mandatory State Verification
import hashlib
import base64
import secrets

class PKCEAuthFlow:
    @staticmethod
    def generate_pkce_pair():
        verifier = secrets.token_urlsafe(48)
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        state = secrets.token_urlsafe(32)
        return verifier, challenge, state

    @staticmethod
    def verify_callback(expected_state: str, incoming_state: str, verifier: str, challenge: str) -> bool:
        # Mandatory CSRF state check
        if not secrets.compare_digest(expected_state, incoming_state):
            raise PermissionError("CSRF State mismatch: rejected")
        
        # Verify PKCE code challenge
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        computed_challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        return secrets.compare_digest(computed_challenge, challenge)
