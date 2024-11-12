// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice
#include "motor_command_msg/msg/detail/id_angle__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `ids`
// Member `angles`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
motor_command_msg__msg__IdAngle__init(motor_command_msg__msg__IdAngle * msg)
{
  if (!msg) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->ids, 0)) {
    motor_command_msg__msg__IdAngle__fini(msg);
    return false;
  }
  // angles
  if (!rosidl_runtime_c__double__Sequence__init(&msg->angles, 0)) {
    motor_command_msg__msg__IdAngle__fini(msg);
    return false;
  }
  return true;
}

void
motor_command_msg__msg__IdAngle__fini(motor_command_msg__msg__IdAngle * msg)
{
  if (!msg) {
    return;
  }
  // ids
  rosidl_runtime_c__int32__Sequence__fini(&msg->ids);
  // angles
  rosidl_runtime_c__double__Sequence__fini(&msg->angles);
}

bool
motor_command_msg__msg__IdAngle__are_equal(const motor_command_msg__msg__IdAngle * lhs, const motor_command_msg__msg__IdAngle * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->ids), &(rhs->ids)))
  {
    return false;
  }
  // angles
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->angles), &(rhs->angles)))
  {
    return false;
  }
  return true;
}

bool
motor_command_msg__msg__IdAngle__copy(
  const motor_command_msg__msg__IdAngle * input,
  motor_command_msg__msg__IdAngle * output)
{
  if (!input || !output) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->ids), &(output->ids)))
  {
    return false;
  }
  // angles
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->angles), &(output->angles)))
  {
    return false;
  }
  return true;
}

motor_command_msg__msg__IdAngle *
motor_command_msg__msg__IdAngle__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_command_msg__msg__IdAngle * msg = (motor_command_msg__msg__IdAngle *)allocator.allocate(sizeof(motor_command_msg__msg__IdAngle), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(motor_command_msg__msg__IdAngle));
  bool success = motor_command_msg__msg__IdAngle__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
motor_command_msg__msg__IdAngle__destroy(motor_command_msg__msg__IdAngle * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    motor_command_msg__msg__IdAngle__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
motor_command_msg__msg__IdAngle__Sequence__init(motor_command_msg__msg__IdAngle__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_command_msg__msg__IdAngle * data = NULL;

  if (size) {
    data = (motor_command_msg__msg__IdAngle *)allocator.zero_allocate(size, sizeof(motor_command_msg__msg__IdAngle), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = motor_command_msg__msg__IdAngle__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        motor_command_msg__msg__IdAngle__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
motor_command_msg__msg__IdAngle__Sequence__fini(motor_command_msg__msg__IdAngle__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      motor_command_msg__msg__IdAngle__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

motor_command_msg__msg__IdAngle__Sequence *
motor_command_msg__msg__IdAngle__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_command_msg__msg__IdAngle__Sequence * array = (motor_command_msg__msg__IdAngle__Sequence *)allocator.allocate(sizeof(motor_command_msg__msg__IdAngle__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = motor_command_msg__msg__IdAngle__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
motor_command_msg__msg__IdAngle__Sequence__destroy(motor_command_msg__msg__IdAngle__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    motor_command_msg__msg__IdAngle__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
motor_command_msg__msg__IdAngle__Sequence__are_equal(const motor_command_msg__msg__IdAngle__Sequence * lhs, const motor_command_msg__msg__IdAngle__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!motor_command_msg__msg__IdAngle__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
motor_command_msg__msg__IdAngle__Sequence__copy(
  const motor_command_msg__msg__IdAngle__Sequence * input,
  motor_command_msg__msg__IdAngle__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(motor_command_msg__msg__IdAngle);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    motor_command_msg__msg__IdAngle * data =
      (motor_command_msg__msg__IdAngle *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!motor_command_msg__msg__IdAngle__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          motor_command_msg__msg__IdAngle__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!motor_command_msg__msg__IdAngle__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
