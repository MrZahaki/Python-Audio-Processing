Usage Examples
--------------


.. raw:: html

   <script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
   <script>
     kofiWidgetOverlay.draw('mrzahaki', {
       'type': 'floating-chat',
       'floating-chat.donateButton.text': 'Support me',
       'floating-chat.donateButton.background-color': '#2980b9',
       'floating-chat.donateButton.text-color': '#fff'
     });
   </script>


Audio Manipulation
^^^^^^^^^^^^^^^^^^

Time Domain Slicing
"""""""""""""""""""

You can easily slice audio files to play specific segments:

.. code-block:: python

    # Create an audio master instance
    su = sudio.Master()

    # Load the audio file 'baroon.mp3' into the system
    song = su.add('baroon.mp3')

    # Play a specific segment of the song from 12 seconds to 27.66 seconds
    su.echo(song[12: 27.66])

    # Play the song starting from 30 seconds to the end of the track
    su.echo(song[30:])

    # Play only the first 15 seconds of the song
    su.echo(song[:15])

    # Reverse play the song from 30 seconds to 15 seconds
    su.echo(song[30:15])


Audio Speed Manipulation
""""""""""""""""""""""""

.. code-block:: python

    import sudio

    su = sudio.Master()
    record = su.add('somewhere_only_we_know.mp3')

    # Increase playback speed by 1.2x for a specific slice (10 to 30 seconds)
    faster_slice = record[10:30:1.2]
    su.echo(faster_slice)

    # Decrease playback speed by 0.75x and play a subsection from 5 seconds of that slice
    slower_slice = record[20:40:0.75]
    su.echo(slower_slice[5:])

An AudioWrap object can be sliced using standard Python slice syntax `x[start: stop: speed_ratio]`, 
where `x` is the wrapped object(in this case record).

    - `speed_ratio` > 1 increases playback speed (reduces duration).
    - `speed_ratio` < 1 decreases playback speed (increases duration).
    - Default `speed_ratio` is 1.0 (original speed).
    - Speed adjustments preserve pitch.


Combining Audio Segments
""""""""""""""""""""""""

You can join multiple segments of audio:

- method 1:

.. code-block:: python

    su = sudio.Master()
    song = su.add('baroon.mp3')
    su.echo(song[12: 27.66, 90: 65: .8])

for time domain slicing use `[i: j: k, i(2): j(2): k(2), i(n): j(n): k(n)]` syntax, where:

  - `i` is the start time,
  - `j` is the stop time,
  - `k` is the `speed_ratio`, which adjusts the playback speed.

This selects `nXm` seconds with index times:

`i, i+1, ..., j`, `i(2), i(2)+1, ..., j(2)`, ..., `i(n), ..., j(n)` where `m = j - i` (`j > i`).

Note For `i < j`, `i` is the stop time and `j` is the start time, meaning audio data is read inversely.


- method 2:

.. code-block:: python

    baroon = su.add('baroon.mp3')
    asemoon = su.add('asemoon.ogg')
    result = baroon[12: 27.66].join(asemoon[65: 90])
    medley = baroon[10:20].join(asemoon[40:50], baroon[70:80])

The join() method merges segments from different audio files into a seamless stream. 
For example, a segment from baroon.mp3 is combined with one from asemoon.ogg. 
You can also join multiple segments from various files, like two from baroon.mp3 and one from asemoon.ogg, to create a medley. 
This is perfect for mashups or audio compilations by stitching together parts of different tracks.



Mixing Tracks
"""""""""""""

.. code-block:: python

    import sudio

    su = sudio.Master()

    # Add two audio files
    song1 = su.add('song1.mp3') 
    song2 = su.add('song2.flac') 

    # Add the two songs
    combined = song1[2:10] + song2[4:20]

    # Play the combined audio
    su.echo(combined)

    # Print durations
    print(f"Song1 duration: {song1.get_duration()} seconds")
    print(f"Song2 duration: {song2.get_duration()} seconds")
    print(f"Combined duration: {combined.get_duration()} seconds")
    print(f"Shifted duration: {shifted.get_duration()} seconds")


When adding two AudioWrap objects, the combined audio will be as long as the longer one, mixing overlapping parts. 


Audio Basic Effects
^^^^^^^^^^^^^^^^^^^

