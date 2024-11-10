from setuptools import find_packages, setup

package_name = 'motor_controller'

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
                      'dynamixel_sdk'],
    zip_safe=True,
    maintainer='Ryo Isogawa',
    maintainer_email='2023m002@kuas.ac.jp',
    description='a package for controlling motors',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_controller = motor_controller:main'
        ],
    },
)
