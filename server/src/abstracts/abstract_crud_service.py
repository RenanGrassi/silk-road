from abc import ABC, abstractmethod
from src.services.database import provide_session, sessionmaker
from src.services.auth import AuthService


class AbstractCRUDService(ABC):
    """
    Abstract base class for CRUD services.
    """

    @property
    @abstractmethod
    def model(self):
        """
        The model class that this service operates on.
        :return: The model class.
        """
        pass

    @provide_session()
    def create(self, data: dict, session: sessionmaker):
        """
        Create a new resource.
        :param data: The data to create the resource with.
        :return: The created resource.
        """
        resource = self.model(**data)

        session.add(resource)
        session.flush()
        print(resource)
        return {c.name: getattr(resource, c.name) for c in resource.__table__.columns}

    @provide_session()
    def read(self, resource_id: int, session: sessionmaker):
        """
        Read a resource by its ID.
        :param resource_id: The ID of the resource to read.
        :return: The resource with the given ID.
        """
        item = session.query(self.model).filter_by(id=resource_id).first()
        if not item:
            raise Exception("Resource not found")
        return {c.name: getattr(item, c.name) for c in item.__table__.columns}

    @provide_session()
    def update(self, resource_id, data, session: sessionmaker):
        """
        Update a resource by its ID.
        :param resource_id: The ID of the resource to update.
        :param data: The data to update the resource with.
        :return: The updated resource.
        """
        resource = session.query(self.model).filter_by(id=resource_id).first()
        for key, value in data.items():
            setattr(resource, key, value)
        session.flush()
        return {c.name: getattr(resource, c.name) for c in resource.__table__.columns}

    @provide_session()
    def list(self, conf: dict, session: sessionmaker):
        """
        List all resources.
        :return: A list of all resources.
        """
        return session.query(self.model).all()

    @provide_session()
    def delete(self, resource_id, session: sessionmaker):
        """
        Delete a resource by its ID.
        :param resource_id: The ID of the resource to delete.
        :return: None
        """
        resource = session.query(self.model).filter_by(id=resource_id).first()
        if resource:
            session.delete(resource)
            return True
        return False

    @provide_session()
    def delete_all(self, conf, session: sessionmaker):
        """
        Delete all resources.
        :return: None
        """
        session.query(self.model).delete()