Gain Adjustment
"""""""""""""""

In Gain Adjustment, we modify the audio's gain (volume) using decibel (dB) units. 
You can adjust the gain either directly via multiplication or using the afx() method to apply gain dynamically within specific time ranges:

- Method 1: Direct Gain Adjustment (Multiplication)

.. code-block:: python

    su = sudio.Master()
    song = su.add('song.mp3')

    # Increase gain by 6 dB
    loud_segment = song[10:20] * 6

    # Decrease gain by 6 dB
    quiet_segment = song[30:40] * -6

    # Play the loud and quiet segments together
    su.echo(loud_segment.join(quiet_segment))

In this method, the * operator adjusts the gain by applying a dB value. 
The result is a segment with increased or decreased volume, represented in dB. 
The scale is converted from dB to amplitude using a formula, and soft clipping is applied to prevent distortion.

- Method 2: Applying Gain Using Effects (AFX)

.. code-block:: python

    import sudio
    from sudio.process.fx import Gain

    su = sudio.Master()
    song = su.add('somewhere_only_we_know.mp3')[10:20]

    # Apply dynamic gain adjustment from 2s to 5s in the segment
    song = song.afx(Gain, gain_db=-30, start=2, stop=5, wet_mix=0.9)

    su.echo(song)

In this approach, the afx() method applies a dynamic gain effect to a specific segment of the track. 
Here, gain is reduced by -30 dB from 2s to 5s. The wet_mix parameter determines how much of the effect is applied, where 1 means full effect and 0 means no effect. 
The gain_db is in dB units, allowing for precise control over volume adjustments.


Applying Filters
""""""""""""""""

Apply frequency filters to audio:

.. code-block:: python

    su = sudio.Master()
    song = su.add('song.mp3')

    # Apply a low-pass filter (keep frequencies below 1000 Hz)
    low_pass = song[:'1000']

    # Apply a high-pass filter (keep frequencies above 500 Hz)
    high_pass = song['500':]

    # Apply a band-pass filter (keep frequencies between 500 Hz and 2000 Hz)
    band_pass = song['500':'2000']
    
    # apply a 6th-order band-stop filter to the audio segment from 5 to 10 seconds
    # with a -0.8 dB attenuation, effectively suppresses this range
    band_stop = audio['200': '1000': 'order=6, scale=-.8']

    su.echo(low_pass.join(high_pass, band_pass, band_stop))

Use `['i': 'j': 'filtering options', 'i(2)': 'j(2)': 'options(2)', ..., 'i(n)': 'j(n)': 'options(n)']` syntax, where:
- `i` is the starting frequency,
- `j` is the stopping frequency (string type, in the same units as `fs`).

This activates `n` IIR filters with specified frequencies and options.

Slice Syntax for Filtering:

  - `x=None`, `y='j'`: Low-pass filter with a cutoff frequency of `j`.
  - `x='i'`, `y=None`: High-pass filter with a cutoff frequency of `i`.
  - `x='i'`, `y='j'`: Band-pass filter with critical frequencies `i`, `j`.
  - `x='i'`, `y='j'`, `options='scale=[negative value]'`: Band-stop filter with critical frequencies `i`, `j`.


Filtering Options:

  - `ftype` : str, optional
      Type of IIR filter to design. Options: `'butter'` (default), `'cheby1'`, `'cheby2'`, `'ellip'`, `'bessel'`.
  - `rs` : float, optional
      Minimum attenuation in the stop band (dB) for Chebyshev and elliptic filters.
  - `rp` : float, optional
      Maximum ripple in the passband (dB) for Chebyshev and elliptic filters.
  - `order` : int, optional
      The order of the filter. Default is 5.
  - `scale` : float or int, optional
      Attenuation or amplification factor. Must be negative for a band-stop filter.


Simple two-band EQ
""""""""""""""""""

.. code-block:: python

    import sudio

    su = sudio.Master()
    song = su.add('file.ogg')
    new_song = song[40:60, : '200': 'order=4, scale=.8', '200'::'scale=.5'] * 1.7
    su.echo(new_song)

Here, a two-band EQ tweaks specific frequencies within a 40-60 second audio slice. 
First, a 4th-order low-pass filter reduces everything below 200 Hz, scaled by 0.8 to lower low frequencies. 
Next, a 5th-order high-pass filter handles frequencies above 200 Hz, scaled by 0.5 to soften the highs. 
After filtering, the overall volume is boosted by 1.7db to balance loudness. 
Finally, the processed audio is played using master.echo(), revealing how these adjustments shape the 
sound—perfect for reducing noise or enhancing specific frequency ranges.


Low-Frequency Temporal Echo Manipulation
""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    import sudio

    su = sudio.Master()

    song = su.add('song.mp3') 
    combined = song[2:10] + song[2.2:10.2:.8, :'300']
    su.echo(combined)

This audio processing technique creates a unique effect by blending the original audio with a time-shifted, filtered version. 
It takes an 8-second slice (2 to 10 seconds), shifts it by 200 milliseconds (2.2 to 10.2 seconds), and applies a low-pass filter that retains only frequencies below 300 Hz. 
The shifted slice is played at 0.8x speed and combined with the original, producing a subtle echo-like texture that enhances low-frequency sounds. 
This approach is ideal for atmospheric sound design, adding depth to music, or creating dynamic audio transitions.


