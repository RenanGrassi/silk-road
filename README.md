# silk-road
Repositório para nosso sistema distribuído da disciplina.

## Erros comuns, e como resolver
```sh
silk-road-client  | This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
silk-road-client  | 
silk-road-client  | Available platform plugins are: offscreen, minimalegl, wayland-egl, wayland, linuxfb, vkkhrdisplay, minimal, eglfs, xcb, vnc.
```
Para resolver esse, precisa apenas de conceder permissão ao docker, com:
```sh
xhost +local:docker
```