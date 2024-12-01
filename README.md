<div align="center">
    <picture style="pointer-events: none; user-select: none;">
        <img src="https://raw.githubusercontent.com/mrzahaki/sudio/Master/docs/_static/sudio.png" alt="sudio" width="60%" height="60%">
    </picture>
</div>


# Sudio 🎵

[![PyPI version](https://badge.fury.io/py/sudio.svg)](https://badge.fury.io/py/sudio)
[![PyPI Downloads](https://static.pepy.tech/badge/sudio)](https://www.pepy.tech/projects/sudio)
[![Documentation Status](https://readthedocs.org/projects/sudio/badge/?version=latest)](https://sudio.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://github.com/mrzahaki/sudio/actions/workflows/python-package.yml/badge.svg)](https://github.com/mrzahaki/sudio/actions/workflows/python-package.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/sudio.svg)](https://pypi.org/project/sudio/)
[![Supported OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Windows-blue)](https://shields.io/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mrzahaki/sudio/blob/Master/docs/_static/sudio.ipynb)  


Sudio is a Python library for audio processing and manipulation, providing set of tools for working with digital audio files. It supports operations like time-domain slicing, frequency filtering, audio mixing, streaming, and effect application across various audio formats, making complex audio engineering tasks accessible through a streamlined, Pythonic interface.


## 🚀 Quick Start

### Installation

Install Sudio using pip:

```bash
pip install sudio --upgrade
```

### Basic Usage

Here's an example to get you started with sudio:

```python
import sudio
from sudio.process.fx import FadeEnvelope, FadePreset

# Initialize Sudio Master
su = sudio.Master()

# Load an audio file
song = su.add('track.ogg')

# Slice, mix, and transform audio with ease
remix = song[10: 30]  + song[10.15: 25: .95, :'300'] * -10
remix = remix.afx(FadeEnvelope, preset=FadePreset.LINEAR_FADE_IN)

# Play and export the transformed audio
su.echo(remix)
su.export(remix, 'remix.mp3')
```

 the original 20-second segment (10-30 seconds) is layered with a slightly time-shifted slice, filtered to low frequencies below 300 Hz, with .95 original speed, and dramatically attenuated by -10 dB to create a subtle, atmospheric undertone. The LINEAR_FADE_IN envelope effect adds a gradual volume increase, creating a smooth, building intensity to the remix. 


### Explore Sudio

Get started with `Sudio` processing in minutes using [Google Colab](https://colab.research.google.com/github/mrzahaki/sudio/blob/Master/docs/_static/sudio.ipynb)!


## 🎹 Key Features
- Handles both real-time streaming and offline processing, allowing for dynamic applications like live audio effects as well as batch processing of audio files.
- Allows integration of custom processing modules.
- Flexible audio playback, precise time-domain slicing, and Comprehensive filtering options
- Advanced audio manipulation (joining, mixing, shifting)
- Real-time audio streaming with dynamic control (pause, resume, jump)
- Custom audio processing pipelines for complex effects
- Multi-format support with quality-controlled encoding/decoding


## 📚 Documentation

For detailed documentation and examples, visit the [Sudio Documentation](https://mrzahaki.github.io/sudio/).


## 💖 Support Sudio

I don't need your support. The link below is fake! Don't click on it, and don't pay anything. I mean it, just ignore it!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/mrzahaki)

## 📄 License

Sudio is released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3. See the [LICENSE](https://github.com/mrzahaki/sudio/blob/Master/LICENSE) file for details.
