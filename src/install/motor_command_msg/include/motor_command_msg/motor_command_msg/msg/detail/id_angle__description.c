// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

#include "motor_command_msg/msg/detail/id_angle__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
const rosidl_type_hash_t *
motor_command_msg__msg__IdAngle__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xcc, 0xab, 0xf0, 0x68, 0x7f, 0xa0, 0xa0, 0x38,
      0x48, 0x1d, 0xb8, 0xf7, 0x29, 0xb2, 0x95, 0x3d,
      0xa1, 0xd6, 0x50, 0x42, 0x62, 0x73, 0xce, 0xcd,
      0x2e, 0x5b, 0xc6, 0x25, 0x84, 0xa5, 0x26, 0xda,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char motor_command_msg__msg__IdAngle__TYPE_NAME[] = "motor_command_msg/msg/IdAngle";

// Define type names, field names, and default values
static char motor_command_msg__msg__IdAngle__FIELD_NAME__ids[] = "ids";
static char motor_command_msg__msg__IdAngle__FIELD_NAME__angles[] = "angles";

static rosidl_runtime_c__type_description__Field motor_command_msg__msg__IdAngle__FIELDS[] = {
  {
    {motor_command_msg__msg__IdAngle__FIELD_NAME__ids, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8_ARRAY,
      10,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {motor_command_msg__msg__IdAngle__FIELD_NAME__angles, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_ARRAY,
      10,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
motor_command_msg__msg__IdAngle__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {motor_command_msg__msg__IdAngle__TYPE_NAME, 29, 29},
      {motor_command_msg__msg__IdAngle__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Messages\n"
  "uint8[10] ids\n"
  "int32[10] angles";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
motor_command_msg__msg__IdAngle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {motor_command_msg__msg__IdAngle__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 42, 42},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_command_msg__msg__IdAngle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *motor_command_msg__msg__IdAngle__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
