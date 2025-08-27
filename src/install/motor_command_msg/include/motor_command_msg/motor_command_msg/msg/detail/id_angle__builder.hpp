// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_command_msg/msg/id_angle.hpp"


#ifndef MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__BUILDER_HPP_
#define MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "motor_command_msg/msg/detail/id_angle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace motor_command_msg
{

namespace msg
{

namespace builder
{

class Init_IdAngle_angles
{
public:
  explicit Init_IdAngle_angles(::motor_command_msg::msg::IdAngle & msg)
  : msg_(msg)
  {}
  ::motor_command_msg::msg::IdAngle angles(::motor_command_msg::msg::IdAngle::_angles_type arg)
  {
    msg_.angles = std::move(arg);
    return std::move(msg_);
  }

private:
  ::motor_command_msg::msg::IdAngle msg_;
};

class Init_IdAngle_ids
{
public:
  Init_IdAngle_ids()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_IdAngle_angles ids(::motor_command_msg::msg::IdAngle::_ids_type arg)
  {
    msg_.ids = std::move(arg);
    return Init_IdAngle_angles(msg_);
  }

private:
  ::motor_command_msg::msg::IdAngle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::motor_command_msg::msg::IdAngle>()
{
  return motor_command_msg::msg::builder::Init_IdAngle_ids();
}

}  // namespace motor_command_msg

#endif  // MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__BUILDER_HPP_
