// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "motor_command_msg/msg/detail/id_angle__rosidl_typesupport_introspection_c.h"
#include "motor_command_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "motor_command_msg/msg/detail/id_angle__functions.h"
#include "motor_command_msg/msg/detail/id_angle__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  motor_command_msg__msg__IdAngle__init(message_memory);
}

void motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_fini_function(void * message_memory)
{
  motor_command_msg__msg__IdAngle__fini(message_memory);
}

size_t motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__size_function__IdAngle__ids(
  const void * untyped_member)
{
  (void)untyped_member;
  return 76800;
}

const void * motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_const_function__IdAngle__ids(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_function__IdAngle__ids(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__fetch_function__IdAngle__ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_const_function__IdAngle__ids(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__assign_function__IdAngle__ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_function__IdAngle__ids(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__size_function__IdAngle__angles(
  const void * untyped_member)
{
  (void)untyped_member;
  return 76800;
}

const void * motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_const_function__IdAngle__angles(
  const void * untyped_member, size_t index)
{
  const int32_t * member =
    (const int32_t *)(untyped_member);
  return &member[index];
}

void * motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_function__IdAngle__angles(
  void * untyped_member, size_t index)
{
  int32_t * member =
    (int32_t *)(untyped_member);
  return &member[index];
}

void motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__fetch_function__IdAngle__angles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_const_function__IdAngle__angles(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__assign_function__IdAngle__angles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_function__IdAngle__angles(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_member_array[2] = {
  {
    "ids",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    76800,  // array size
    false,  // is upper bound
    offsetof(motor_command_msg__msg__IdAngle, ids),  // bytes offset in struct
    NULL,  // default value
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__size_function__IdAngle__ids,  // size() function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_const_function__IdAngle__ids,  // get_const(index) function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_function__IdAngle__ids,  // get(index) function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__fetch_function__IdAngle__ids,  // fetch(index, &value) function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__assign_function__IdAngle__ids,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    76800,  // array size
    false,  // is upper bound
    offsetof(motor_command_msg__msg__IdAngle, angles),  // bytes offset in struct
    NULL,  // default value
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__size_function__IdAngle__angles,  // size() function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_const_function__IdAngle__angles,  // get_const(index) function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__get_function__IdAngle__angles,  // get(index) function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__fetch_function__IdAngle__angles,  // fetch(index, &value) function pointer
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__assign_function__IdAngle__angles,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_members = {
  "motor_command_msg__msg",  // message namespace
  "IdAngle",  // message name
  2,  // number of fields
  sizeof(motor_command_msg__msg__IdAngle),
  false,  // has_any_key_member_
  motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_member_array,  // message members
  motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_init_function,  // function to initialize message memory (memory has to be allocated)
  motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_type_support_handle = {
  0,
  &motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_members,
  get_message_typesupport_handle_function,
  &motor_command_msg__msg__IdAngle__get_type_hash,
  &motor_command_msg__msg__IdAngle__get_type_description,
  &motor_command_msg__msg__IdAngle__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_motor_command_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_command_msg, msg, IdAngle)() {
  if (!motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_type_support_handle.typesupport_identifier) {
    motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &motor_command_msg__msg__IdAngle__rosidl_typesupport_introspection_c__IdAngle_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
