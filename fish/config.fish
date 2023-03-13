if status is-interactive
    # Commands to run in interactive sessions can go here
set fish_greeting ""

alias grub-config="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias reboot="sudo reboot now --no-wall"
alias shutdown="sudo shutdown now --no-wall"
alias :q="exit"

starship init fish | source
end
