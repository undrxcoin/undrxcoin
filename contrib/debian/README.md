
Debian
====================
This directory contains files used to package skrtd/skrt-qt
for Debian-based Linux systems. If you compile skrtd/skrt-qt yourself, there are some useful files here.

## skrt: URI support ##


skrt-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install skrt-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your skrtqt binary to `/usr/bin`
and the `../../share/pixmaps/skrt128.png` to `/usr/share/pixmaps`

skrt-qt.protocol (KDE)

