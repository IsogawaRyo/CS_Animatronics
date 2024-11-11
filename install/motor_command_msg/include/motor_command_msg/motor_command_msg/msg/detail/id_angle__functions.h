// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_command_msg/msg/id_angle.h"


#ifndef MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__FUNCTIONS_H_
#define MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "motor_command_msg/msg/rosidl_generator_c__visibility_control.h"

#include "motor_command_msg/msg/detail/id_angle__struct.h"

/// Initialize msg/IdAngle message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * motor_command_msg__msg__IdAngle
 * )) before or use
 * motor_command_msg__msg__IdAngle__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
bool
motor_command_msg__msg__IdAngle__init(motor_command_msg__msg__IdAngle * msg);

/// Finalize msg/IdAngle message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
void
motor_command_msg__msg__IdAngle__fini(motor_command_msg__msg__IdAngle * msg);

/// Create msg/IdAngle message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * motor_command_msg__msg__IdAngle__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
motor_command_msg__msg__IdAngle *
motor_command_msg__msg__IdAngle__create(void);

/// Destroy msg/IdAngle message.
/**
 * It calls
 * motor_command_msg__msg__IdAngle__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
void
motor_command_msg__msg__IdAngle__destroy(motor_command_msg__msg__IdAngle * msg);

/// Check for msg/IdAngle message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
bool
motor_command_msg__msg__IdAngle__are_equal(const motor_command_msg__msg__IdAngle * lhs, const motor_command_msg__msg__IdAngle * rhs);

/// Copy a msg/IdAngle message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
bool
motor_command_msg__msg__IdAngle__copy(
  const motor_command_msg__msg__IdAngle * input,
  motor_command_msg__msg__IdAngle * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
const rosidl_type_hash_t *
motor_command_msg__msg__IdAngle__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
const rosidl_runtime_c__type_description__TypeDescription *
motor_command_msg__msg__IdAngle__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
const rosidl_runtime_c__type_description__TypeSource *
motor_command_msg__msg__IdAngle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_command_msg__msg__IdAngle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/IdAngle messages.
/**
 * It allocates the memory for the number of elements and calls
 * motor_command_msg__msg__IdAngle__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
bool
motor_command_msg__msg__IdAngle__Sequence__init(motor_command_msg__msg__IdAngle__Sequence * array, size_t size);

/// Finalize array of msg/IdAngle messages.
/**
 * It calls
 * motor_command_msg__msg__IdAngle__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
void
motor_command_msg__msg__IdAngle__Sequence__fini(motor_command_msg__msg__IdAngle__Sequence * array);

/// Create array of msg/IdAngle messages.
/**
 * It allocates the memory for the array and calls
 * motor_command_msg__msg__IdAngle__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
motor_command_msg__msg__IdAngle__Sequence *
motor_command_msg__msg__IdAngle__Sequence__create(size_t size);

/// Destroy array of msg/IdAngle messages.
/**
 * It calls
 * motor_command_msg__msg__IdAngle__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
void
motor_command_msg__msg__IdAngle__Sequence__destroy(motor_command_msg__msg__IdAngle__Sequence * array);

/// Check for msg/IdAngle message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
bool
motor_command_msg__msg__IdAngle__Sequence__are_equal(const motor_command_msg__msg__IdAngle__Sequence * lhs, const motor_command_msg__msg__IdAngle__Sequence * rhs);

/// Copy an array of msg/IdAngle messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_command_msg
bool
motor_command_msg__msg__IdAngle__Sequence__copy(
  const motor_command_msg__msg__IdAngle__Sequence * input,
  motor_command_msg__msg__IdAngle__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__FUNCTIONS_H_
