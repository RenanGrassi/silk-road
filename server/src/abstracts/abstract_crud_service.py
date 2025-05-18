from abc import ABC, abstractmethod
from src.services.database import provide_session, sessionmaker


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

    @provide_session
    def create(self, session: sessionmaker, data: dict):
        """
        Create a new resource.
        :param data: The data to create the resource with.
        :return: The created resource.
        """
        resource = self.model(**data)
        session.add(resource)
        return resource

    @provide_session
    def read(self, session: sessionmaker, resource_id: int):
        """
        Read a resource by its ID.
        :param resource_id: The ID of the resource to read.
        :return: The resource with the given ID.
        """
        return session.query(self.model).filter_by(id=resource_id).first()

    @provide_session
    def update(self, session, resource_id, data):
        """
        Update a resource by its ID.
        :param resource_id: The ID of the resource to update.
        :param data: The data to update the resource with.
        :return: The updated resource.
        """
        resource = session.query(self.model).filter_by(id=resource_id).first()
        for key, value in data.items():
            setattr(resource, key, value)
        return resource

    @provide_session
    def list(self, session: sessionmaker):
        """
        List all resources.
        :return: A list of all resources.
        """
        return session.query(self.model).all()

    @provide_session
    def delete(self, session, resource_id):
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

    @provide_session
    def delete_all(self, session: sessionmaker):
        """
        Delete all resources.
        :return: None
        """
        session.query(self.model).delete()
