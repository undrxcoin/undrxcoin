
Debian
====================
This directory contains files used to package undxd/undx-qt
for Debian-based Linux systems. If you compile undxd/undx-qt yourself, there are some useful files here.

## undx: URI support ##


undx-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install undx-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your undxqt binary to `/usr/bin`
and the `../../share/pixmaps/undx128.png` to `/usr/share/pixmaps`

undx-qt.protocol (KDE)

