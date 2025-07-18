from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

engine = create_engine("sqlite:////app/data/database.sqlite", echo=True)
Base = declarative_base()


def provide_session():
    def wrapper(func):
        def wrapped(*args, **kwargs):
            Session = sessionmaker(bind=engine)
            session = Session()
            try:
                result = func(*args, session=session, **kwargs)
                session.commit()
                return result
            except Exception as e:
                if isinstance(e, IntegrityError):
                    return {
                        "error": "Integrity error occurred, possibly a duplicate entry."
                    }
                print(f"An error occurred: {e}")
                session.rollback()
                raise e
            finally:
                session.close()

        return wrapped

    return wrapper
