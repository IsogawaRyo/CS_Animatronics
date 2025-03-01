// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "motor_commands/srv/detail/get_motor_states__functions.h"
#include "motor_commands/srv/detail/get_motor_states__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace motor_commands
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetMotorStates_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetMotorStates_Request_type_support_ids_t;

static const _GetMotorStates_Request_type_support_ids_t _GetMotorStates_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetMotorStates_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetMotorStates_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetMotorStates_Request_type_support_symbol_names_t _GetMotorStates_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, motor_commands, srv, GetMotorStates_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, motor_commands, srv, GetMotorStates_Request)),
  }
};

typedef struct _GetMotorStates_Request_type_support_data_t
{
  void * data[2];
} _GetMotorStates_Request_type_support_data_t;

static _GetMotorStates_Request_type_support_data_t _GetMotorStates_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetMotorStates_Request_message_typesupport_map = {
  2,
  "motor_commands",
  &_GetMotorStates_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GetMotorStates_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GetMotorStates_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetMotorStates_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetMotorStates_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Request__get_type_hash,
  &motor_commands__srv__GetMotorStates_Request__get_type_description,
  &motor_commands__srv__GetMotorStates_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<motor_commands::srv::GetMotorStates_Request>()
{
  return &::motor_commands::srv::rosidl_typesupport_cpp::GetMotorStates_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, motor_commands, srv, GetMotorStates_Request)() {
  return get_message_type_support_handle<motor_commands::srv::GetMotorStates_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__functions.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace motor_commands
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetMotorStates_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetMotorStates_Response_type_support_ids_t;

static const _GetMotorStates_Response_type_support_ids_t _GetMotorStates_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetMotorStates_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetMotorStates_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetMotorStates_Response_type_support_symbol_names_t _GetMotorStates_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, motor_commands, srv, GetMotorStates_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, motor_commands, srv, GetMotorStates_Response)),
  }
};

typedef struct _GetMotorStates_Response_type_support_data_t
{
  void * data[2];
} _GetMotorStates_Response_type_support_data_t;

static _GetMotorStates_Response_type_support_data_t _GetMotorStates_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetMotorStates_Response_message_typesupport_map = {
  2,
  "motor_commands",
  &_GetMotorStates_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GetMotorStates_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GetMotorStates_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetMotorStates_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetMotorStates_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Response__get_type_hash,
  &motor_commands__srv__GetMotorStates_Response__get_type_description,
  &motor_commands__srv__GetMotorStates_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<motor_commands::srv::GetMotorStates_Response>()
{
  return &::motor_commands::srv::rosidl_typesupport_cpp::GetMotorStates_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, motor_commands, srv, GetMotorStates_Response)() {
  return get_message_type_support_handle<motor_commands::srv::GetMotorStates_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__functions.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace motor_commands
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetMotorStates_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetMotorStates_Event_type_support_ids_t;

static const _GetMotorStates_Event_type_support_ids_t _GetMotorStates_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetMotorStates_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetMotorStates_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetMotorStates_Event_type_support_symbol_names_t _GetMotorStates_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, motor_commands, srv, GetMotorStates_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, motor_commands, srv, GetMotorStates_Event)),
  }
};

typedef struct _GetMotorStates_Event_type_support_data_t
{
  void * data[2];
} _GetMotorStates_Event_type_support_data_t;

static _GetMotorStates_Event_type_support_data_t _GetMotorStates_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetMotorStates_Event_message_typesupport_map = {
  2,
  "motor_commands",
  &_GetMotorStates_Event_message_typesupport_ids.typesupport_identifier[0],
  &_GetMotorStates_Event_message_typesupport_symbol_names.symbol_name[0],
  &_GetMotorStates_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetMotorStates_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetMotorStates_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Event__get_type_hash,
  &motor_commands__srv__GetMotorStates_Event__get_type_description,
  &motor_commands__srv__GetMotorStates_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<motor_commands::srv::GetMotorStates_Event>()
{
  return &::motor_commands::srv::rosidl_typesupport_cpp::GetMotorStates_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, motor_commands, srv, GetMotorStates_Event)() {
  return get_message_type_support_handle<motor_commands::srv::GetMotorStates_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace motor_commands
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetMotorStates_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetMotorStates_type_support_ids_t;

static const _GetMotorStates_type_support_ids_t _GetMotorStates_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetMotorStates_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetMotorStates_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetMotorStates_type_support_symbol_names_t _GetMotorStates_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, motor_commands, srv, GetMotorStates)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, motor_commands, srv, GetMotorStates)),
  }
};

typedef struct _GetMotorStates_type_support_data_t
{
  void * data[2];
} _GetMotorStates_type_support_data_t;

static _GetMotorStates_type_support_data_t _GetMotorStates_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetMotorStates_service_typesupport_map = {
  2,
  "motor_commands",
  &_GetMotorStates_service_typesupport_ids.typesupport_identifier[0],
  &_GetMotorStates_service_typesupport_symbol_names.symbol_name[0],
  &_GetMotorStates_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GetMotorStates_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetMotorStates_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<motor_commands::srv::GetMotorStates_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<motor_commands::srv::GetMotorStates_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<motor_commands::srv::GetMotorStates_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<motor_commands::srv::GetMotorStates>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<motor_commands::srv::GetMotorStates>,
  &motor_commands__srv__GetMotorStates__get_type_hash,
  &motor_commands__srv__GetMotorStates__get_type_description,
  &motor_commands__srv__GetMotorStates__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<motor_commands::srv::GetMotorStates>()
{
  return &::motor_commands::srv::rosidl_typesupport_cpp::GetMotorStates_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, motor_commands, srv, GetMotorStates)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<motor_commands::srv::GetMotorStates>();
}

#ifdef __cplusplus
}
#endif
