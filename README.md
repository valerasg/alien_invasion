# Alien Invasion - Sergio Edition 🚀

Este proyecto es una versión extendida y mejorada del juego clásico "Alien Invasion", basado originalmente en el libro "Python Crash Course" de Eric Matthes. Esta edición añade múltiples mecánicas modernas, mejoras visuales y una experiencia de juego más dinámica.

![Alien Invasion Start Screen](/startscreen.png)

## Créditos Originales 📜
Gran parte del código base proviene de la excelente obra de **Eric Matthes, "Python Crash Course"**. Agradecimiento especial por proporcionar los cimientos de este proyecto.

## Nuevas Funcionalidades 👽

Esta versión ("Sergio Edition") incluye cambios significativos para aumentar la diversión y el desafío:

### Gameplay & Mecánicas
*   **Jefe Final (Boss Fight):** Cada 3 niveles te enfrentarás a un UFO gigante con una barra de vida escalable y patrones de ataque agresivos.
*   **Sistema de Power-ups:** Al destruir aliens, estos pueden soltar mejoras temporales:
    *   🔵 **Escudo:** Protege la nave contra un impacto fatal.
    *   🟢 **Disparo Múltiple:** Dispara ráfagas de 3 balas simultáneas.
    *   🟡 **Velocidad:** Aumenta temporalmente la rapidez de maniobra de la nave.
*   **Balas Especiales:** Cada 5 disparos normales, la nave dispara una bala súper potente (Super Bullet).
*   **Enemigos Ofensivos:** Los aliens ahora pueden devolver el fuego.
*   **Guardado de Puntuación:** El puntaje máximo (High Score) se guarda automáticamente en `highscore.txt`.

### Mejoras Visuales y Audio 🎨
*   **Modo Pantalla Completa:** El juego se adapta automáticamente a cualquier resolución de pantalla con escalado dinámico de elementos.
*   **Efectos de Partículas:** Explosiones dinámicas al destruir enemigos o recibir daño.
*   **Fondo Animado:** Un campo de estrellas (Starfield) que da sensación de profundidad y movimiento.
*   **Sistema de Audio:** Música de fondo envolvente y efectos de sonido para disparos, explosiones y recolección de objetos.
*   **Interfaz Actualizada:** Barra de vida para jefes, indicadores de nivel y contador de naves restantes.

## Requisitos y Ejecución 🎮

*   **Python 3.x**
*   **Pygame** (`pip install pygame`)

Para iniciar el juego, simplemente ejecuta:

```bash
python3 alien_invasion.py
```

## Controles ⌨️
*   **Flechas Izquierda/Derecha:** Mover la nave.
*   **Flecha Arriba/Abajo:** Movimiento vertical limitado.
*   **Barra Espaciadora:** Disparar.
*   **Enter:** Iniciar el juego / Reiniciar tras Game Over.
*   **Q:** Salir del juego.

## Créditos de Imágenes 🖼️
*   **Nave:** [NicePNG - Vector Spaces Ship](https://www.nicepng.com/ourpic/u2q8a9y3a9r5i1r5_vector-spaces-ship-8-bit-spaceship-sprite/)
*   **Aliens:** Inspirados en el clásico "Galaga".
*   **Fuentes:** Fuente `invasion.TTF` incluida en la carpeta `font/`.

---
Desarrollado y extendido por **valerasg** (Sergio Guadalupe Valadez Rivera).
