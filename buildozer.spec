[app]
title = Anthobiz
package.name = anthobiz
package.domain = com.anthotech.anthobiz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.3.2
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
p4a.url = https://github.com/kivy/python-for-android.git
p4a.branch = master
android.accept_sdk_license_agreements = True
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.buildtools = 33.0.2
android.ant = auto
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.backup_rules = 
p4a.bootstrap = sdl2
