// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_commands/srv/get_motor_states.h"


#ifndef MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__FUNCTIONS_H_
#define MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__FUNCTIONS_H_

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
#include "motor_commands/msg/rosidl_generator_c__visibility_control.h"

#include "motor_commands/srv/detail/get_motor_states__struct.h"

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates__get_type_hash(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates__get_type_description(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates__get_type_description_sources(
  const rosidl_service_type_support_t * type_support);

/// Initialize srv/GetMotorStates message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * motor_commands__srv__GetMotorStates_Request
 * )) before or use
 * motor_commands__srv__GetMotorStates_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Request__init(motor_commands__srv__GetMotorStates_Request * msg);

/// Finalize srv/GetMotorStates message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Request__fini(motor_commands__srv__GetMotorStates_Request * msg);

/// Create srv/GetMotorStates message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * motor_commands__srv__GetMotorStates_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
motor_commands__srv__GetMotorStates_Request *
motor_commands__srv__GetMotorStates_Request__create(void);

/// Destroy srv/GetMotorStates message.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Request__destroy(motor_commands__srv__GetMotorStates_Request * msg);

/// Check for srv/GetMotorStates message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Request__are_equal(const motor_commands__srv__GetMotorStates_Request * lhs, const motor_commands__srv__GetMotorStates_Request * rhs);

