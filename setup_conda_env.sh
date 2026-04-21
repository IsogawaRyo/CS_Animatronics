#!/bin/bash
# ==============================================================================
# CS_Animatronics Conda Environment Setup Script
# ==============================================================================
# このスクリプトは、CS_Animatronicsプロジェクトで必要になる可能性がある
# Pythonパッケージ群をConda環境にまとめるためのテンプレートです。
# ROS 2パッケージ自体の実行には通常システムのPython環境を使用しますが、
# 機械学習(DeepLabCut)やシミュレータ(Genesis)等を動かす際に利用してください。

ENV_NAME="cs_animatronics_env"
PYTHON_VERSION="3.10"

echo "=== Conda環境 [${ENV_NAME}] を作成しています (Python ${PYTHON_VERSION}) ==="
conda create -n ${ENV_NAME} python=${PYTHON_VERSION} -y

echo "=== 環境を有効化してベースパッケージをインストールしています ==="
# スクリプト内でconda activateを機能させるためのおまじない
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ${ENV_NAME}

# [必須] PyTorch 等のインストール (環境に合わせて変更してください)
# conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

# [必須] Graphvizシステムバイナリのインストール (WireVizの画像出力に必要)
conda install -c conda-forge graphviz -y

# [必須] プロジェクトで利用するPythonモジュール群
pip install numpy pygame pyserial dynamixel_sdk wireviz
# ※ ROS 2のパッケージ(rclpy等)はConda環境と競合することがあるため、
# ROS 2コマンドを使用する端末ではCondaを一旦 `conda deactivate` してください。

echo ""
echo "=============================================================================="
echo "✅ セットアップが完了しました！"
echo "今後は以下のコマンドで仮想環境に入ることができます："
echo "conda activate ${ENV_NAME}"
echo "=============================================================================="
