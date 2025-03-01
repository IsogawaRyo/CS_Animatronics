// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

#include "motor_commands/srv/detail/get_motor_states__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xdd, 0x15, 0xc7, 0xa3, 0x65, 0x2f, 0x3a, 0x52,
      0xc4, 0x4c, 0x08, 0xec, 0xf7, 0x9b, 0x6d, 0x4c,
      0x82, 0x8b, 0x21, 0x51, 0x33, 0xca, 0x57, 0x4f,
      0xd7, 0x5b, 0xf8, 0xee, 0x53, 0x49, 0xea, 0x84,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x8d, 0xaa, 0xc4, 0xc5, 0x0a, 0xa5, 0xea, 0x59,
      0xbd, 0xf8, 0xc4, 0x4b, 0xb5, 0xa6, 0x77, 0x39,
      0x06, 0x40, 0x6f, 0xc6, 0x12, 0xa2, 0x94, 0x14,
      0x8c, 0x8d, 0x3e, 0x3e, 0x3e, 0x9f, 0x43, 0xac,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x78, 0x91, 0x03, 0xb2, 0xfe, 0x75, 0x5a, 0x8f,
      0x3f, 0xa3, 0x67, 0x37, 0x1b, 0x88, 0xa3, 0xe4,
      0xfa, 0xb3, 0xc7, 0x27, 0x8f, 0xc5, 0xb3, 0x3b,
      0xbc, 0x63, 0x3f, 0x74, 0x6c, 0x48, 0x7a, 0xf1,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xff, 0x59, 0x42, 0xb1, 0xbc, 0x53, 0x03, 0xb3,
      0xea, 0x7e, 0x26, 0x45, 0x74, 0xed, 0xc0, 0xf6,
      0xde, 0xaf, 0x59, 0x25, 0x0c, 0x72, 0x86, 0xc9,
      0x86, 0xb3, 0x9b, 0xc4, 0xdc, 0x4f, 0x13, 0xe2,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "service_msgs/msg/detail/service_event_info__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char motor_commands__srv__GetMotorStates__TYPE_NAME[] = "motor_commands/srv/GetMotorStates";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char motor_commands__srv__GetMotorStates_Event__TYPE_NAME[] = "motor_commands/srv/GetMotorStates_Event";
static char motor_commands__srv__GetMotorStates_Request__TYPE_NAME[] = "motor_commands/srv/GetMotorStates_Request";
static char motor_commands__srv__GetMotorStates_Response__TYPE_NAME[] = "motor_commands/srv/GetMotorStates_Response";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char motor_commands__srv__GetMotorStates__FIELD_NAME__request_message[] = "request_message";
static char motor_commands__srv__GetMotorStates__FIELD_NAME__response_message[] = "response_message";
static char motor_commands__srv__GetMotorStates__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field motor_commands__srv__GetMotorStates__FIELDS[] = {
  {
    {motor_commands__srv__GetMotorStates__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {motor_commands__srv__GetMotorStates_Request__TYPE_NAME, 41, 41},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {motor_commands__srv__GetMotorStates_Response__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {motor_commands__srv__GetMotorStates_Event__TYPE_NAME, 39, 39},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription motor_commands__srv__GetMotorStates__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Event__TYPE_NAME, 39, 39},
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Request__TYPE_NAME, 41, 41},
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Response__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {motor_commands__srv__GetMotorStates__TYPE_NAME, 33, 33},
      {motor_commands__srv__GetMotorStates__FIELDS, 3, 3},
    },
    {motor_commands__srv__GetMotorStates__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = motor_commands__srv__GetMotorStates_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = motor_commands__srv__GetMotorStates_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = motor_commands__srv__GetMotorStates_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char motor_commands__srv__GetMotorStates_Request__FIELD_NAME__ids[] = "ids";

static rosidl_runtime_c__type_description__Field motor_commands__srv__GetMotorStates_Request__FIELDS[] = {
  {
    {motor_commands__srv__GetMotorStates_Request__FIELD_NAME__ids, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {motor_commands__srv__GetMotorStates_Request__TYPE_NAME, 41, 41},
      {motor_commands__srv__GetMotorStates_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char motor_commands__srv__GetMotorStates_Response__FIELD_NAME__ids[] = "ids";
static char motor_commands__srv__GetMotorStates_Response__FIELD_NAME__positions[] = "positions";
static char motor_commands__srv__GetMotorStates_Response__FIELD_NAME__temperatures[] = "temperatures";
static char motor_commands__srv__GetMotorStates_Response__FIELD_NAME__torques[] = "torques";

static rosidl_runtime_c__type_description__Field motor_commands__srv__GetMotorStates_Response__FIELDS[] = {
  {
    {motor_commands__srv__GetMotorStates_Response__FIELD_NAME__ids, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Response__FIELD_NAME__positions, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Response__FIELD_NAME__temperatures, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Response__FIELD_NAME__torques, 7, 7},
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
motor_commands__srv__GetMotorStates_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {motor_commands__srv__GetMotorStates_Response__TYPE_NAME, 42, 42},
      {motor_commands__srv__GetMotorStates_Response__FIELDS, 4, 4},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char motor_commands__srv__GetMotorStates_Event__FIELD_NAME__info[] = "info";
static char motor_commands__srv__GetMotorStates_Event__FIELD_NAME__request[] = "request";
static char motor_commands__srv__GetMotorStates_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field motor_commands__srv__GetMotorStates_Event__FIELDS[] = {
  {
    {motor_commands__srv__GetMotorStates_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {motor_commands__srv__GetMotorStates_Request__TYPE_NAME, 41, 41},
    },
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {motor_commands__srv__GetMotorStates_Response__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription motor_commands__srv__GetMotorStates_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Request__TYPE_NAME, 41, 41},
    {NULL, 0, 0},
  },
  {
    {motor_commands__srv__GetMotorStates_Response__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {motor_commands__srv__GetMotorStates_Event__TYPE_NAME, 39, 39},
      {motor_commands__srv__GetMotorStates_Event__FIELDS, 3, 3},
    },
    {motor_commands__srv__GetMotorStates_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = motor_commands__srv__GetMotorStates_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = motor_commands__srv__GetMotorStates_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint8[] ids\n"
  "---\n"
  "uint8[] ids\n"
  "int32[] positions\n"
  "int32[] temperatures\n"
  "int32[] torques";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {motor_commands__srv__GetMotorStates__TYPE_NAME, 33, 33},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 83, 83},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {motor_commands__srv__GetMotorStates_Request__TYPE_NAME, 41, 41},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {motor_commands__srv__GetMotorStates_Response__TYPE_NAME, 42, 42},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {motor_commands__srv__GetMotorStates_Event__TYPE_NAME, 39, 39},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *motor_commands__srv__GetMotorStates__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *motor_commands__srv__GetMotorStates_Event__get_individual_type_description_source(NULL);
    sources[3] = *motor_commands__srv__GetMotorStates_Request__get_individual_type_description_source(NULL);
    sources[4] = *motor_commands__srv__GetMotorStates_Response__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *motor_commands__srv__GetMotorStates_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *motor_commands__srv__GetMotorStates_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *motor_commands__srv__GetMotorStates_Event__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *motor_commands__srv__GetMotorStates_Request__get_individual_type_description_source(NULL);
    sources[3] = *motor_commands__srv__GetMotorStates_Response__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
