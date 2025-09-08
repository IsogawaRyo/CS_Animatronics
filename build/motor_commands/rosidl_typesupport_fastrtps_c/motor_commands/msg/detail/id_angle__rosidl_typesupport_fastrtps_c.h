// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from motor_commands:msg/IdAngle.idl
// generated code does not contain a copyright notice
#ifndef MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "motor_commands/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "motor_commands/msg/detail/id_angle__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
bool cdr_serialize_motor_commands__msg__IdAngle(
  const motor_commands__msg__IdAngle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
bool cdr_deserialize_motor_commands__msg__IdAngle(
  eprosima::fastcdr::Cdr &,
  motor_commands__msg__IdAngle * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
size_t get_serialized_size_motor_commands__msg__IdAngle(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
size_t max_serialized_size_motor_commands__msg__IdAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
bool cdr_serialize_key_motor_commands__msg__IdAngle(
  const motor_commands__msg__IdAngle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
size_t get_serialized_size_key_motor_commands__msg__IdAngle(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
size_t max_serialized_size_key_motor_commands__msg__IdAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_motor_commands
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, motor_commands, msg, IdAngle)();

#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
