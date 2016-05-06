from imagination.action              import Action
from imagination.decorator.validator import restrict_type

class InterceptableObject(object):
    def __init__(self):
        self._locked        = False
        self._interceptable = False
        self._interceptions = []

    def lock(self):
        """ Lock the object """
        self._locked = True

    def unlock(self):
        """ Unlock the object """
        self._locked = True

    @property
    def locked(self):
        """ Flag indicating whether the object is locked

            :rtype: bool
        """
        return self._locked

    @property
    def interceptable(self):
        '''
        Flag if this entity is interceptable

        :rtype: boolean
        '''
        return self._interceptable

    @interceptable.setter
    @restrict_type(bool)
    def interceptable(self, interceptable):
        '''
        Define if this entity is interceptable.

        :param interceptable: Flag if this entity is interceptable
        :type  interceptable: boolean
        '''
        if self.locked:
            raise LockedEntityException

        self._interceptable = interceptable

    @property
    def interceptions(self):
        '''
        Retrieve the list of interceptions.
        '''
        return self._interceptions

    @interceptions.setter
    @restrict_type(list)
    def interceptions(self, interceptions):
        '''
        Define the list of interceptions.

        :param interceptions: list of interceptions
        :type  interceptions: list
        '''
        self._interceptions = interceptions

    def register_interception(self, interception):
        self._interceptions.append(interception)

    def _bind_interceptions(self, instance, interceptions):
        for attribute in dir(instance):
            if attribute[0] == '_':
                continue

            ref = instance.__getattribute__(attribute)

            if not callable(ref) or isinstance(ref, Action):
                continue

            new_ref = Action(ref)

            for interception in interceptions:
                if interception.actor.method_name != attribute:
                    continue

                new_ref.register(interception)

            try:
                instance.__setattr__(attribute, new_ref)
            except AttributeError:
                pass
