// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_commands/srv/get_motor_states.h"


#ifndef MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__STRUCT_H_
#define MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'ids'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/GetMotorStates in the package motor_commands.
typedef struct motor_commands__srv__GetMotorStates_Request
{
  rosidl_runtime_c__uint8__Sequence ids;
} motor_commands__srv__GetMotorStates_Request;

// Struct for a sequence of motor_commands__srv__GetMotorStates_Request.
typedef struct motor_commands__srv__GetMotorStates_Request__Sequence
{
  motor_commands__srv__GetMotorStates_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} motor_commands__srv__GetMotorStates_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'ids'
// Member 'positions'
// Member 'temperatures'
// Member 'torques'
// already included above
// #include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/GetMotorStates in the package motor_commands.
typedef struct motor_commands__srv__GetMotorStates_Response
{
  rosidl_runtime_c__uint8__Sequence ids;
  rosidl_runtime_c__int32__Sequence positions;
  rosidl_runtime_c__int32__Sequence temperatures;
  rosidl_runtime_c__int32__Sequence torques;
} motor_commands__srv__GetMotorStates_Response;

// Struct for a sequence of motor_commands__srv__GetMotorStates_Response.
typedef struct motor_commands__srv__GetMotorStates_Response__Sequence
{
  motor_commands__srv__GetMotorStates_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} motor_commands__srv__GetMotorStates_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  motor_commands__srv__GetMotorStates_Event__request__MAX_SIZE = 1
};
// response
enum
{
  motor_commands__srv__GetMotorStates_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/GetMotorStates in the package motor_commands.
typedef struct motor_commands__srv__GetMotorStates_Event
{
  service_msgs__msg__ServiceEventInfo info;
  motor_commands__srv__GetMotorStates_Request__Sequence request;
  motor_commands__srv__GetMotorStates_Response__Sequence response;
} motor_commands__srv__GetMotorStates_Event;

// Struct for a sequence of motor_commands__srv__GetMotorStates_Event.
typedef struct motor_commands__srv__GetMotorStates_Event__Sequence
{
  motor_commands__srv__GetMotorStates_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} motor_commands__srv__GetMotorStates_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__STRUCT_H_
