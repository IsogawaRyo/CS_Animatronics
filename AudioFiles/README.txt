Dinosaur Robot Audio Files

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

Controller Audio Mapping:
- Cross (×) → Basic roar (ID 1)
- Circle (○) → Aggressive roar (ID 2) 
- Square (□) → Growl (ID 3)
- Triangle (△) → Hiss (ID 4)
- L1 → Chomp (ID 5)
- R1 → Footstep (ID 6)
- L2 → Ground shake (ID 7)
- R2 → Heavy breathing (ID 8)
- Options → Warning call (ID 9)
- PS (Recording start) → Hunt call (ID 10)
- L3 → Pain sound (ID 11)
- R3/PS (Recording end) → Victory roar (ID 12)

Auto-Playing Features:
- Jaw opening (>60%) : Randomly selects from available roar_X.wav files
- Breathing (5-10s intervals) : Randomly selects from available breath_X.wav files

Manual Usage:
- Play by ID: ros2 topic pub /play_audio_id std_msgs/msg/Int32 '{data: 1}'
- Play by name: ros2 topic pub /play_audio_name std_msgs/msg/String '{data: "roar_1.wav"}'
- Stop audio: ros2 topic pub /stop_audio std_msgs/msg/String '{data: ""}'
- Check status: ros2 topic echo /audio_status

Running the audio player:
ros2 run audio_player audio_player

Dependencies:
- pygame (for audio playback)
- Install with: pip install pygame