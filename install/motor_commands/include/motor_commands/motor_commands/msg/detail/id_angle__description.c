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
      0x92, 0x9d, 0xc5, 0xaf, 0x6b, 0x8e, 0x08, 0x05,
      0x5c, 0xd9, 0xef, 0x0e, 0xe4, 0x66, 0x43, 0x1a,
      0xf3, 0x88, 0x45, 0xb4, 0x59, 0x3c, 0x4e, 0xc7,
      0xc2, 0x58, 0x71, 0x09, 0x9c, 0x9b, 0x8e, 0x70,
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
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__msg__IdAngle__FIELD_NAME__angles, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_UNBOUNDED_SEQUENCE,
      0,
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
  "uint8[] ids\n"
  "int32[] angles";

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
    {toplevel_type_raw_source, 38, 38},
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
