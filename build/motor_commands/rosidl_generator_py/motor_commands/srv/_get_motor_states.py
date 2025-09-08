# generated from rosidl_generator_py/resource/_idl.py.em
# with input from motor_commands:srv/GetMotorStates.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

# Member 'ids'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetMotorStates_Request(type):
    """Metaclass of message 'GetMotorStates_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('motor_commands')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'motor_commands.srv.GetMotorStates_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_motor_states__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_motor_states__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_motor_states__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_motor_states__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_motor_states__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetMotorStates_Request(metaclass=Metaclass_GetMotorStates_Request):
    """Message class 'GetMotorStates_Request'."""

    __slots__ = [
        '_ids',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'ids': 'sequence<uint8>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.ids = array.array('B', kwargs.get('ids', []))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.ids != other.ids:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def ids(self):
        """Message field 'ids'."""
        return self._ids

    @ids.setter
    def ids(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'B', \
                    "The 'ids' array.array() must have the type code of 'B'"
                self._ids = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'ids' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._ids = array.array('B', value)


# Import statements for member types

# Member 'ids'
# Member 'positions'
# Member 'temperatures'
# Member 'torques'
# already imported above
# import array

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_GetMotorStates_Response(type):
    """Metaclass of message 'GetMotorStates_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('motor_commands')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'motor_commands.srv.GetMotorStates_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_motor_states__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_motor_states__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_motor_states__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_motor_states__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_motor_states__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetMotorStates_Response(metaclass=Metaclass_GetMotorStates_Response):
    """Message class 'GetMotorStates_Response'."""

    __slots__ = [
        '_ids',
        '_positions',
        '_temperatures',
        '_torques',
        '_error_status',
        '_port0_total_current',
        '_port1_total_current',
        '_system_total_current',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'ids': 'sequence<uint8>',
        'positions': 'sequence<int32>',
        'temperatures': 'sequence<int32>',
        'torques': 'sequence<int32>',
        'error_status': 'sequence<string>',
        'port0_total_current': 'int32',
        'port1_total_current': 'int32',
        'system_total_current': 'int32',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int32')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int32')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int32')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.ids = array.array('B', kwargs.get('ids', []))
        self.positions = array.array('i', kwargs.get('positions', []))
        self.temperatures = array.array('i', kwargs.get('temperatures', []))
        self.torques = array.array('i', kwargs.get('torques', []))
        self.error_status = kwargs.get('error_status', [])
        self.port0_total_current = kwargs.get('port0_total_current', int())
        self.port1_total_current = kwargs.get('port1_total_current', int())
        self.system_total_current = kwargs.get('system_total_current', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.ids != other.ids:
            return False
        if self.positions != other.positions:
            return False
        if self.temperatures != other.temperatures:
            return False
        if self.torques != other.torques:
            return False
        if self.error_status != other.error_status:
            return False
        if self.port0_total_current != other.port0_total_current:
            return False
        if self.port1_total_current != other.port1_total_current:
            return False
        if self.system_total_current != other.system_total_current:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def ids(self):
        """Message field 'ids'."""
        return self._ids

    @ids.setter
    def ids(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'B', \
                    "The 'ids' array.array() must have the type code of 'B'"
                self._ids = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'ids' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._ids = array.array('B', value)

    @builtins.property
    def positions(self):
        """Message field 'positions'."""
        return self._positions

    @positions.setter
    def positions(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'i', \
                    "The 'positions' array.array() must have the type code of 'i'"
                self._positions = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= -2147483648 and val < 2147483648 for val in value)), \
                "The 'positions' field must be a set or sequence and each value of type 'int' and each integer in [-2147483648, 2147483647]"
        self._positions = array.array('i', value)

    @builtins.property
    def temperatures(self):
        """Message field 'temperatures'."""
        return self._temperatures

    @temperatures.setter
    def temperatures(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'i', \
                    "The 'temperatures' array.array() must have the type code of 'i'"
                self._temperatures = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= -2147483648 and val < 2147483648 for val in value)), \
                "The 'temperatures' field must be a set or sequence and each value of type 'int' and each integer in [-2147483648, 2147483647]"
        self._temperatures = array.array('i', value)

    @builtins.property
    def torques(self):
        """Message field 'torques'."""
        return self._torques

    @torques.setter
    def torques(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'i', \
                    "The 'torques' array.array() must have the type code of 'i'"
                self._torques = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= -2147483648 and val < 2147483648 for val in value)), \
                "The 'torques' field must be a set or sequence and each value of type 'int' and each integer in [-2147483648, 2147483647]"
        self._torques = array.array('i', value)

    @builtins.property
    def error_status(self):
        """Message field 'error_status'."""
        return self._error_status

    @error_status.setter
    def error_status(self, value):
        if self._check_fields:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'error_status' field must be a set or sequence and each value of type 'str'"
        self._error_status = value

    @builtins.property
    def port0_total_current(self):
        """Message field 'port0_total_current'."""
        return self._port0_total_current

    @port0_total_current.setter
    def port0_total_current(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'port0_total_current' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'port0_total_current' field must be an integer in [-2147483648, 2147483647]"
        self._port0_total_current = value

    @builtins.property
    def port1_total_current(self):
        """Message field 'port1_total_current'."""
        return self._port1_total_current

    @port1_total_current.setter
    def port1_total_current(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'port1_total_current' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'port1_total_current' field must be an integer in [-2147483648, 2147483647]"
        self._port1_total_current = value

    @builtins.property
    def system_total_current(self):
        """Message field 'system_total_current'."""
        return self._system_total_current

    @system_total_current.setter
    def system_total_current(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'system_total_current' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'system_total_current' field must be an integer in [-2147483648, 2147483647]"
        self._system_total_current = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_GetMotorStates_Event(type):
    """Metaclass of message 'GetMotorStates_Event'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('motor_commands')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'motor_commands.srv.GetMotorStates_Event')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_motor_states__event
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_motor_states__event
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_motor_states__event
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_motor_states__event
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_motor_states__event

            from service_msgs.msg import ServiceEventInfo
            if ServiceEventInfo.__class__._TYPE_SUPPORT is None:
                ServiceEventInfo.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetMotorStates_Event(metaclass=Metaclass_GetMotorStates_Event):
    """Message class 'GetMotorStates_Event'."""

    __slots__ = [
        '_info',
        '_request',
        '_response',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'info': 'service_msgs/ServiceEventInfo',
        'request': 'sequence<motor_commands/GetMotorStates_Request, 1>',
        'response': 'sequence<motor_commands/GetMotorStates_Response, 1>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['service_msgs', 'msg'], 'ServiceEventInfo'),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['motor_commands', 'srv'], 'GetMotorStates_Request'), 1),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['motor_commands', 'srv'], 'GetMotorStates_Response'), 1),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from service_msgs.msg import ServiceEventInfo
        self.info = kwargs.get('info', ServiceEventInfo())
        self.request = kwargs.get('request', [])
        self.response = kwargs.get('response', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.info != other.info:
            return False
        if self.request != other.request:
            return False
        if self.response != other.response:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def info(self):
        """Message field 'info'."""
        return self._info

    @info.setter
    def info(self, value):
        if self._check_fields:
            from service_msgs.msg import ServiceEventInfo
            assert \
                isinstance(value, ServiceEventInfo), \
                "The 'info' field must be a sub message of type 'ServiceEventInfo'"
        self._info = value

    @builtins.property
    def request(self):
        """Message field 'request'."""
        return self._request

    @request.setter
    def request(self, value):
        if self._check_fields:
            from motor_commands.srv import GetMotorStates_Request
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) <= 1 and
                 all(isinstance(v, GetMotorStates_Request) for v in value) and
                 True), \
                "The 'request' field must be a set or sequence with length <= 1 and each value of type 'GetMotorStates_Request'"
        self._request = value

    @builtins.property
    def response(self):
        """Message field 'response'."""
        return self._response

    @response.setter
    def response(self, value):
        if self._check_fields:
            from motor_commands.srv import GetMotorStates_Response
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) <= 1 and
                 all(isinstance(v, GetMotorStates_Response) for v in value) and
                 True), \
                "The 'response' field must be a set or sequence with length <= 1 and each value of type 'GetMotorStates_Response'"
        self._response = value


class Metaclass_GetMotorStates(type):
    """Metaclass of service 'GetMotorStates'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('motor_commands')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'motor_commands.srv.GetMotorStates')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_motor_states

            from motor_commands.srv import _get_motor_states
            if _get_motor_states.Metaclass_GetMotorStates_Request._TYPE_SUPPORT is None:
                _get_motor_states.Metaclass_GetMotorStates_Request.__import_type_support__()
            if _get_motor_states.Metaclass_GetMotorStates_Response._TYPE_SUPPORT is None:
                _get_motor_states.Metaclass_GetMotorStates_Response.__import_type_support__()
            if _get_motor_states.Metaclass_GetMotorStates_Event._TYPE_SUPPORT is None:
                _get_motor_states.Metaclass_GetMotorStates_Event.__import_type_support__()


class GetMotorStates(metaclass=Metaclass_GetMotorStates):
    from motor_commands.srv._get_motor_states import GetMotorStates_Request as Request
    from motor_commands.srv._get_motor_states import GetMotorStates_Response as Response
    from motor_commands.srv._get_motor_states import GetMotorStates_Event as Event

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
