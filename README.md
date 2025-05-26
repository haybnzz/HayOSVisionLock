# HayOSVisionLock


![HayOSVisionLock Logo](https://raw.githubusercontent.com/haybnzz/HayOSVisionLock/refs/heads/main/hayOS%20VISIONLock.png)

[![CC BY-NC 4.0 License](https://img.shields.io/static/v1?label=License&message=CC%20BY-NC%204.0&style=for-the-badge&logo=creative-commons&logoSize=auto&labelColor=4B4453&color=FFD166)](https://github.com/haybnzz/HayOSVisionLock/blob/main/LICENSE) [![GitHub Issues](https://img.shields.io/github/issues/haybnzz/HayOSVisionLock?style=for-the-badge&logo=github&logoSize=auto&labelColor=4B4453&color=073B4C)](https://github.com/haybnzz/HayOSVisionLock/issues) [![GitHub Stars](https://img.shields.io/github/stars/haybnzz/HayOSVisionLock?style=for-the-badge&logo=github&logoSize=auto&labelColor=4B4453&color=EF476F)](https://github.com/haybnzz/HayOSVisionLock/stargazers) ![Profile Views](https://komarev.com/ghpvc/?username=haybnzz&style=for-the-badge&logo=github&logoSize=auto&labelColor=4B4453&color=FFD166) [![Website](https://img.shields.io/static/v1?label=Website&message=Hay.Bnz&style=for-the-badge&logo=data:image/png;base64,...&logoSize=auto&labelColor=4B4453&color=EF233C)](https://haybnz.glitch.me/) [![Paper](https://img.shields.io/static/v1?label=Paper&message=GitHub&style=for-the-badge&logo=github&logoSize=auto&labelColor=4B4453&color=FFD700)](https://github.com/haybnzz/HayOSVisionLock/blob/main/paper.md) [![Python](https://img.shields.io/static/v1?label=Language&message=Python&style=for-the-badge&logo=python&logoColor=FFD43B&labelColor=4B4453&color=306998)](https://www.python.org/) [![OpenCV](https://img.shields.io/static/v1?label=Library&message=OpenCV&style=for-the-badge&logo=opencv&logoColor=white&labelColor=4B4453&color=5C2DD5)](https://opencv.org/) [![Face Recognition](https://img.shields.io/static/v1?label=Module&message=Face%20Recognition&style=for-the-badge&logo=ai&logoColor=white&labelColor=4B4453&color=118AB2)](https://github.com/ageitgey/face_recognition)

>"HayOSVisionLock" 🔒 Secure your PC with **HayOSVisionLock**! 🖼️ Powered by `face_recognition` and OpenCV (`cv2`), this tool uses your webcam to detect faces and locks your Windows PC if an unknown face is detected. 🚨 It sends Discord notifications with images of unrecognized faces and allows secure face registration with password verification. 🔑.


## Overview

HayOSVisionLock is a CNN-based tool designed for secure and accurate image classification, supporting various visual analysis tasks. The model leverages a convolutional neural network architecture built with TensorFlow and Keras to deliver robust performance.

## 🔍 Features

- Secure and automated image classification
- Support for multiple visual analysis categories
- User-friendly web interface for image upload and analysis
- High-accuracy classification using convolutional neural networks

## 📋 Table of Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [License](#-license)
- [Support](#-support)
- [Contributors](#-contributors-and-developers)

## 🔧 Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Steps

1. Clone the repository:
`git clone https://github.com/haybnzz/HayOSVisionLock/
cd HayOSVisionLock
pip install -r requirements.txt
python HayOSVisionLock.py`

## 📌 Usage

### ▶️ Running the Application

- Ensure your **webcam** is connected.
- Place images of authorized faces in the `known_faces` folder.
- Run the application — the webcam feed will open and start detecting faces.

#### 🔑 Controls

- Press **`r`** to register a new face (requires system password).
- Press **`q`** to quit the application.

#### 🔒 Lock Behavior

- If an **unknown face** is detected **or** no known face is seen for **10 seconds (default timeout)**:
  - The **PC will automatically lock**.
  - A **Discord notification** will be sent with the captured unknown face image.

---

## 📁 Project Structure

`
HayOSVisionLock/
├── known_faces/              # Folder for storing authorized face images
├── HayOSVisionLock.py         # Main application script
├── requirements.txt
└── README.md
`

## ⚙️ Configuration

Edit the following variables in `face_lock.py` to customize behavior:

- **`KNOWN_FACES_DIR`**: Directory for authorized face images (default: `known_faces`)
- **`DISCORD_WEBHOOK_URL`**: Your Discord webhook URL for notifications
- **`TOLERANCE`**: Face recognition tolerance (default: `0.6`, lower is stricter)
- **`LOCK_TIMEOUT`**: Seconds before locking if no known face is detected (default: `10`)
- **`CHECK_INTERVAL`**: Seconds between face checks (default: `1`)

## 📄 License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) License.  
See the [LICENSE](https://github.com/haybnzz/HayOSVisionLock/blob/main/LICENSE) file for more details.  
**Unauthorized use is strictly prohibited.**



## 📧 Contact

**Email**: `singularat@protn.me`



## 💸 Support

**Donate via Monero**:
`45PU6txuLxtFFcVP95qT2xXdg7eZzPsqFfbtZp5HTjLbPquDAugBKNSh1bJ76qmAWNGMBCKk4R1UCYqXxYwYfP2wTggZNhq`



## 👨‍💻 Contributors and Developers

<img src="https://avatars.githubusercontent.com/u/67865621?s=64&v=4" width="64" height="64" alt="haybnzz">  
<img src="https://avatars.githubusercontent.com/u/144106684?s=64&v=4" width="64" height="64" alt="Glitchesminds">



## 📚 Citation

If you use **HayOSVisionLock** in your research, please cite:

```bibtex
@misc{HayOSVisionLock2025,
  author       = {Hayden Banz and Glitchesminds},
  title        = {HayOSVisionLock: Face Recognition Based System Lock with Discord Alerts},
  year         = {2025},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/haybnzz/HayOSVisionLock}},
}




