// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from motor_command_msg:msg/IdAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_command_msg/msg/id_angle.hpp"


#ifndef MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__TRAITS_HPP_
#define MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "motor_command_msg/msg/detail/id_angle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace motor_command_msg
{

namespace msg
{

inline void to_flow_style_yaml(
  const IdAngle & msg,
  std::ostream & out)
{
  out << "{";
  // member: ids
  {
    if (msg.ids.size() == 0) {
      out << "ids: []";
    } else {
      out << "ids: [";
      size_t pending_items = msg.ids.size();
      for (auto item : msg.ids) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: angles
  {
    if (msg.angles.size() == 0) {
      out << "angles: []";
    } else {
      out << "angles: [";
      size_t pending_items = msg.angles.size();
      for (auto item : msg.angles) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IdAngle & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.ids.size() == 0) {
      out << "ids: []\n";
    } else {
      out << "ids:\n";
      for (auto item : msg.ids) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: angles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.angles.size() == 0) {
      out << "angles: []\n";
    } else {
      out << "angles:\n";
      for (auto item : msg.angles) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IdAngle & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace motor_command_msg

namespace rosidl_generator_traits
{

[[deprecated("use motor_command_msg::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const motor_command_msg::msg::IdAngle & msg,
  std::ostream & out, size_t indentation = 0)
{
  motor_command_msg::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use motor_command_msg::msg::to_yaml() instead")]]
inline std::string to_yaml(const motor_command_msg::msg::IdAngle & msg)
{
  return motor_command_msg::msg::to_yaml(msg);
}

template<>
inline const char * data_type<motor_command_msg::msg::IdAngle>()
{
  return "motor_command_msg::msg::IdAngle";
}

template<>
inline const char * name<motor_command_msg::msg::IdAngle>()
{
  return "motor_command_msg/msg/IdAngle";
}

template<>
struct has_fixed_size<motor_command_msg::msg::IdAngle>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<motor_command_msg::msg::IdAngle>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<motor_command_msg::msg::IdAngle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MOTOR_COMMAND_MSG__MSG__DETAIL__ID_ANGLE__TRAITS_HPP_