Custom Fade-In Effect
"""""""""""""""""""""

.. code-block:: python

    import sudio
    from sudio.types import SampleFormat
    import numpy as np

    su = sudio.Master()
    song = su.add('example.mp3')

    fade_length = int(song.get_sample_rate() * 5)  # 5-second fade
    fade_in = np.linspace(0, 1, fade_length)

    with song.unpack(astype=SampleFormat.FLOAT32, start=2, stop=20) as data:
        data[:, :fade_length] *= fade_in
        song.set_data(data)

    su.echo(song)
    su.export(song, 'modified_song.ogg')

The audio file example.mp3 is loaded into sudio.Master(), where a 5-second fade-in is applied using np.linspace to adjust the volume based on the sample rate. 
The unpack method  extracts audio between 2 and 20 seconds in FLOAT32 format for precise processing, with normalization handled via the astype parameter to prevent distortion.

After processing, the audio is repacked and saved as modified_song.ogg. 
The unpack method supports resetting (reset=True), format conversion (astype), time range selection (start/stop), and truncation (truncate=True), 
enabling precise audio manipulation without re-encoding, ensuring high performance and minimal data loss.


Advanced Effect Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `afx()` method provides a powerful way to apply audio effects dynamically to specific time ranges within an audio segment. It supports precise control over effect parameters, timing, and mix levels.

Gain Effect Dynamics
""""""""""""""""""""

Apply gain adjustments to specific segments with fine-grained control:

.. code-block:: python

    import sudio
    from sudio.process.fx import Gain

    su = sudio.Master()
    song = su.add('somewhere_only_we_know.mp3')[10:20]

    # Reduce volume by -30 dB from 2s to 5s within the segment
    song = song.afx(Gain, gain_db=-30, start=2, stop=5, wet_mix=0.9)
    su.echo(song)

Parameters for afx() method:

  - `start`: Beginning of effect application (in segment time)
  - `stop`: End of effect application (in segment time)
  - `wet_mix`: Effect intensity (0.0 to 1.0)
  
    - 0.0: No effect
    - 1.0: Full effect
    - Values between 0 and 1 allow blending

Tempo Time Stretching
"""""""""""""""""""""

Dynamically modify audio tempo:

.. code-block:: python

    import sudio
    from sudio.process.fx import Tempo

    su = sudio.Master()
    song = su.add('somewhere_only_we_know.mp3')[10:20]

    # Slow down segment to 0.8x speed 
    song = song.afx(Tempo, tempo=0.8, output_gain_db=1)
    su.echo(song)

