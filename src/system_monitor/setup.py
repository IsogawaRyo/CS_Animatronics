from setuptools import setup

package_name = 'system_monitor'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ryo Isogawa',
    maintainer_email='isogawaryou@todo.todo',
    description='System monitor GUI for Animatronics',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'system_monitor = system_monitor.system_monitor_node:main'
        ],
    },
)
