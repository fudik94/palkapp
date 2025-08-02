[app]
title = PalkApp
package.name = palkapp
package.domain = org.palkapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = tests, bin
version = 0.1
icon.filename = icons/palk_icon.png
orientation = portrait
requirements = python3,kivy,kivymd,matplotlib
source.main = main.py
android.entrypoint = org.kivy.android.PythonActivity
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = armeabi-v7a
android.debug = 1
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
