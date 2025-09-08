// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_commands/srv/get_motor_states.hpp"


#ifndef MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__STRUCT_HPP_
#define MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__motor_commands__srv__GetMotorStates_Request __attribute__((deprecated))
#else
# define DEPRECATED__motor_commands__srv__GetMotorStates_Request __declspec(deprecated)
#endif

namespace motor_commands
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetMotorStates_Request_
{
  using Type = GetMotorStates_Request_<ContainerAllocator>;

  explicit GetMotorStates_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit GetMotorStates_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _ids_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _ids_type ids;

  // setters for named parameter idiom
  Type & set__ids(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->ids = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    motor_commands::srv::GetMotorStates_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const motor_commands::srv::GetMotorStates_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__motor_commands__srv__GetMotorStates_Request
    std::shared_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__motor_commands__srv__GetMotorStates_Request
    std::shared_ptr<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetMotorStates_Request_ & other) const
  {
    if (this->ids != other.ids) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetMotorStates_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetMotorStates_Request_

// alias to use template instance with default allocator
using GetMotorStates_Request =
  motor_commands::srv::GetMotorStates_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace motor_commands


#ifndef _WIN32
# define DEPRECATED__motor_commands__srv__GetMotorStates_Response __attribute__((deprecated))
#else
# define DEPRECATED__motor_commands__srv__GetMotorStates_Response __declspec(deprecated)
#endif

namespace motor_commands
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetMotorStates_Response_
{
  using Type = GetMotorStates_Response_<ContainerAllocator>;

  explicit GetMotorStates_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->port0_total_current = 0l;
      this->port1_total_current = 0l;
      this->system_total_current = 0l;
    }
  }

  explicit GetMotorStates_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->port0_total_current = 0l;
      this->port1_total_current = 0l;
      this->system_total_current = 0l;
    }
  }

  // field types and members
  using _ids_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _ids_type ids;
  using _positions_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _positions_type positions;
  using _temperatures_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _temperatures_type temperatures;
  using _torques_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _torques_type torques;
  using _error_status_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _error_status_type error_status;
  using _port0_total_current_type =
    int32_t;
  _port0_total_current_type port0_total_current;
  using _port1_total_current_type =
    int32_t;
  _port1_total_current_type port1_total_current;
  using _system_total_current_type =
    int32_t;
  _system_total_current_type system_total_current;

  // setters for named parameter idiom
  Type & set__ids(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->ids = _arg;
    return *this;
  }
  Type & set__positions(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->positions = _arg;
    return *this;
  }
  Type & set__temperatures(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->temperatures = _arg;
    return *this;
  }
  Type & set__torques(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->torques = _arg;
    return *this;
  }
  Type & set__error_status(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->error_status = _arg;
    return *this;
  }
  Type & set__port0_total_current(
    const int32_t & _arg)
  {
    this->port0_total_current = _arg;
    return *this;
  }
  Type & set__port1_total_current(
    const int32_t & _arg)
  {
    this->port1_total_current = _arg;
    return *this;
  }
  Type & set__system_total_current(
    const int32_t & _arg)
  {
    this->system_total_current = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    motor_commands::srv::GetMotorStates_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const motor_commands::srv::GetMotorStates_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__motor_commands__srv__GetMotorStates_Response
    std::shared_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__motor_commands__srv__GetMotorStates_Response
    std::shared_ptr<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetMotorStates_Response_ & other) const
  {
    if (this->ids != other.ids) {
      return false;
    }
    if (this->positions != other.positions) {
      return false;
    }
    if (this->temperatures != other.temperatures) {
      return false;
    }
    if (this->torques != other.torques) {
      return false;
    }
    if (this->error_status != other.error_status) {
      return false;
    }
    if (this->port0_total_current != other.port0_total_current) {
      return false;
    }
    if (this->port1_total_current != other.port1_total_current) {
      return false;
    }
    if (this->system_total_current != other.system_total_current) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetMotorStates_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetMotorStates_Response_

// alias to use template instance with default allocator
using GetMotorStates_Response =
  motor_commands::srv::GetMotorStates_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace motor_commands


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__motor_commands__srv__GetMotorStates_Event __attribute__((deprecated))
#else
# define DEPRECATED__motor_commands__srv__GetMotorStates_Event __declspec(deprecated)
#endif

namespace motor_commands
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetMotorStates_Event_
{
  using Type = GetMotorStates_Event_<ContainerAllocator>;

  explicit GetMotorStates_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit GetMotorStates_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<motor_commands::srv::GetMotorStates_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<motor_commands::srv::GetMotorStates_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    motor_commands::srv::GetMotorStates_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const motor_commands::srv::GetMotorStates_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      motor_commands::srv::GetMotorStates_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      motor_commands::srv::GetMotorStates_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__motor_commands__srv__GetMotorStates_Event
    std::shared_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__motor_commands__srv__GetMotorStates_Event
    std::shared_ptr<motor_commands::srv::GetMotorStates_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetMotorStates_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetMotorStates_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetMotorStates_Event_

// alias to use template instance with default allocator
using GetMotorStates_Event =
  motor_commands::srv::GetMotorStates_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace motor_commands

namespace motor_commands
{

namespace srv
{

struct GetMotorStates
{
  using Request = motor_commands::srv::GetMotorStates_Request;
  using Response = motor_commands::srv::GetMotorStates_Response;
  using Event = motor_commands::srv::GetMotorStates_Event;
};

}  // namespace srv

}  // namespace motor_commands

#endif  // MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__STRUCT_HPP_
