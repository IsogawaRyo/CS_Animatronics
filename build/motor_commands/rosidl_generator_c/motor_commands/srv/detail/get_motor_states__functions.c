// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice
#include "motor_commands/srv/detail/get_motor_states__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `ids`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
motor_commands__srv__GetMotorStates_Request__init(motor_commands__srv__GetMotorStates_Request * msg)
{
  if (!msg) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->ids, 0)) {
    motor_commands__srv__GetMotorStates_Request__fini(msg);
    return false;
  }
  return true;
}

void
motor_commands__srv__GetMotorStates_Request__fini(motor_commands__srv__GetMotorStates_Request * msg)
{
  if (!msg) {
    return;
  }
  // ids
  rosidl_runtime_c__uint8__Sequence__fini(&msg->ids);
}

bool
motor_commands__srv__GetMotorStates_Request__are_equal(const motor_commands__srv__GetMotorStates_Request * lhs, const motor_commands__srv__GetMotorStates_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->ids), &(rhs->ids)))
  {
    return false;
  }
  return true;
}

bool
motor_commands__srv__GetMotorStates_Request__copy(
  const motor_commands__srv__GetMotorStates_Request * input,
  motor_commands__srv__GetMotorStates_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->ids), &(output->ids)))
  {
    return false;
  }
  return true;
}

motor_commands__srv__GetMotorStates_Request *
motor_commands__srv__GetMotorStates_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Request * msg = (motor_commands__srv__GetMotorStates_Request *)allocator.allocate(sizeof(motor_commands__srv__GetMotorStates_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(motor_commands__srv__GetMotorStates_Request));
  bool success = motor_commands__srv__GetMotorStates_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
motor_commands__srv__GetMotorStates_Request__destroy(motor_commands__srv__GetMotorStates_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    motor_commands__srv__GetMotorStates_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
motor_commands__srv__GetMotorStates_Request__Sequence__init(motor_commands__srv__GetMotorStates_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Request * data = NULL;

  if (size) {
    data = (motor_commands__srv__GetMotorStates_Request *)allocator.zero_allocate(size, sizeof(motor_commands__srv__GetMotorStates_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = motor_commands__srv__GetMotorStates_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        motor_commands__srv__GetMotorStates_Request__fini(&data[i - 1]);
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
motor_commands__srv__GetMotorStates_Request__Sequence__fini(motor_commands__srv__GetMotorStates_Request__Sequence * array)
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
      motor_commands__srv__GetMotorStates_Request__fini(&array->data[i]);
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

motor_commands__srv__GetMotorStates_Request__Sequence *
motor_commands__srv__GetMotorStates_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Request__Sequence * array = (motor_commands__srv__GetMotorStates_Request__Sequence *)allocator.allocate(sizeof(motor_commands__srv__GetMotorStates_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = motor_commands__srv__GetMotorStates_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
motor_commands__srv__GetMotorStates_Request__Sequence__destroy(motor_commands__srv__GetMotorStates_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    motor_commands__srv__GetMotorStates_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
motor_commands__srv__GetMotorStates_Request__Sequence__are_equal(const motor_commands__srv__GetMotorStates_Request__Sequence * lhs, const motor_commands__srv__GetMotorStates_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!motor_commands__srv__GetMotorStates_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
motor_commands__srv__GetMotorStates_Request__Sequence__copy(
  const motor_commands__srv__GetMotorStates_Request__Sequence * input,
  motor_commands__srv__GetMotorStates_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(motor_commands__srv__GetMotorStates_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    motor_commands__srv__GetMotorStates_Request * data =
      (motor_commands__srv__GetMotorStates_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!motor_commands__srv__GetMotorStates_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          motor_commands__srv__GetMotorStates_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!motor_commands__srv__GetMotorStates_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `ids`
// Member `positions`
// Member `temperatures`
// Member `torques`
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `error_status`
#include "rosidl_runtime_c/string_functions.h"

bool
motor_commands__srv__GetMotorStates_Response__init(motor_commands__srv__GetMotorStates_Response * msg)
{
  if (!msg) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->ids, 0)) {
    motor_commands__srv__GetMotorStates_Response__fini(msg);
    return false;
  }
  // positions
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->positions, 0)) {
    motor_commands__srv__GetMotorStates_Response__fini(msg);
    return false;
  }
  // temperatures
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->temperatures, 0)) {
    motor_commands__srv__GetMotorStates_Response__fini(msg);
    return false;
  }
  // torques
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->torques, 0)) {
    motor_commands__srv__GetMotorStates_Response__fini(msg);
    return false;
  }
  // error_status
  if (!rosidl_runtime_c__String__Sequence__init(&msg->error_status, 0)) {
    motor_commands__srv__GetMotorStates_Response__fini(msg);
    return false;
  }
  // port0_total_current
  // port1_total_current
  // system_total_current
  return true;
}

void
motor_commands__srv__GetMotorStates_Response__fini(motor_commands__srv__GetMotorStates_Response * msg)
{
  if (!msg) {
    return;
  }
  // ids
  rosidl_runtime_c__uint8__Sequence__fini(&msg->ids);
  // positions
  rosidl_runtime_c__int32__Sequence__fini(&msg->positions);
  // temperatures
  rosidl_runtime_c__int32__Sequence__fini(&msg->temperatures);
  // torques
  rosidl_runtime_c__int32__Sequence__fini(&msg->torques);
  // error_status
  rosidl_runtime_c__String__Sequence__fini(&msg->error_status);
  // port0_total_current
  // port1_total_current
  // system_total_current
}

bool
motor_commands__srv__GetMotorStates_Response__are_equal(const motor_commands__srv__GetMotorStates_Response * lhs, const motor_commands__srv__GetMotorStates_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->ids), &(rhs->ids)))
  {
    return false;
  }
  // positions
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->positions), &(rhs->positions)))
  {
    return false;
  }
  // temperatures
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->temperatures), &(rhs->temperatures)))
  {
    return false;
  }
  // torques
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->torques), &(rhs->torques)))
  {
    return false;
  }
  // error_status
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->error_status), &(rhs->error_status)))
  {
    return false;
  }
  // port0_total_current
  if (lhs->port0_total_current != rhs->port0_total_current) {
    return false;
  }
  // port1_total_current
  if (lhs->port1_total_current != rhs->port1_total_current) {
    return false;
  }
  // system_total_current
  if (lhs->system_total_current != rhs->system_total_current) {
    return false;
  }
  return true;
}

