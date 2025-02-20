from setuptools import find_packages, setup

package_name = 'motion_editor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools',
                     'rclpy',
                     'motor_command_msg',],
    zip_safe=True,
    maintainer='csanimatronics',
    maintainer_email='2023m002@kuas.ac.jp',
    description='package for motion editor',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motion_editor = motion_editor.motion_editor:main',
            'system_controller = system_controller.system_controller:main',
        ],
    },
)
