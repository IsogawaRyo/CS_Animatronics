// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from motor_commands:msg/IdAngle.idl
// generated code does not contain a copyright notice

#include "motor_commands/msg/detail/id_angle__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__msg__IdAngle__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x05, 0xea, 0xb5, 0x69, 0x54, 0xb5, 0xed, 0xb6,
      0x29, 0x2c, 0xdd, 0xe2, 0x86, 0x31, 0x1f, 0xfc,
      0x3b, 0x8c, 0x4f, 0xe7, 0xc8, 0xcb, 0x6e, 0xb5,
      0x3b, 0x56, 0xba, 0x86, 0x5a, 0x72, 0xba, 0x13,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char motor_commands__msg__IdAngle__TYPE_NAME[] = "motor_commands/msg/IdAngle";

// Define type names, field names, and default values
static char motor_commands__msg__IdAngle__FIELD_NAME__ids[] = "ids";
static char motor_commands__msg__IdAngle__FIELD_NAME__angles[] = "angles";

static rosidl_runtime_c__type_description__Field motor_commands__msg__IdAngle__FIELDS[] = {
  {
    {motor_commands__msg__IdAngle__FIELD_NAME__ids, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8_ARRAY,
      12,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__msg__IdAngle__FIELD_NAME__angles, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_ARRAY,
      12,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__msg__IdAngle__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {motor_commands__msg__IdAngle__TYPE_NAME, 26, 26},
      {motor_commands__msg__IdAngle__FIELDS, 2, 2},
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
  "uint8[12] ids\n"
  "int32[12] angles";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
motor_commands__msg__IdAngle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {motor_commands__msg__IdAngle__TYPE_NAME, 26, 26},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 42, 42},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__msg__IdAngle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *motor_commands__msg__IdAngle__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
