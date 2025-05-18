from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///data/database.sqlite", echo=True)


class Base(DeclarativeBase):
    pass


def provide_session():
    def wrapper(func):
        def wrapped(*args, **kwargs):
            Session = sessionmaker(bind=engine)
            session = Session()
            try:
                result = func(session, *args, **kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
                return result

        return wrapped

    return wrapper
