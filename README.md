# Minieks dotfiles

This repository contains the fotfiles for my system
![Picture of desktop](https://raw.githubusercontent.com/Miniek1/dotfiles/refs/heads/main/desktop.png?token=GHSAT0AAAAAACY6JCDJWK3VMKN76GJV7UVMZYNP66A)


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