/// Copy a srv/GetMotorStates message.
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
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Request__copy(
  const motor_commands__srv__GetMotorStates_Request * input,
  motor_commands__srv__GetMotorStates_Request * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates_Request__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/GetMotorStates messages.
/**
 * It allocates the memory for the number of elements and calls
 * motor_commands__srv__GetMotorStates_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Request__Sequence__init(motor_commands__srv__GetMotorStates_Request__Sequence * array, size_t size);

/// Finalize array of srv/GetMotorStates messages.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Request__Sequence__fini(motor_commands__srv__GetMotorStates_Request__Sequence * array);

/// Create array of srv/GetMotorStates messages.
/**
 * It allocates the memory for the array and calls
 * motor_commands__srv__GetMotorStates_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
motor_commands__srv__GetMotorStates_Request__Sequence *
motor_commands__srv__GetMotorStates_Request__Sequence__create(size_t size);

/// Destroy array of srv/GetMotorStates messages.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Request__Sequence__destroy(motor_commands__srv__GetMotorStates_Request__Sequence * array);

/// Check for srv/GetMotorStates message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Request__Sequence__are_equal(const motor_commands__srv__GetMotorStates_Request__Sequence * lhs, const motor_commands__srv__GetMotorStates_Request__Sequence * rhs);

/// Copy an array of srv/GetMotorStates messages.
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
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Request__Sequence__copy(
  const motor_commands__srv__GetMotorStates_Request__Sequence * input,
  motor_commands__srv__GetMotorStates_Request__Sequence * output);

/// Initialize srv/GetMotorStates message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * motor_commands__srv__GetMotorStates_Response
 * )) before or use
 * motor_commands__srv__GetMotorStates_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Response__init(motor_commands__srv__GetMotorStates_Response * msg);

/// Finalize srv/GetMotorStates message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Response__fini(motor_commands__srv__GetMotorStates_Response * msg);

/// Create srv/GetMotorStates message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * motor_commands__srv__GetMotorStates_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
motor_commands__srv__GetMotorStates_Response *
motor_commands__srv__GetMotorStates_Response__create(void);

/// Destroy srv/GetMotorStates message.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Response__destroy(motor_commands__srv__GetMotorStates_Response * msg);

/// Check for srv/GetMotorStates message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Response__are_equal(const motor_commands__srv__GetMotorStates_Response * lhs, const motor_commands__srv__GetMotorStates_Response * rhs);

/// Copy a srv/GetMotorStates message.
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
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Response__copy(
  const motor_commands__srv__GetMotorStates_Response * input,
  motor_commands__srv__GetMotorStates_Response * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates_Response__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/GetMotorStates messages.
/**
 * It allocates the memory for the number of elements and calls
 * motor_commands__srv__GetMotorStates_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Response__Sequence__init(motor_commands__srv__GetMotorStates_Response__Sequence * array, size_t size);

/// Finalize array of srv/GetMotorStates messages.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Response__Sequence__fini(motor_commands__srv__GetMotorStates_Response__Sequence * array);

/// Create array of srv/GetMotorStates messages.
/**
 * It allocates the memory for the array and calls
 * motor_commands__srv__GetMotorStates_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
motor_commands__srv__GetMotorStates_Response__Sequence *
motor_commands__srv__GetMotorStates_Response__Sequence__create(size_t size);

/// Destroy array of srv/GetMotorStates messages.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Response__Sequence__destroy(motor_commands__srv__GetMotorStates_Response__Sequence * array);

/// Check for srv/GetMotorStates message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Response__Sequence__are_equal(const motor_commands__srv__GetMotorStates_Response__Sequence * lhs, const motor_commands__srv__GetMotorStates_Response__Sequence * rhs);

/// Copy an array of srv/GetMotorStates messages.
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
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Response__Sequence__copy(
  const motor_commands__srv__GetMotorStates_Response__Sequence * input,
  motor_commands__srv__GetMotorStates_Response__Sequence * output);

/// Initialize srv/GetMotorStates message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * motor_commands__srv__GetMotorStates_Event
 * )) before or use
 * motor_commands__srv__GetMotorStates_Event__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Event__init(motor_commands__srv__GetMotorStates_Event * msg);

/// Finalize srv/GetMotorStates message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Event__fini(motor_commands__srv__GetMotorStates_Event * msg);

/// Create srv/GetMotorStates message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * motor_commands__srv__GetMotorStates_Event__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
motor_commands__srv__GetMotorStates_Event *
motor_commands__srv__GetMotorStates_Event__create(void);

/// Destroy srv/GetMotorStates message.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Event__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Event__destroy(motor_commands__srv__GetMotorStates_Event * msg);

/// Check for srv/GetMotorStates message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Event__are_equal(const motor_commands__srv__GetMotorStates_Event * lhs, const motor_commands__srv__GetMotorStates_Event * rhs);

/// Copy a srv/GetMotorStates message.
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
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Event__copy(
  const motor_commands__srv__GetMotorStates_Event * input,
  motor_commands__srv__GetMotorStates_Event * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_type_hash_t *
motor_commands__srv__GetMotorStates_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeDescription *
motor_commands__srv__GetMotorStates_Event__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource *
motor_commands__srv__GetMotorStates_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
const rosidl_runtime_c__type_description__TypeSource__Sequence *
motor_commands__srv__GetMotorStates_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/GetMotorStates messages.
/**
 * It allocates the memory for the number of elements and calls
 * motor_commands__srv__GetMotorStates_Event__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Event__Sequence__init(motor_commands__srv__GetMotorStates_Event__Sequence * array, size_t size);

/// Finalize array of srv/GetMotorStates messages.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Event__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Event__Sequence__fini(motor_commands__srv__GetMotorStates_Event__Sequence * array);

/// Create array of srv/GetMotorStates messages.
/**
 * It allocates the memory for the array and calls
 * motor_commands__srv__GetMotorStates_Event__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
motor_commands__srv__GetMotorStates_Event__Sequence *
motor_commands__srv__GetMotorStates_Event__Sequence__create(size_t size);

/// Destroy array of srv/GetMotorStates messages.
/**
 * It calls
 * motor_commands__srv__GetMotorStates_Event__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
void
motor_commands__srv__GetMotorStates_Event__Sequence__destroy(motor_commands__srv__GetMotorStates_Event__Sequence * array);

/// Check for srv/GetMotorStates message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Event__Sequence__are_equal(const motor_commands__srv__GetMotorStates_Event__Sequence * lhs, const motor_commands__srv__GetMotorStates_Event__Sequence * rhs);

/// Copy an array of srv/GetMotorStates messages.
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
ROSIDL_GENERATOR_C_PUBLIC_motor_commands
bool
motor_commands__srv__GetMotorStates_Event__Sequence__copy(
  const motor_commands__srv__GetMotorStates_Event__Sequence * input,
  motor_commands__srv__GetMotorStates_Event__Sequence * output);
#ifdef __cplusplus
}
#endif

#endif  // MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__FUNCTIONS_H_
