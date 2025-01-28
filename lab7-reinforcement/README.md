# LAB7 - RL - Breakout – Wczytywanie Wytrenowanego Modelu i Test

**Autor**: Aleksander Opałka s24399

## Opis problemu
Projekt demonstruje użycie **Reinforcement Learning** (algorytm PPO) do nauki agenta w grze *Breakout* (dostępnej w ramach Arcade Learning Environment).  
Po zakończonym treningu powstaje plik `nai_rl_breakout_model.zip` (zapisany model PPO).  
Skrypt `play_breakout.py` ładuje ten wytrenowany model i **uruchamia go** w środowisku *Breakout*, w trybie wizualnym (`render_mode="human"`), aby można było **obserwować rozgrywkę**.

## Wymagane biblioteki

- **Python 3.7+**  
- [**gymnasium[atari]**](https://github.com/Farama-Foundation/Gymnasium) (oraz `ale_py`)  
- [**stable-baselines3**](https://stable-baselines3.readthedocs.io/) (z algorytmem PPO)  
- Ewentualnie inne pakiety: `numpy`, `time`, itd.

Instalacja przykładowa (w wirtualnym środowisku):
```bash
pip install gymnasium[atari] ale-py stable-baselines3
