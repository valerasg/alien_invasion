# Changelog - Alien Invasion (Sergio Edition)

## [1.1.0] - 2026-03-16

### Añadido
- **Sistema de Partículas:** Explosiones visuales al destruir enemigos.
- **Fondo Animado:** Campo de estrellas (starfield) con movimiento de profundidad.
- **Power-ups:** 
  - *Escudo (Azul):* Protege contra un impacto.
  - *Disparo Múltiple (Verde):* Ráfaga de 3 balas.
  - *Velocidad (Amarillo):* Aumento temporal de rapidez de la nave.
- **Jefe Final (Boss):** Aparición de un UFO gigante cada 3 niveles con barra de vida y patrones de ataque.
- **Audio:** Música de fondo y efectos de sonido para disparos, explosiones y power-ups.
- **Modo Pantalla Completa:** El juego se adapta automáticamente a la resolución del monitor.

### Cambios y Mejoras
- **Escalado Dinámico:** Los elementos (nave, boss, límites de flota) se ajustan proporcionalmente al tamaño de la pantalla.
- **Optimización de Flota:** Límite máximo de aliens para mantener la jugabilidad en altas resoluciones.
- **Refactorización de Código:** Centralización de colisiones en `game_functions.py` para mayor rendimiento.
- **Limpieza de Proyecto:** Eliminación de archivos redundantes, scripts temporales y entornos virtuales obsoletos.

### Correciones (Bug Fixes)
- Solucionado error `UnboundLocalError` en `Enemy_Bullet` cuando el Boss intentaba disparar.
- Corregido error de renderizado donde el Boss se salía de los límites de la pantalla.