bool
motor_commands__srv__GetMotorStates_Response__copy(
  const motor_commands__srv__GetMotorStates_Response * input,
  motor_commands__srv__GetMotorStates_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // ids
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->ids), &(output->ids)))
  {
    return false;
  }
  // positions
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->positions), &(output->positions)))
  {
    return false;
  }
  // temperatures
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->temperatures), &(output->temperatures)))
  {
    return false;
  }
  // torques
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->torques), &(output->torques)))
  {
    return false;
  }
  // error_status
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->error_status), &(output->error_status)))
  {
    return false;
  }
  // port0_total_current
  output->port0_total_current = input->port0_total_current;
  // port1_total_current
  output->port1_total_current = input->port1_total_current;
  // system_total_current
  output->system_total_current = input->system_total_current;
  return true;
}

motor_commands__srv__GetMotorStates_Response *
motor_commands__srv__GetMotorStates_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Response * msg = (motor_commands__srv__GetMotorStates_Response *)allocator.allocate(sizeof(motor_commands__srv__GetMotorStates_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(motor_commands__srv__GetMotorStates_Response));
  bool success = motor_commands__srv__GetMotorStates_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
motor_commands__srv__GetMotorStates_Response__destroy(motor_commands__srv__GetMotorStates_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    motor_commands__srv__GetMotorStates_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
motor_commands__srv__GetMotorStates_Response__Sequence__init(motor_commands__srv__GetMotorStates_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Response * data = NULL;

  if (size) {
    data = (motor_commands__srv__GetMotorStates_Response *)allocator.zero_allocate(size, sizeof(motor_commands__srv__GetMotorStates_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = motor_commands__srv__GetMotorStates_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        motor_commands__srv__GetMotorStates_Response__fini(&data[i - 1]);
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
motor_commands__srv__GetMotorStates_Response__Sequence__fini(motor_commands__srv__GetMotorStates_Response__Sequence * array)
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
      motor_commands__srv__GetMotorStates_Response__fini(&array->data[i]);
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

motor_commands__srv__GetMotorStates_Response__Sequence *
motor_commands__srv__GetMotorStates_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Response__Sequence * array = (motor_commands__srv__GetMotorStates_Response__Sequence *)allocator.allocate(sizeof(motor_commands__srv__GetMotorStates_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = motor_commands__srv__GetMotorStates_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
motor_commands__srv__GetMotorStates_Response__Sequence__destroy(motor_commands__srv__GetMotorStates_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    motor_commands__srv__GetMotorStates_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
motor_commands__srv__GetMotorStates_Response__Sequence__are_equal(const motor_commands__srv__GetMotorStates_Response__Sequence * lhs, const motor_commands__srv__GetMotorStates_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!motor_commands__srv__GetMotorStates_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
motor_commands__srv__GetMotorStates_Response__Sequence__copy(
  const motor_commands__srv__GetMotorStates_Response__Sequence * input,
  motor_commands__srv__GetMotorStates_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(motor_commands__srv__GetMotorStates_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    motor_commands__srv__GetMotorStates_Response * data =
      (motor_commands__srv__GetMotorStates_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!motor_commands__srv__GetMotorStates_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          motor_commands__srv__GetMotorStates_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!motor_commands__srv__GetMotorStates_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "motor_commands/srv/detail/get_motor_states__functions.h"

bool
motor_commands__srv__GetMotorStates_Event__init(motor_commands__srv__GetMotorStates_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    motor_commands__srv__GetMotorStates_Event__fini(msg);
    return false;
  }
  // request
  if (!motor_commands__srv__GetMotorStates_Request__Sequence__init(&msg->request, 0)) {
    motor_commands__srv__GetMotorStates_Event__fini(msg);
    return false;
  }
  // response
  if (!motor_commands__srv__GetMotorStates_Response__Sequence__init(&msg->response, 0)) {
    motor_commands__srv__GetMotorStates_Event__fini(msg);
    return false;
  }
  return true;
}

void
motor_commands__srv__GetMotorStates_Event__fini(motor_commands__srv__GetMotorStates_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  motor_commands__srv__GetMotorStates_Request__Sequence__fini(&msg->request);
  // response
  motor_commands__srv__GetMotorStates_Response__Sequence__fini(&msg->response);
}

bool
motor_commands__srv__GetMotorStates_Event__are_equal(const motor_commands__srv__GetMotorStates_Event * lhs, const motor_commands__srv__GetMotorStates_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!motor_commands__srv__GetMotorStates_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!motor_commands__srv__GetMotorStates_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
motor_commands__srv__GetMotorStates_Event__copy(
  const motor_commands__srv__GetMotorStates_Event * input,
  motor_commands__srv__GetMotorStates_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!motor_commands__srv__GetMotorStates_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!motor_commands__srv__GetMotorStates_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

motor_commands__srv__GetMotorStates_Event *
motor_commands__srv__GetMotorStates_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Event * msg = (motor_commands__srv__GetMotorStates_Event *)allocator.allocate(sizeof(motor_commands__srv__GetMotorStates_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(motor_commands__srv__GetMotorStates_Event));
  bool success = motor_commands__srv__GetMotorStates_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
motor_commands__srv__GetMotorStates_Event__destroy(motor_commands__srv__GetMotorStates_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    motor_commands__srv__GetMotorStates_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
motor_commands__srv__GetMotorStates_Event__Sequence__init(motor_commands__srv__GetMotorStates_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Event * data = NULL;

  if (size) {
    data = (motor_commands__srv__GetMotorStates_Event *)allocator.zero_allocate(size, sizeof(motor_commands__srv__GetMotorStates_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = motor_commands__srv__GetMotorStates_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        motor_commands__srv__GetMotorStates_Event__fini(&data[i - 1]);
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
motor_commands__srv__GetMotorStates_Event__Sequence__fini(motor_commands__srv__GetMotorStates_Event__Sequence * array)
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
      motor_commands__srv__GetMotorStates_Event__fini(&array->data[i]);
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

motor_commands__srv__GetMotorStates_Event__Sequence *
motor_commands__srv__GetMotorStates_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  motor_commands__srv__GetMotorStates_Event__Sequence * array = (motor_commands__srv__GetMotorStates_Event__Sequence *)allocator.allocate(sizeof(motor_commands__srv__GetMotorStates_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = motor_commands__srv__GetMotorStates_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
motor_commands__srv__GetMotorStates_Event__Sequence__destroy(motor_commands__srv__GetMotorStates_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    motor_commands__srv__GetMotorStates_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
motor_commands__srv__GetMotorStates_Event__Sequence__are_equal(const motor_commands__srv__GetMotorStates_Event__Sequence * lhs, const motor_commands__srv__GetMotorStates_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!motor_commands__srv__GetMotorStates_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
motor_commands__srv__GetMotorStates_Event__Sequence__copy(
  const motor_commands__srv__GetMotorStates_Event__Sequence * input,
  motor_commands__srv__GetMotorStates_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(motor_commands__srv__GetMotorStates_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    motor_commands__srv__GetMotorStates_Event * data =
      (motor_commands__srv__GetMotorStates_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!motor_commands__srv__GetMotorStates_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          motor_commands__srv__GetMotorStates_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!motor_commands__srv__GetMotorStates_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
