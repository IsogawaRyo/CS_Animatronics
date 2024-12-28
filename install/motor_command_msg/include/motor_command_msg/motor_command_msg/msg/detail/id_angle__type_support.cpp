// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "motor_command_msg/msg/detail/id_angle__functions.h"
#include "motor_command_msg/msg/detail/id_angle__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace motor_command_msg
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void IdAngle_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) motor_command_msg::msg::IdAngle(_init);
}

void IdAngle_fini_function(void * message_memory)
{
  auto typed_message = static_cast<motor_command_msg::msg::IdAngle *>(message_memory);
  typed_message->~IdAngle();
}

size_t size_function__IdAngle__ids(const void * untyped_member)
{
  (void)untyped_member;
  return 10;
}

const void * get_const_function__IdAngle__ids(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<uint8_t, 10> *>(untyped_member);
  return &member[index];
}

void * get_function__IdAngle__ids(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<uint8_t, 10> *>(untyped_member);
  return &member[index];
}

void fetch_function__IdAngle__ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint8_t *>(
    get_const_function__IdAngle__ids(untyped_member, index));
  auto & value = *reinterpret_cast<uint8_t *>(untyped_value);
  value = item;
}

void assign_function__IdAngle__ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint8_t *>(
    get_function__IdAngle__ids(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint8_t *>(untyped_value);
  item = value;
}

size_t size_function__IdAngle__angles(const void * untyped_member)
{
  (void)untyped_member;
  return 10;
}

const void * get_const_function__IdAngle__angles(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<int32_t, 10> *>(untyped_member);
  return &member[index];
}

void * get_function__IdAngle__angles(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<int32_t, 10> *>(untyped_member);
  return &member[index];
}

void fetch_function__IdAngle__angles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const int32_t *>(
    get_const_function__IdAngle__angles(untyped_member, index));
  auto & value = *reinterpret_cast<int32_t *>(untyped_value);
  value = item;
}

void assign_function__IdAngle__angles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<int32_t *>(
    get_function__IdAngle__angles(untyped_member, index));
  const auto & value = *reinterpret_cast<const int32_t *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember IdAngle_message_member_array[2] = {
  {
    "ids",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    10,  // array size
    false,  // is upper bound
    offsetof(motor_command_msg::msg::IdAngle, ids),  // bytes offset in struct
    nullptr,  // default value
    size_function__IdAngle__ids,  // size() function pointer
    get_const_function__IdAngle__ids,  // get_const(index) function pointer
    get_function__IdAngle__ids,  // get(index) function pointer
    fetch_function__IdAngle__ids,  // fetch(index, &value) function pointer
    assign_function__IdAngle__ids,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "angles",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    10,  // array size
    false,  // is upper bound
    offsetof(motor_command_msg::msg::IdAngle, angles),  // bytes offset in struct
    nullptr,  // default value
    size_function__IdAngle__angles,  // size() function pointer
    get_const_function__IdAngle__angles,  // get_const(index) function pointer
    get_function__IdAngle__angles,  // get(index) function pointer
    fetch_function__IdAngle__angles,  // fetch(index, &value) function pointer
    assign_function__IdAngle__angles,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers IdAngle_message_members = {
  "motor_command_msg::msg",  // message namespace
  "IdAngle",  // message name
  2,  // number of fields
  sizeof(motor_command_msg::msg::IdAngle),
  false,  // has_any_key_member_
  IdAngle_message_member_array,  // message members
  IdAngle_init_function,  // function to initialize message memory (memory has to be allocated)
  IdAngle_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t IdAngle_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &IdAngle_message_members,
  get_message_typesupport_handle_function,
  &motor_command_msg__msg__IdAngle__get_type_hash,
  &motor_command_msg__msg__IdAngle__get_type_description,
  &motor_command_msg__msg__IdAngle__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace motor_command_msg


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<motor_command_msg::msg::IdAngle>()
{
  return &::motor_command_msg::msg::rosidl_typesupport_introspection_cpp::IdAngle_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, motor_command_msg, msg, IdAngle)() {
  return &::motor_command_msg::msg::rosidl_typesupport_introspection_cpp::IdAngle_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
