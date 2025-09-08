// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from motor_commands:msg/IdAngle.idl
// generated code does not contain a copyright notice

#ifndef MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "motor_commands/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "motor_commands/msg/detail/id_angle__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace motor_commands
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
cdr_serialize(
  const motor_commands::msg::IdAngle & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  motor_commands::msg::IdAngle & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
get_serialized_size(
  const motor_commands::msg::IdAngle & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
max_serialized_size_IdAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
cdr_serialize_key(
  const motor_commands::msg::IdAngle & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
get_serialized_size_key(
  const motor_commands::msg::IdAngle & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
max_serialized_size_key_IdAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace motor_commands

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_motor_commands
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, motor_commands, msg, IdAngle)();

#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMANDS__MSG__DETAIL__ID_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
