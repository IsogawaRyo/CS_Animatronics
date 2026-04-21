from setuptools import find_packages, setup

package_name = 'audio_player'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ryo Isogawa',
    maintainer_email='ryo@example.com',
    description='Audio player node for dinosaur robot',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'audio_player = audio_player.audio_player:main',
        ],
    },
)