import time
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.env_util import make_atari_env
import ale_py


def main():
    """
    Odtwarzanie gry Breakout przy użyciu wstępnie wytrenowanego modelu PPO (render_mode="human").

    Skrypt ładuje wcześniej wytrenowanego agenta (nai_rl_breakout_model.zip) i uruchamia go
    w pojedynczym środowisku Breakout z wizualizacją w oknie.
    Możesz obserwować kilka epizodów rozgrywki i zobaczyć, jaki wynik (reward) osiąga agent.

    Autor: Aleksander Opałka
    """

    # Wczytaj wytrenowany model PPO
    model = PPO.load("nai_rl_breakout_model")

    # Utwórz środowisko gry Breakout z wizualizacją
    env = make_atari_env(
        env_id="ALE/Breakout-v5",  # Identyfikator środowiska Atari
        n_envs=1,  # Pojedyncze środowisko
        seed=42,  # Ustaw ziarno losowości
        env_kwargs={"render_mode": "human"}  # Tryb wizualizacji
    )

    # Zintegruj ramki (klatki) w wektor
    env = VecFrameStack(env, n_stack=4)

    num_episodes = 10  # Liczba epizodów do uruchomienia

    for ep in range(num_episodes):
        obs = env.reset()  # Zresetuj środowisko
        done = [False]  # Flaga końca epizodu
        total_reward = 0.0  # Suma nagród w epizodzie

        while not done[0]:  # Kontynuuj, dopóki epizod się nie zakończy
            action, _ = model.predict(obs, deterministic=True)  # Przewidź akcję
            obs, rewards, done, info = env.step(action)  # Wykonaj krok w środowisku
            total_reward += rewards[0]  # Dodaj nagrodę za bieżący krok
            time.sleep(0.02)  # Spowolnij rozgrywkę dla czytelniejszej wizualizacji

        print(f"Epizod {ep + 1} skończony, total_reward={total_reward}")  # Wynik epizodu

    env.close()  # Zamknij środowisko

if __name__ == "__main__":
    main()
