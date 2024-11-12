// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_command_msg/msg/id_angle.hpp"


#ifndef MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__STRUCT_HPP_
#define MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__motor_command_msg__msg__IdAngle __attribute__((deprecated))
#else
# define DEPRECATED__motor_command_msg__msg__IdAngle __declspec(deprecated)
#endif

namespace motor_command_msg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct IdAngle_
{
  using Type = IdAngle_<ContainerAllocator>;

  explicit IdAngle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<uint8_t, 76800>::iterator, uint8_t>(this->ids.begin(), this->ids.end(), 0);
      std::fill<typename std::array<int32_t, 76800>::iterator, int32_t>(this->angles.begin(), this->angles.end(), 0l);
    }
  }

  explicit IdAngle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : ids(_alloc),
    angles(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<uint8_t, 76800>::iterator, uint8_t>(this->ids.begin(), this->ids.end(), 0);
      std::fill<typename std::array<int32_t, 76800>::iterator, int32_t>(this->angles.begin(), this->angles.end(), 0l);
    }
  }

  // field types and members
  using _ids_type =
    std::array<uint8_t, 76800>;
  _ids_type ids;
  using _angles_type =
    std::array<int32_t, 76800>;
  _angles_type angles;

  // setters for named parameter idiom
  Type & set__ids(
    const std::array<uint8_t, 76800> & _arg)
  {
    this->ids = _arg;
    return *this;
  }
  Type & set__angles(
    const std::array<int32_t, 76800> & _arg)
  {
    this->angles = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    motor_command_msg::msg::IdAngle_<ContainerAllocator> *;
  using ConstRawPtr =
    const motor_command_msg::msg::IdAngle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      motor_command_msg::msg::IdAngle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      motor_command_msg::msg::IdAngle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__motor_command_msg__msg__IdAngle
    std::shared_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__motor_command_msg__msg__IdAngle
    std::shared_ptr<motor_command_msg::msg::IdAngle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const IdAngle_ & other) const
  {
    if (this->ids != other.ids) {
      return false;
    }
    if (this->angles != other.angles) {
      return false;
    }
    return true;
  }
  bool operator!=(const IdAngle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct IdAngle_

// alias to use template instance with default allocator
using IdAngle =
  motor_command_msg::msg::IdAngle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace motor_command_msg

#endif  // MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__STRUCT_HPP_
