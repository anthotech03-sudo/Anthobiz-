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
          
      - name: Accept licenses and install build-tools
        run: |
          mkdir -p $HOME/.android
          touch $HOME/.android/repositories.cfg
          export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
          export ANDROID_SDK_ROOT=$HOME/.buildozer/android/platform/android-sdk
          yes | sdkmanager --licenses || true
          # Buildozer will create SDK dir, so pre-create and install build-tools there
          mkdir -p $ANDROID_HOME/cmdline-tools
          cd /tmp
          wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline.zip
          unzip -q cmdline.zip
          mkdir -p $ANDROID_HOME/cmdline-tools/latest
          mv cmdline-tools/* $ANDROID_HOME/cmdline-tools/latest/ || mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest/ 2>/dev/null || true
          export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
          sdkmanager --install "build-tools;33.0.2" "platform-tools" || true

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Anthobiz-APK
          path: bin/*.apk
