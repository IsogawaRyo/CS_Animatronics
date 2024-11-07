cmake_minimum_required(VERSION 3.5)
project(your_ros2_package)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Message files
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/IdAngleArray.msg"
)

# Include directories
include_directories(
  include
)

# Add the executable
add_executable(my_node src/my_node.cpp)
ament_target_dependencies(my_node rclcpp std_msgs)

# Install executable
install(TARGETS
  my_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

# Install message files
install(DIRECTORY
  msg
  DESTINATION share/${PROJECT_NAME}
)

# Ament package
ament_package()

