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
    w pojedynczym środowisku Breakout z wizualizacją w oknie (tzw. tryb "human").
    Możesz obserwować kilka epizodów rozgrywki i zobaczyć, jaki wynik (reward) osiąga agent.

    Autor: Aleksander Opałka
    """

    # 1. Wczytujemy wytrenowany model
    model = PPO.load("nai_rl_breakout_model")  # plik utworzony w main.py

    # 2. Tworzymy środowisko w *taki sam sposób*,
    #    ale tym razem z n_envs=1 i parametrem render_mode="human" (o ile jest wspierany).
    env = make_atari_env(
        env_id="ALE/Breakout-v5",
        n_envs=1,
        seed=42,
        env_kwargs={"render_mode": "human"}
    )
    env = VecFrameStack(env, n_stack=4)

    num_episodes = 10

    for ep in range(num_episodes):
        obs = env.reset()
        done = [False]
        total_reward = 0.0

        while not (done[0] ):
            action, _ = model.predict(obs, deterministic=True)
            obs, rewards, done, info = env.step(action)
            total_reward += rewards[0]
            time.sleep(0.02)

        print(f"Epizod {ep+1} skończony, total_reward={total_reward}")

    env.close()

if __name__ == "__main__":
    main()
