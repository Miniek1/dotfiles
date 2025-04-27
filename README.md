[!NOTE]  
> I haven't updated this for a while. I'm planning on redoing most of it lol.

# Minieks dotfiles

### This repository contains the dotfiles for my system
![Picture of desktop](https://github.com/Miniek1/dotfiles/blob/main/desktop.png?raw=true)


## Requirements
### dependencies
```
sudo pacman -S git stow pipewire libgtop bluez bluez-utils btop networkmanager dart-sass wl-clipboard brightnessctl swww python gnome-bluetooth-3.0 pacman-contrib power-profiles-daemon gvfs
```
```
yay -S grimblast-git gpu-screen-recorder hyprpicker matugen-bin python-gpustat hyprsunset-git
```

## Installation
First, clone the repo into your $HOME directory using git.
```
git clone https://github.com/Miniek1/dotfiles.git
cd dotfiles
```

Then use stow to crete the symlinks
```
stow .
```

### HyprPanel config
## Starting HyprPanel
Make sure to install AGSv1 using the included MAKEPKG
```
cd ags
makepkgs -si
```

now you can launch the panel with:
```
hyprctl dispatch exec agsv1 
```

## Edit the config file
Edit these lines accordingly to your location, make sure to put your own API key from [weatherapi.com](https://www.weatherapi.com)
```
"menus.clock.weather.location": "",
"menus.clock.weather.unit": "metric",
"menus.clock.weather.key": "",
```

Finally, import the config file in the HyprPanel settings.
