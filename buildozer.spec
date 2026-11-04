[app]
title = Anthobiz
package.name = anthobiz
package.domain = com.antotech.anthobiz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.3.2
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license_agreements = True
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
