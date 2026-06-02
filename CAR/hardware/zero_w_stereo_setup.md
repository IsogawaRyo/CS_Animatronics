# Raspberry Pi Zero W (Stereo Camera) Setup Guide

このドキュメントは、ステレオビジョン（複眼）用として2台の初代Raspberry Pi Zero WをUSB Ethernetカメラ化するためのセットアップ手順です。

## 1. SDカードの事前設定 (USB Gadget Mode)
Raspberry Pi Imager等でOSを書き込んだ直後のSDカード内にあるファイルを編集します。

### 両方のZero共通: `config.txt`
ファイルの末尾に以下の1行を追加します。
```text
dtoverlay=dwc2
```

### MACアドレスの固定化: `cmdline.txt`
ファイル内の `rootwait` の後に、1行に続けて以下を追記します。
（PC側で別々のUSBデバイスとして認識させるため、左右で異なるMACアドレスを指定します）

**左目用 (Zero 1) の追記内容:**
```text
modules-load=dwc2,g_ether g_ether.host_addr=12:34:56:78:9a:bc g_ether.dev_addr=12:34:56:78:9a:bd
```

**右目用 (Zero 2) の追記内容:**
```text
modules-load=dwc2,g_ether g_ether.host_addr=22:34:56:78:9a:bc g_ether.dev_addr=22:34:56:78:9a:bd
```

## 2. 固定IPの設定
Zeroが起動したら、SSH等でログインして固定IPを設定します。
`/etc/dhcpcd.conf` の末尾に以下を追記します。
*(※最新のRaspberry Pi OS Bookwormの場合はNetworkManagerを使っているため、`nmcli` コマンドで `usb0` のIPを固定してください)*

**左目用 (Zero 1):**
```text
interface usb0
static ip_address=10.55.0.2/24
```

**右目用 (Zero 2):**
```text
interface usb0
static ip_address=10.55.1.2/24
```
※メインのPC側（Mac/Linux）では、接続されたUSBネットワークインターフェースに対してそれぞれ `10.55.0.1` と `10.55.1.1` を割り当ててください。

## 3. カメラストリーミングの自動実行
Zero側の負荷を最小化するため、生映像をMJPEG形式でTCP配信します。

**左目用 (ポート 5000):**
```bash
libcamera-vid -t 0 --inline --codec mjpeg --width 640 --height 480 --framerate 30 --listen -o tcp://0.0.0.0:5000
```

**右目用 (ポート 5001):**
```bash
libcamera-vid -t 0 --inline --codec mjpeg --width 640 --height 480 --framerate 30 --listen -o tcp://0.0.0.0:5001
```

上記コマンドを `/etc/systemd/system/camera-stream.service` などのSystemdサービスとして登録し、OS起動時に自動実行されるように構成してください。
