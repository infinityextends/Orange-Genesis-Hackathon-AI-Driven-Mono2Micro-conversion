class AccountDao:
    """
    Interface for accessing account data.
    """

    def get_account(self, username: str):
        raise NotImplementedError

    def create_account(self, account):
        raise NotImplementedError

    # Other data access methods...
