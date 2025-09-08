#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import os
import json
import pygame
import threading
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32

class AudioPlayer(Node):
    def __init__(self):
        super().__init__('audio_player')
        self.get_logger().info('Initializing Dinosaur Robot Audio Player')
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Audio files directory
        self.audio_dir = "/home/csanimatronics/CS_Animatronics/AudioFiles"
        self.audio_map_file = "/home/csanimatronics/CS_Animatronics/AudioMap.json"
        
        # Audio mapping (ID -> file path)
        self.audio_map = {}
        self.load_audio_map()
        
        # Playback state
        self.is_playing = False
        self.current_sound = None
        
        # Create directories if they don't exist
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # ROS2 Subscribers
        self.play_audio_by_id_sub = self.create_subscription(
            Int32,
            'play_audio_id',
            self.play_audio_by_id_callback,
            10
        )
        
        self.play_audio_by_name_sub = self.create_subscription(
            String,
            'play_audio_name',
            self.play_audio_by_name_callback,
            10
        )
        
        self.stop_audio_sub = self.create_subscription(
            String,
            'stop_audio',
            self.stop_audio_callback,
            10
        )
        
        # ROS2 Publishers for status
        self.status_pub = self.create_publisher(
            String,
            'audio_status',
            10
        )
        
        # Preload dinosaur sounds
        self.create_default_audio_map()
        
        self.get_logger().info('Audio Player initialized successfully')
    
    def load_audio_map(self):
        """Load audio ID mapping from JSON file"""
        try:
            if os.path.exists(self.audio_map_file):
                with open(self.audio_map_file, 'r', encoding='utf-8') as f:
                    self.audio_map = json.load(f)
                self.get_logger().info(f"Loaded audio map with {len(self.audio_map)} entries")
            else:
                self.audio_map = {}
                self.get_logger().info("No audio map file found, creating new one")
        except Exception as e:
            self.get_logger().error(f"Error loading audio map: {e}")
            self.audio_map = {}
    
    def save_audio_map(self):
        """Save audio ID mapping to JSON file"""
        try:
            with open(self.audio_map_file, 'w', encoding='utf-8') as f:
                json.dump(self.audio_map, f, indent=4, ensure_ascii=False)
            self.get_logger().info("Audio map saved successfully")
        except Exception as e:
            self.get_logger().error(f"Error saving audio map: {e}")
    
    def create_default_audio_map(self):
        """Create default audio mapping for dinosaur sounds"""
        default_sounds = {
            "1": "roar_1.wav",        # Basic roar
            "2": "roar_2.wav",        # Aggressive roar
            "3": "growl.wav",         # Low growl
            "4": "hiss.wav",          # Hissing sound
            "5": "chomp.wav",         # Jaw chomping
            "6": "footstep_1.wav",    # Heavy footstep
            "7": "footstep_2.wav",    # Ground shake
            "8": "breath_1.wav",      # Heavy breathing (updated to breath_1)
            "9": "warning.wav",       # Warning call
            "10": "hunt.wav",         # Hunting call
            "11": "pain.wav",         # Pain/injury sound
            "12": "victory.wav",      # Victory roar
        }
        
        # Only add mappings for files that don't exist yet
        updated = False
        for sound_id, filename in default_sounds.items():
            if sound_id not in self.audio_map:
                self.audio_map[sound_id] = filename
                updated = True
        
        if updated:
            self.save_audio_map()
            self.get_logger().info("Created default dinosaur audio map")
    
    def play_audio_by_id_callback(self, msg):
        """Play audio file by ID"""
        audio_id = str(msg.data)
        self.get_logger().info(f"Received play audio ID request: {audio_id}")
        
        if audio_id in self.audio_map:
            filename = self.audio_map[audio_id]
            self.play_audio_file(filename, audio_id)
        else:
            self.get_logger().warn(f"Audio ID {audio_id} not found in audio map")
            self.publish_status(f"ERROR: Audio ID {audio_id} not found")
    
    def play_audio_by_name_callback(self, msg):
        """Play audio file by filename"""
        filename = msg.data
        self.get_logger().info(f"Received play audio name request: {filename}")
        self.play_audio_file(filename, "name")
    
    def stop_audio_callback(self, msg):
        """Stop currently playing audio"""
        self.get_logger().info("Received stop audio request")
        self.stop_audio()
    
    def play_audio_file(self, filename, identifier):
        """Play audio file with error handling"""
        try:
            # Stop current audio if playing
            if self.is_playing:
                self.stop_audio()
            
            # Construct full path
            if not filename.startswith('/'):
                filepath = os.path.join(self.audio_dir, filename)
            else:
                filepath = filename
            
            # Check if file exists
            if not os.path.exists(filepath):
                self.get_logger().error(f"Audio file not found: {filepath}")
                self.publish_status(f"ERROR: File not found - {filename}")
                return
            
            # Play audio in separate thread to avoid blocking
            thread = threading.Thread(
                target=self._play_audio_thread,
                args=(filepath, identifier, filename)
            )
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.get_logger().error(f"Error playing audio {filename}: {e}")
            self.publish_status(f"ERROR: {str(e)}")
    
    def _play_audio_thread(self, filepath, identifier, filename):
        """Audio playback thread"""
        try:
            self.get_logger().info(f"Starting playback: {filename}")
            self.is_playing = True
            self.publish_status(f"PLAYING: {filename}")
            
            # Load and play sound
            self.current_sound = pygame.mixer.Sound(filepath)
            channel = self.current_sound.play()
            
            # Wait for playback to complete
            while channel.get_busy() and self.is_playing:
                time.sleep(0.1)
            
            if self.is_playing:  # Normal completion
                self.get_logger().info(f"Finished playback: {filename}")
                self.publish_status(f"FINISHED: {filename}")
            else:  # Stopped manually
                self.get_logger().info(f"Stopped playback: {filename}")
                self.publish_status("STOPPED")
                
        except Exception as e:
            self.get_logger().error(f"Audio playback error: {e}")
            self.publish_status(f"ERROR: {str(e)}")
        finally:
            self.is_playing = False
            self.current_sound = None
    
    def stop_audio(self):
        """Stop currently playing audio"""
        if self.is_playing:
            self.is_playing = False
            pygame.mixer.stop()
            self.get_logger().info("Audio playback stopped")
            self.publish_status("STOPPED")
    
    def publish_status(self, status):
        """Publish audio player status"""
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)
    
    def list_available_sounds(self):
        """Log available sound files"""
        if os.path.exists(self.audio_dir):
            files = [f for f in os.listdir(self.audio_dir) 
                    if f.lower().endswith(('.wav', '.mp3', '.ogg'))]
            self.get_logger().info(f"Available audio files: {files}")
            
            self.get_logger().info("Audio ID mappings:")
            for audio_id, filename in self.audio_map.items():
                status = "✓" if os.path.exists(os.path.join(self.audio_dir, filename)) else "✗"
                self.get_logger().info(f"  ID {audio_id}: {filename} {status}")
    
    def create_sample_sounds_info(self):
        """Create information file about expected dinosaur sounds"""
        info_file = os.path.join(self.audio_dir, "README.txt")
        info_content = """Dinosaur Robot Audio Files

Place your audio files (.wav, .mp3, .ogg) in this directory.

Recommended dinosaur sounds (with multiple pattern support):
- roar_1.wav, roar_2.wav, roar_3.wav... : Territorial roars (auto jaw trigger)
- breath_1.wav, breath_2.wav, breath_3.wav... : Heavy breathing (auto background)
- growl.wav      : Low threatening growl
- hiss.wav       : Snake-like hiss
- chomp.wav      : Jaw snapping sound
- footstep_1.wav : Heavy footstep
- footstep_2.wav : Ground shaking step
- warning.wav    : Warning/alert call
- hunt.wav       : Hunting vocalization
- pain.wav       : Pain/injury sound
- victory.wav    : Victory roar

Auto-Playing Features:
- Jaw opening (>60%) : Randomly selects from available roar_X.wav files
- Breathing (5-10s intervals) : Randomly selects from available breath_X.wav files

Usage:
- Play by ID: ros2 topic pub /play_audio_id std_msgs/msg/Int32 '{data: 1}'
- Play by name: ros2 topic pub /play_audio_name std_msgs/msg/String '{data: "roar_1.wav"}'
- Stop audio: ros2 topic pub /stop_audio std_msgs/msg/String '{data: ""}'
- Check status: ros2 topic echo /audio_status
"""
        
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(info_content)
            self.get_logger().info(f"Created audio info file: {info_file}")
        except Exception as e:
            self.get_logger().error(f"Error creating info file: {e}")

def main(args=None):
    rclpy.init(args=args)
    
    try:
        audio_player = AudioPlayer()
        
        # Show available sounds on startup
        audio_player.list_available_sounds()
        audio_player.create_sample_sounds_info()
        
        rclpy.spin(audio_player)
        
    except KeyboardInterrupt:
        print("\nShutting down Audio Player...")
    except Exception as e:
        print(f"Error in audio player: {e}")
    finally:
        if 'audio_player' in locals():
            audio_player.stop_audio()
            audio_player.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()