from typing import Annotated

from fastapi import Depends


class FakeSession:
    def __init__(self):
        self.open = True

    def close(self):
        self.open = False


def get_db_session():
    print("DB: open session")
    session = FakeSession()
    try:
        yield session
    finally:
        session.close()
        print("DB: close session")


DbSessionDeps = Annotated[
    FakeSession,
    Depends(get_db_session),
]
