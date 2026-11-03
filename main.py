name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          pip install --upgrade pip
          pip install buildozer cython==0.29.33 kivy==2.3.0
      - name: Install Aidl
        run: |
          export ANDROID_HOME=/usr/local/lib/android/sdk
          echo "y" | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
          $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --install "build-tools;33.0.2" "platform-tools"
      - name: Build APK
        run: |
          mkdir -p $HOME/.buildozer/android/platform/android-sdk/tools/bin
          mkdir -p $HOME/.buildozer/android/platform/android-sdk/build-tools
          ln -sf /usr/local/lib/android/sdk/cmdline-tools $HOME/.buildozer/android/platform/android-sdk/cmdline-tools || true
          cp -r /usr/local/lib/android/sdk/build-tools/* $HOME/.buildozer/android/platform/android-sdk/build-tools/ || true
          cp -r /usr/local/lib/android/sdk/platform-tools $HOME/.buildozer/android/platform/android-sdk/ || true
          buildozer android debug
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Anthobiz-APK
          path: bin/*.apk
