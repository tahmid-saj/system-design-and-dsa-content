# Video streaming

## Encoding

- Encoding involves compressing the raw video into a more manageable format via compression so that it is easier to stream. Encoding may sometimes be lossy, meaning that some of the original video data is lost

## Transcoding
  
- Transcoding involves taking an already compressed or encoded video and converting it to		multiple formats, resolutions or bitrates so that it is compatible with different devices.			Transcoding involves decompressing and compressing the video in different formats,			resolutions or bitrates. Transcoding is used to adapt the video to different network qualities		and devices.

## Video codec

- A video codec is an algorithm which compresses and decompresses video, making it more efficient for storage and transmission. Codec stands for “encoder and decoder”. Codecs will reduce the size of the video while preserving quality. Codecs may have the below trade-offs:
  - Time required to compress a file
  - Codec support on different machines
  - Compression efficiency
  - Compression quality - if it is lossy or lossless

- Some popular codecs include: H.264, H.265 (HEVC), VP9, AC1, MPEG-2, MPEG-4

## Video container

- A video container is a file format / space that stores video data (frames, audio, etc), and metadata. A video container may store info like video transcripts as well. Codecs determine how a video is compressed / decompressed, whereas a video container is a file format for how the video is actually stored. Supported video containers varies by devices / OS. The video container could have file extensions like mp4, avi, mov etc

## Bitrate
  
- Bitrate is the number of bits transmitted over a period of time (usually in kbps / mbps). The video size and video quality affects the bitrate. High resolution videos with higher framerates (measured in FPS) have much higher bitrates than low resolution videos at lower framerates. This is because there’s more video data to transfer. Compression via codecs may also affect the bitrate, since more efficient compression algorithms can lead to much less video data that needs to be transferred.

## Manifest files

Manifest files are text based files that give details about video streams. There’s usually 2 types of manifest files:

- Primary manifest files:
  - A primary manifest file lists all the available versions and formats of a video. The primary is the “root” file and points to all the media manifest files
- Media manifest files:
  - Media manifest files each represent a different version or format of the video. A video version or format will be split into small segments of a few seconds. Media manifest files list out the links to these segment files, and will be used by video players to stream the video by serving as an “index” to these segment files

## Video format
  
- A video format will usually represent both the video codec and video container being used

## Streaming protocols

- Streaming protocols are a standardized way to control data transfer for video streaming

- Popular streaming protocols are:
  - MEGA-DASH
  - Apple HLS (HTTP Live Streaming)
  - Microsoft Smooth Streaming
  - Adobe HTTP Dynamic Streaming (HDS)

