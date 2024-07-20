<p align="center"><img src="data/icons/org.cristoto.Quimera.svg" width="256" height="256" alt=""></p>

<h1 align="center">Quimera</h1>
<p align="center">Generate Fake Data.</p>

# Quimera

Quimera is a powerful tool designed to generate high-quality fake data, perfect for testing, prototyping, and simulations. Ideal for developers, data scientists, and AI professionals needing to populate databases with fictional data to test application functionality or perform preliminary analyses.

## Main Features

- **Fake Data Generation**: Creates fictitious data for fields including names, emails, phone numbers, addresses, and more.
- **Data Exportation**: Exports generated data in several popular formats, including CSV, JSON, XML, and SQL.
- **Intuitive User Interface**: Designed with GTK4 and Adwaita for a smooth and modern user experience.
- **Cross-Platform Compatibility**: Works on Linux, Windows, and macOS, ensuring you can work on any operating system.


## Building

### Meson

Use this to build the application outside of a Flatpak image. Note that this method should
only be used by power users, to package the application on build scripts for rolling-release
distributions, or for development purposes.

Currently, to build the application you'll have to make sure that the required
libraries are installed on your system.

* glib >= 2.72
* gtk >= 4.14
* gtksourceview >= 5.4
* libadwaita >= 1.5

Make sure that you have Meson in your system. For instance,

```sh
sudo apt install meson
sudo dnf install meson
sudo pacman -S meson
```

Then use the following commands to build and install the application

```sh
meson setup build
ninja -C build
ninja -C build install
```

To avoid installing system-wide the application, you can use a prefix:

```sh
meson setup build --prefix=/usr
ninja -C build
ninja -C build install
```

## Contribution

We are committed to quality and inclusion in our project. If you're interested in contributing, please consult our contribution guide and adhere to our principles of conduct.

## License

Quimera is licensed under the GNU General Public License v3.0 or later.

## Credits and Acknowledgements

Quimera is maintained by Cristo. Many thanks to all contributors and users for their support and feedback.

## Blog

Follow the development of Quimera on the [cristoto.dev](https://www.cristoto.dev/blog).
