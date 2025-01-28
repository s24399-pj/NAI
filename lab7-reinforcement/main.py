import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
import ale_py

def main():
    """
     Ten skrypt wczytuje wytrenowany model PPO (zapisany w pliku "nai_rl_breakout_model")
    i uruchamia go w środowisku Breakout (z pakietu ALE/Atari) w trybie wizualnym.
    Dzięki temu możemy obserwować, jak agent gra w grę po zakończonym treningu.

    Autor: Aleksander Opałka
    """
    env_id = "ALE/Breakout-v5"  # Identyfikator środowiska Atari

    # Tworzymy 64 równoległe środowiska Atari
    env = make_atari_env(env_id, n_envs=64)

    # Stackujemy 4 klatki w jedno obserwowane wejście
    env = VecFrameStack(env, n_stack=4)

    # Inicjalizujemy model PPO z wybranymi parametrami
    model = PPO(
        "CnnPolicy",  # Typ polityki (z siecią CNN)
        env=env,  # Środowisko
        device="cuda",  # Wykorzystanie GPU
        n_steps=256,  # Liczba kroków na jedną aktualizację
        batch_size=2048,  # Rozmiar batcha
        n_epochs=4,  # Liczba epok na aktualizację
        learning_rate=2.5e-4,  # Szybkość uczenia
        verbose=1,  # Szczegółowość logów
        tensorboard_log="./tb_log"  # Ścieżka do logów TensorBoard
    )

    # Trenuj model przez 8 milionów kroków
    model.learn(total_timesteps=8_000_000)

    # Zapisz wytrenowany model do pliku
    model.save("nai_rl_breakout_model")

if __name__ == "__main__":
    main()