Envelope Shaping with FadeEnvelope
""""""""""""""""""""""""""""""""""

Apply various envelope presets or create custom amplitude shapes. For more details and predefined presets, see the sudio.process submodule.

.. code-block:: python

    import sudio
    from sudio.process.fx import FadeEnvelope, FadePreset
    import numpy as np

    su = sudio.Master()
    song = su.add('./song.ogg')

    # Predefined Envelope Presets
    # Smooth fade at segment ends
    song = song.afx(FadeEnvelope, preset=FadePreset.SMOOTH_ENDS, output_gain_db=1)

    # Bell curve envelope
    song = song.afx(FadeEnvelope, preset=FadePreset.BELL_CURVE, start=10, stop=20)

    # Keep only the attack portion
    song = song.afx(FadeEnvelope, preset=FadePreset.KEEP_ATTACK_ONLY, 
            start=20, stop=30, input_gain_db=1)

    # Custom envelope with spline interpolation
    custom_envelope = np.array([0.0, 0.0, 0.1, 0.2, 0.3, 0.7, 0.1, 0.0])
    song = song.afx(FadeEnvelope, preset=custom_envelope, 
            start=30, stop=40, output_gain_db=1, 
            enable_spline=True)

    su.export(song, 'song.mp3')
    su.echo(song)

The SUDIO library's FadeEnvelope effect offers a powerful toolkit for audio envelope manipulation, enabling sound designers to precisely shape audio dynamics. 
By loading an audio file and applying various preset and custom envelope transformations, users can create nuanced sonic textures with ease. 
The example demonstrates multiple techniques, including smooth fades, bell curve envelopes, attack preservation, and custom amplitude shaping with spline interpolation. 
With fine-grained control over parameters like gain, time range, and interpolation methods, users can craft complex audio effects ranging from subtle amplitude adjustments to dramatic sound design. 


Audio Analysis
^^^^^^^^^^^^^^

Perform simple analysis on audio files:

.. code-block:: python

    su = sudio.Master()
    song = su.add('song.mp3')

    # Get audio duration
    duration = song.get_duration()
    print(f"Song duration: {duration} seconds")

    # Get sample rate
    sample_rate = song.get_sample_rate()
    print(f"Sample rate: {sample_rate} Hz")

    # Get number of channels
    channels = song.get_nchannels()
    print(f"Number of channels: {channels}")

This code demonstrates how to slice and play specific segments of an audio file using time-based indexing, similar to slicing lists in Python.


Audio Format Conversion and Encoding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's explore how sudio handles different audio formats. We'll convert between MP3, WAV, FLAC, and OGG, and throw in some audio tweaks along the way.

.. code-block:: python

    import sudio
    from sudio.types import FileFormat

    su = sudio.Master()

    # Load any audio file - MP3, WAV, OGG, or FLAC
    record = su.add('original_song.mp3')

    # Slice and save as WAV
    su.export(record[10.5: 30], 'cool_snippet.wav')

    # Quiet it down and save as high-quality FLAC
    su.export(record * -10.5, format=FileFormat.FLAC, quality=0.8)

    # Convert to medium-quality OGG
    su.export(record, 'medium_quality.ogg', quality=0.5)

    # Convert to medium-quality mp3
    su.export(record, 'medium_quality.mp3', quality=0.5, bitrate=64)

Pro tip: The second export creates a file named after the original, but with a .flac extension.

Remember, converting between lossy formats (like MP3 to OGG) might not sound great. For best results, start with high-quality or lossless files when possible.



Audio Streaming
^^^^^^^^^^^^^^^

Basic Streaming with Pause and Resume
"""""""""""""""""""""""""""""""""""""

This example demonstrates how to control audio playback using the sudio library, including starting, pausing, resuming, and stopping a stream.

.. code-block:: python

    import sudio
    import time

    # Initialize the audio master
    su = sudio.Master()
    su.start()

    # Add an audio file to the master
    record = su.add('example.mp3')
    stream = su.stream(record)

    # Enable stdout echo
    su.echo()

    # Start the audio stream
    stream.start()
    print(f"Current playback time: {stream.time} seconds")

    # Pause the playback after 5 seconds
    time.sleep(5)
    stream.pause()
    print("Paused playback")

    # Resume playback after 2 seconds
    time.sleep(2)
    stream.resume()
    print("Resumed playback")

    # Stop playback after 5 more seconds
    time.sleep(5)
    stream.stop()
    print("Stopped playback")

This script showcases basic audio control operations, allowing you to manage playback with precise timing.

Basic Streaming with Jumping to Specific Times in the Audio
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This example illustrates how to start playback and jump to a specific time in an audio file.

.. code-block:: python

    import sudio
    import time

    # Initialize the audio master
    su = sudio.Master()
    su.start()

    # Add a long audio file to the master
    record = su.add('long_audio.mp3')
    stream = su.stream(record)

    # Enable stdout echo
    su.echo()

    # Start the audio stream
    stream.start()
    print(f"Starting playback at: {stream.time} seconds")

    # Jump to 30 seconds into the audio after 5 seconds of playback
    time.sleep(5)
    stream.time = 30
    print(f"Jumped to: {stream.time} seconds")

    # Continue playback for 10 more seconds
    time.sleep(10)
    print(f"Current playback time: {stream.time} seconds")

    # Stop the audio stream
    stream.stop()

This script demonstrates how to navigate within an audio file, which is useful for long audio content or when specific sections need to be accessed quickly.

Streaming with Volume Control
"""""""""""""""""""""""""""""

This example shows how to dynamically control the volume of an audio stream using a custom pipeline.

.. code-block:: python

    import sudio
    import time
    import sudio.types

    # Initialize the audio master with a specific input device
    su = sudio.Master(std_input_dev_id=2)
    su.start()

    # Add an audio file to the master
    record = su.add('example.mp3')
    stream = su.stream(record)

    # Define a function to adjust the volume
    def adjust_volume(data, args):
        return data * args['volume']

    # Create a pipeline and append the volume adjustment function
    pip = sudio.Pipeline()
    pip.append(adjust_volume, args={'volume': 1.0})

    # Start the pipeline
    pip.start()

    # Add the pipeline to the master
    pipeline_id = su.add_pipeline(pip, process_type=sudio.types.PipelineProcessType.MAIN)
    su.set_pipeline(pipeline_id)

    # Enable stdout echo
    su.echo()

    # Start the audio stream
    stream.start()
    print("Playing at normal volume")
    time.sleep(10)

    # Adjust the volume to 50%
    pip.update_args(adjust_volume, {'volume': 0.5})
    print("Reduced volume to 50%")
    time.sleep(10)

    # Restore the volume to normal
    pip.update_args(adjust_volume, {'volume': 1.0})
    print("Restored normal volume")
    time.sleep(10)

    # Stop the audio stream
    stream.stop()

This example introduces a more complex setup using a custom pipeline to dynamically adjust the audio volume during playback. It's particularly useful for applications requiring real-time audio processing or user-controlled volume adjustments.
