################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 3.5)
project(dynamixel_sdk_examples)

## Compile as C++11
add_compile_options(-std=c++11)

################################################################################
# Find ament packages and libraries for ament and system dependencies
################################################################################
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(dynamixel_sdk REQUIRED)

# ROS2のメッセージ生成用
find_package(rosidl_default_generators REQUIRED)

################################################################################
# Declare ROS messages, services and actions
################################################################################
## Generate messages in the 'msg' folder
set(msg_files
  "msg/SetPosition.msg"
  "msg/SyncSetPosition.msg"
  "msg/BulkSetItem.msg"
)

## Generate services in the 'srv' folder
set(srv_files
  "srv/GetPosition.srv"
  "srv/SyncGetPosition.srv"
  "srv/BulkGetItem.srv"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES std_msgs
)

################################################################################
# Build
################################################################################
## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  ${rclcpp_INCLUDE_DIRS}
  ${dynamixel_sdk_INCLUDE_DIRS}
)

add_executable(read_write_node src/read_write_node.cpp)
ament_target_dependencies(read_write_node rclcpp std_msgs dynamixel_sdk)
target_link_libraries(read_write_node ${dynamixel_sdk_LIBRARIES})

add_executable(sync_read_write_node src/sync_read_write_node.cpp)
ament_target_dependencies(sync_read_write_node rclcpp std_msgs dynamixel_sdk)
target_link_libraries(sync_read_write_node ${dynamixel_sdk_LIBRARIES})

add_executable(bulk_read_write_node src/bulk_read_write_node.cpp)
ament_target_dependencies(bulk_read_write_node rclcpp std_msgs dynamixel_sdk)
target_link_libraries(bulk_read_write_node ${dynamixel_sdk_LIBRARIES})

add_executable(indirect_address_node src/indirect_address_node.cpp)
ament_target_dependencies(indirect_address_node rclcpp std_msgs dynamixel_sdk)
target_link_libraries(indirect_address_node ${dynamixel_sdk_LIBRARIES})

################################################################################
# Install
################################################################################
install(TARGETS
  read_write_node
  sync_read_write_node
  bulk_read_write_node
  indirect_address_node
  DESTINATION lib/${PROJECT_NAME}
)

################################################################################
# Export package
################################################################################
ament_export_dependencies(rclcpp std_msgs dynamixel_sdk)
ament_package()
