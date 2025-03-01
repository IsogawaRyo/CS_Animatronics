// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "motor_commands/srv/detail/get_motor_states__rosidl_typesupport_introspection_c.h"
#include "motor_commands/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "motor_commands/srv/detail/get_motor_states__functions.h"
#include "motor_commands/srv/detail/get_motor_states__struct.h"


// Include directives for member types
// Member `ids`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  motor_commands__srv__GetMotorStates_Request__init(message_memory);
}

void motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_fini_function(void * message_memory)
{
  motor_commands__srv__GetMotorStates_Request__fini(message_memory);
}

size_t motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Request__ids(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Request__ids(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Request__ids(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Request__ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Request__ids(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Request__ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Request__ids(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Request__ids(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_member_array[1] = {
  {
    "ids",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Request, ids),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Request__ids,  // size() function pointer
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Request__ids,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Request__ids,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Request__ids,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Request__ids,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Request__ids  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_members = {
  "motor_commands__srv",  // message namespace
  "GetMotorStates_Request",  // message name
  1,  // number of fields
  sizeof(motor_commands__srv__GetMotorStates_Request),
  false,  // has_any_key_member_
  motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_member_array,  // message members
  motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_type_support_handle = {
  0,
  &motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_members,
  get_message_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Request__get_type_hash,
  &motor_commands__srv__GetMotorStates_Request__get_type_description,
  &motor_commands__srv__GetMotorStates_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_motor_commands
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Request)() {
  if (!motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_type_support_handle.typesupport_identifier) {
    motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "motor_commands/srv/detail/get_motor_states__rosidl_typesupport_introspection_c.h"
// already included above
// #include "motor_commands/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__functions.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__struct.h"


// Include directives for member types
// Member `ids`
// Member `positions`
// Member `temperatures`
// Member `torques`
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  motor_commands__srv__GetMotorStates_Response__init(message_memory);
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_fini_function(void * message_memory)
{
  motor_commands__srv__GetMotorStates_Response__fini(message_memory);
}

size_t motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__ids(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__ids(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__ids(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__ids(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__ids(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__ids(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

size_t motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__positions(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__positions(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

size_t motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__temperatures(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__temperatures(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__temperatures(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__temperatures(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__temperatures(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__temperatures(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__temperatures(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__temperatures(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

size_t motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__torques(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__torques(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__torques(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__torques(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__torques(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__torques(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__torques(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__torques(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_member_array[4] = {
  {
    "ids",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Response, ids),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__ids,  // size() function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__ids,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__ids,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__ids,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__ids,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__ids  // resize(index) function pointer
  },
  {
    "positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Response, positions),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__positions,  // size() function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__positions,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__positions,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__positions,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__positions,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__positions  // resize(index) function pointer
  },
  {
    "temperatures",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Response, temperatures),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__temperatures,  // size() function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__temperatures,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__temperatures,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__temperatures,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__temperatures,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__temperatures  // resize(index) function pointer
  },
  {
    "torques",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Response, torques),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Response__torques,  // size() function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Response__torques,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Response__torques,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Response__torques,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Response__torques,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Response__torques  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_members = {
  "motor_commands__srv",  // message namespace
  "GetMotorStates_Response",  // message name
  4,  // number of fields
  sizeof(motor_commands__srv__GetMotorStates_Response),
  false,  // has_any_key_member_
  motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_member_array,  // message members
  motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle = {
  0,
  &motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_members,
  get_message_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Response__get_type_hash,
  &motor_commands__srv__GetMotorStates_Response__get_type_description,
  &motor_commands__srv__GetMotorStates_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_motor_commands
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Response)() {
  if (!motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle.typesupport_identifier) {
    motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "motor_commands/srv/detail/get_motor_states__rosidl_typesupport_introspection_c.h"
// already included above
// #include "motor_commands/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__functions.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "motor_commands/srv/get_motor_states.h"
// Member `request`
// Member `response`
// already included above
// #include "motor_commands/srv/detail/get_motor_states__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  motor_commands__srv__GetMotorStates_Event__init(message_memory);
}

void motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_fini_function(void * message_memory)
{
  motor_commands__srv__GetMotorStates_Event__fini(message_memory);
}

size_t motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Event__request(
  const void * untyped_member)
{
  const motor_commands__srv__GetMotorStates_Request__Sequence * member =
    (const motor_commands__srv__GetMotorStates_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Event__request(
  const void * untyped_member, size_t index)
{
  const motor_commands__srv__GetMotorStates_Request__Sequence * member =
    (const motor_commands__srv__GetMotorStates_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Event__request(
  void * untyped_member, size_t index)
{
  motor_commands__srv__GetMotorStates_Request__Sequence * member =
    (motor_commands__srv__GetMotorStates_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const motor_commands__srv__GetMotorStates_Request * item =
    ((const motor_commands__srv__GetMotorStates_Request *)
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Event__request(untyped_member, index));
  motor_commands__srv__GetMotorStates_Request * value =
    (motor_commands__srv__GetMotorStates_Request *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  motor_commands__srv__GetMotorStates_Request * item =
    ((motor_commands__srv__GetMotorStates_Request *)
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Event__request(untyped_member, index));
  const motor_commands__srv__GetMotorStates_Request * value =
    (const motor_commands__srv__GetMotorStates_Request *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Event__request(
  void * untyped_member, size_t size)
{
  motor_commands__srv__GetMotorStates_Request__Sequence * member =
    (motor_commands__srv__GetMotorStates_Request__Sequence *)(untyped_member);
  motor_commands__srv__GetMotorStates_Request__Sequence__fini(member);
  return motor_commands__srv__GetMotorStates_Request__Sequence__init(member, size);
}

size_t motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Event__response(
  const void * untyped_member)
{
  const motor_commands__srv__GetMotorStates_Response__Sequence * member =
    (const motor_commands__srv__GetMotorStates_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Event__response(
  const void * untyped_member, size_t index)
{
  const motor_commands__srv__GetMotorStates_Response__Sequence * member =
    (const motor_commands__srv__GetMotorStates_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Event__response(
  void * untyped_member, size_t index)
{
  motor_commands__srv__GetMotorStates_Response__Sequence * member =
    (motor_commands__srv__GetMotorStates_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const motor_commands__srv__GetMotorStates_Response * item =
    ((const motor_commands__srv__GetMotorStates_Response *)
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Event__response(untyped_member, index));
  motor_commands__srv__GetMotorStates_Response * value =
    (motor_commands__srv__GetMotorStates_Response *)(untyped_value);
  *value = *item;
}

void motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  motor_commands__srv__GetMotorStates_Response * item =
    ((motor_commands__srv__GetMotorStates_Response *)
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Event__response(untyped_member, index));
  const motor_commands__srv__GetMotorStates_Response * value =
    (const motor_commands__srv__GetMotorStates_Response *)(untyped_value);
  *item = *value;
}

bool motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Event__response(
  void * untyped_member, size_t size)
{
  motor_commands__srv__GetMotorStates_Response__Sequence * member =
    (motor_commands__srv__GetMotorStates_Response__Sequence *)(untyped_member);
  motor_commands__srv__GetMotorStates_Response__Sequence__fini(member);
  return motor_commands__srv__GetMotorStates_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Event, request),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Event__request,  // size() function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Event__request,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Event__request,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Event__request,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Event__request,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(motor_commands__srv__GetMotorStates_Event, response),  // bytes offset in struct
    NULL,  // default value
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__size_function__GetMotorStates_Event__response,  // size() function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_const_function__GetMotorStates_Event__response,  // get_const(index) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__get_function__GetMotorStates_Event__response,  // get(index) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__fetch_function__GetMotorStates_Event__response,  // fetch(index, &value) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__assign_function__GetMotorStates_Event__response,  // assign(index, value) function pointer
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__resize_function__GetMotorStates_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_members = {
  "motor_commands__srv",  // message namespace
  "GetMotorStates_Event",  // message name
  3,  // number of fields
  sizeof(motor_commands__srv__GetMotorStates_Event),
  false,  // has_any_key_member_
  motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_member_array,  // message members
  motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_type_support_handle = {
  0,
  &motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_members,
  get_message_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Event__get_type_hash,
  &motor_commands__srv__GetMotorStates_Event__get_type_description,
  &motor_commands__srv__GetMotorStates_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_motor_commands
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Event)() {
  motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Request)();
  motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Response)();
  if (!motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_type_support_handle.typesupport_identifier) {
    motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "motor_commands/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "motor_commands/srv/detail/get_motor_states__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_members = {
  "motor_commands__srv",  // service namespace
  "GetMotorStates",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_type_support_handle,
  NULL,  // response message
  // motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle
  NULL  // event_message
  // motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle
};


static rosidl_service_type_support_t motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_type_support_handle = {
  0,
  &motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_members,
  get_service_typesupport_handle_function,
  &motor_commands__srv__GetMotorStates_Request__rosidl_typesupport_introspection_c__GetMotorStates_Request_message_type_support_handle,
  &motor_commands__srv__GetMotorStates_Response__rosidl_typesupport_introspection_c__GetMotorStates_Response_message_type_support_handle,
  &motor_commands__srv__GetMotorStates_Event__rosidl_typesupport_introspection_c__GetMotorStates_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    motor_commands,
    srv,
    GetMotorStates
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    motor_commands,
    srv,
    GetMotorStates
  ),
  &motor_commands__srv__GetMotorStates__get_type_hash,
  &motor_commands__srv__GetMotorStates__get_type_description,
  &motor_commands__srv__GetMotorStates__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_motor_commands
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates)(void) {
  if (!motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_type_support_handle.typesupport_identifier) {
    motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, motor_commands, srv, GetMotorStates_Event)()->data;
  }

  return &motor_commands__srv__detail__get_motor_states__rosidl_typesupport_introspection_c__GetMotorStates_service_type_support_handle;
}
