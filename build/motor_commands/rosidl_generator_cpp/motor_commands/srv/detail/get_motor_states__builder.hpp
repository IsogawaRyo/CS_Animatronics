// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_commands/srv/get_motor_states.hpp"


#ifndef MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__BUILDER_HPP_
#define MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "motor_commands/srv/detail/get_motor_states__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace motor_commands
{

namespace srv
{

namespace builder
{

class Init_GetMotorStates_Request_ids
{
public:
  Init_GetMotorStates_Request_ids()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::motor_commands::srv::GetMotorStates_Request ids(::motor_commands::srv::GetMotorStates_Request::_ids_type arg)
  {
    msg_.ids = std::move(arg);
    return std::move(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::motor_commands::srv::GetMotorStates_Request>()
{
  return motor_commands::srv::builder::Init_GetMotorStates_Request_ids();
}

}  // namespace motor_commands


namespace motor_commands
{

namespace srv
{

namespace builder
{

class Init_GetMotorStates_Response_system_total_current
{
public:
  explicit Init_GetMotorStates_Response_system_total_current(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  ::motor_commands::srv::GetMotorStates_Response system_total_current(::motor_commands::srv::GetMotorStates_Response::_system_total_current_type arg)
  {
    msg_.system_total_current = std::move(arg);
    return std::move(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_port1_total_current
{
public:
  explicit Init_GetMotorStates_Response_port1_total_current(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Response_system_total_current port1_total_current(::motor_commands::srv::GetMotorStates_Response::_port1_total_current_type arg)
  {
    msg_.port1_total_current = std::move(arg);
    return Init_GetMotorStates_Response_system_total_current(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_port0_total_current
{
public:
  explicit Init_GetMotorStates_Response_port0_total_current(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Response_port1_total_current port0_total_current(::motor_commands::srv::GetMotorStates_Response::_port0_total_current_type arg)
  {
    msg_.port0_total_current = std::move(arg);
    return Init_GetMotorStates_Response_port1_total_current(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_error_status
{
public:
  explicit Init_GetMotorStates_Response_error_status(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Response_port0_total_current error_status(::motor_commands::srv::GetMotorStates_Response::_error_status_type arg)
  {
    msg_.error_status = std::move(arg);
    return Init_GetMotorStates_Response_port0_total_current(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_torques
{
public:
  explicit Init_GetMotorStates_Response_torques(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Response_error_status torques(::motor_commands::srv::GetMotorStates_Response::_torques_type arg)
  {
    msg_.torques = std::move(arg);
    return Init_GetMotorStates_Response_error_status(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_temperatures
{
public:
  explicit Init_GetMotorStates_Response_temperatures(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Response_torques temperatures(::motor_commands::srv::GetMotorStates_Response::_temperatures_type arg)
  {
    msg_.temperatures = std::move(arg);
    return Init_GetMotorStates_Response_torques(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_positions
{
public:
  explicit Init_GetMotorStates_Response_positions(::motor_commands::srv::GetMotorStates_Response & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Response_temperatures positions(::motor_commands::srv::GetMotorStates_Response::_positions_type arg)
  {
    msg_.positions = std::move(arg);
    return Init_GetMotorStates_Response_temperatures(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

class Init_GetMotorStates_Response_ids
{
public:
  Init_GetMotorStates_Response_ids()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetMotorStates_Response_positions ids(::motor_commands::srv::GetMotorStates_Response::_ids_type arg)
  {
    msg_.ids = std::move(arg);
    return Init_GetMotorStates_Response_positions(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::motor_commands::srv::GetMotorStates_Response>()
{
  return motor_commands::srv::builder::Init_GetMotorStates_Response_ids();
}

}  // namespace motor_commands


namespace motor_commands
{

namespace srv
{

namespace builder
{

class Init_GetMotorStates_Event_response
{
public:
  explicit Init_GetMotorStates_Event_response(::motor_commands::srv::GetMotorStates_Event & msg)
  : msg_(msg)
  {}
  ::motor_commands::srv::GetMotorStates_Event response(::motor_commands::srv::GetMotorStates_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Event msg_;
};

class Init_GetMotorStates_Event_request
{
public:
  explicit Init_GetMotorStates_Event_request(::motor_commands::srv::GetMotorStates_Event & msg)
  : msg_(msg)
  {}
  Init_GetMotorStates_Event_response request(::motor_commands::srv::GetMotorStates_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GetMotorStates_Event_response(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Event msg_;
};

class Init_GetMotorStates_Event_info
{
public:
  Init_GetMotorStates_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetMotorStates_Event_request info(::motor_commands::srv::GetMotorStates_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GetMotorStates_Event_request(msg_);
  }

private:
  ::motor_commands::srv::GetMotorStates_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::motor_commands::srv::GetMotorStates_Event>()
{
  return motor_commands::srv::builder::Init_GetMotorStates_Event_info();
}

}  // namespace motor_commands

#endif  // MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__BUILDER_HPP_
