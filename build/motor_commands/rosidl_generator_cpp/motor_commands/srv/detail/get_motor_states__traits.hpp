// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from motor_commands:srv/GetMotorStates.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "motor_commands/srv/get_motor_states.hpp"


#ifndef MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__TRAITS_HPP_
#define MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "motor_commands/srv/detail/get_motor_states__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace motor_commands
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetMotorStates_Request & msg,
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
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetMotorStates_Request & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetMotorStates_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_generator_traits
{

[[deprecated("use motor_commands::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const motor_commands::srv::GetMotorStates_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  motor_commands::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use motor_commands::srv::to_yaml() instead")]]
inline std::string to_yaml(const motor_commands::srv::GetMotorStates_Request & msg)
{
  return motor_commands::srv::to_yaml(msg);
}

template<>
inline const char * data_type<motor_commands::srv::GetMotorStates_Request>()
{
  return "motor_commands::srv::GetMotorStates_Request";
}

template<>
inline const char * name<motor_commands::srv::GetMotorStates_Request>()
{
  return "motor_commands/srv/GetMotorStates_Request";
}

template<>
struct has_fixed_size<motor_commands::srv::GetMotorStates_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<motor_commands::srv::GetMotorStates_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<motor_commands::srv::GetMotorStates_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace motor_commands
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetMotorStates_Response & msg,
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

  // member: positions
  {
    if (msg.positions.size() == 0) {
      out << "positions: []";
    } else {
      out << "positions: [";
      size_t pending_items = msg.positions.size();
      for (auto item : msg.positions) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: temperatures
  {
    if (msg.temperatures.size() == 0) {
      out << "temperatures: []";
    } else {
      out << "temperatures: [";
      size_t pending_items = msg.temperatures.size();
      for (auto item : msg.temperatures) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: torques
  {
    if (msg.torques.size() == 0) {
      out << "torques: []";
    } else {
      out << "torques: [";
      size_t pending_items = msg.torques.size();
      for (auto item : msg.torques) {
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
  const GetMotorStates_Response & msg,
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

  // member: positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.positions.size() == 0) {
      out << "positions: []\n";
    } else {
      out << "positions:\n";
      for (auto item : msg.positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: temperatures
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.temperatures.size() == 0) {
      out << "temperatures: []\n";
    } else {
      out << "temperatures:\n";
      for (auto item : msg.temperatures) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: torques
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.torques.size() == 0) {
      out << "torques: []\n";
    } else {
      out << "torques:\n";
      for (auto item : msg.torques) {
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

inline std::string to_yaml(const GetMotorStates_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_generator_traits
{

[[deprecated("use motor_commands::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const motor_commands::srv::GetMotorStates_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  motor_commands::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use motor_commands::srv::to_yaml() instead")]]
inline std::string to_yaml(const motor_commands::srv::GetMotorStates_Response & msg)
{
  return motor_commands::srv::to_yaml(msg);
}

template<>
inline const char * data_type<motor_commands::srv::GetMotorStates_Response>()
{
  return "motor_commands::srv::GetMotorStates_Response";
}

template<>
inline const char * name<motor_commands::srv::GetMotorStates_Response>()
{
  return "motor_commands/srv/GetMotorStates_Response";
}

template<>
struct has_fixed_size<motor_commands::srv::GetMotorStates_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<motor_commands::srv::GetMotorStates_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<motor_commands::srv::GetMotorStates_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace motor_commands
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetMotorStates_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
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
  const GetMotorStates_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetMotorStates_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace motor_commands

namespace rosidl_generator_traits
{

[[deprecated("use motor_commands::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const motor_commands::srv::GetMotorStates_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  motor_commands::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use motor_commands::srv::to_yaml() instead")]]
inline std::string to_yaml(const motor_commands::srv::GetMotorStates_Event & msg)
{
  return motor_commands::srv::to_yaml(msg);
}

template<>
inline const char * data_type<motor_commands::srv::GetMotorStates_Event>()
{
  return "motor_commands::srv::GetMotorStates_Event";
}

template<>
inline const char * name<motor_commands::srv::GetMotorStates_Event>()
{
  return "motor_commands/srv/GetMotorStates_Event";
}

template<>
struct has_fixed_size<motor_commands::srv::GetMotorStates_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<motor_commands::srv::GetMotorStates_Event>
  : std::integral_constant<bool, has_bounded_size<motor_commands::srv::GetMotorStates_Request>::value && has_bounded_size<motor_commands::srv::GetMotorStates_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<motor_commands::srv::GetMotorStates_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<motor_commands::srv::GetMotorStates>()
{
  return "motor_commands::srv::GetMotorStates";
}

template<>
inline const char * name<motor_commands::srv::GetMotorStates>()
{
  return "motor_commands/srv/GetMotorStates";
}

template<>
struct has_fixed_size<motor_commands::srv::GetMotorStates>
  : std::integral_constant<
    bool,
    has_fixed_size<motor_commands::srv::GetMotorStates_Request>::value &&
    has_fixed_size<motor_commands::srv::GetMotorStates_Response>::value
  >
{
};

template<>
struct has_bounded_size<motor_commands::srv::GetMotorStates>
  : std::integral_constant<
    bool,
    has_bounded_size<motor_commands::srv::GetMotorStates_Request>::value &&
    has_bounded_size<motor_commands::srv::GetMotorStates_Response>::value
  >
{
};

template<>
struct is_service<motor_commands::srv::GetMotorStates>
  : std::true_type
{
};

template<>
struct is_service_request<motor_commands::srv::GetMotorStates_Request>
  : std::true_type
{
};

template<>
struct is_service_response<motor_commands::srv::GetMotorStates_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MOTOR_COMMANDS__SRV__DETAIL__GET_MOTOR_STATES__TRAITS_HPP_
