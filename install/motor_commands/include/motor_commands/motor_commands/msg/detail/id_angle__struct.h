// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from motor_commands:msg/IdAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_commands/msg/id_angle.h"


#ifndef MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__STRUCT_H_
#define MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__STRUCT_H_

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

/// Struct defined in msg/IdAngle in the package motor_commands.
/**
  * Messages
 */
typedef struct motor_commands__msg__IdAngle
{
  rosidl_runtime_c__uint8__Sequence ids;
  rosidl_runtime_c__int32__Sequence angles;
} motor_commands__msg__IdAngle;

// Struct for a sequence of motor_commands__msg__IdAngle.
typedef struct motor_commands__msg__IdAngle__Sequence
{
  motor_commands__msg__IdAngle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} motor_commands__msg__IdAngle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__STRUCT_H_
