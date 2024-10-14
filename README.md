# Minieks dotfiles

This repository contains the fotfiles for my system

## Requirements
### Git
```
sudo pacman -S git
```

### Stow
```
sudo pacman -S Stow
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
