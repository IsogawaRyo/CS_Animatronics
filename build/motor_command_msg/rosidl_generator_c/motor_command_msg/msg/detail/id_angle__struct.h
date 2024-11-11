// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_command_msg/msg/id_angle.h"


#ifndef MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__STRUCT_H_
#define MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__STRUCT_H_

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
// Member 'angles'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/IdAngle in the package motor_command_msg.
typedef struct motor_command_msg__msg__IdAngle
{
  rosidl_runtime_c__int32__Sequence ids;
  rosidl_runtime_c__double__Sequence angles;
} motor_command_msg__msg__IdAngle;

// Struct for a sequence of motor_command_msg__msg__IdAngle.
typedef struct motor_command_msg__msg__IdAngle__Sequence
{
  motor_command_msg__msg__IdAngle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} motor_command_msg__msg__IdAngle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__STRUCT_H_
