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
    env_id = "ALE/Breakout-v5"

    # Tworzymy równoległe środowiska Atari (64) i stackujemy 4 klatki
    env = make_atari_env(env_id, n_envs=64)
    env = VecFrameStack(env, n_stack=4)

    # Inicjalizujemy model PPO z parametrami
    model = PPO(
        "CnnPolicy",
        env=env,
        device="cuda",
        n_steps=256,
        batch_size=2048,
        n_epochs=4,
        learning_rate=2.5e-4,
        verbose=1,
        tensorboard_log="./tb_log"
    )

    model.learn(total_timesteps=8_000_000)
    model.save("nai_rl_breakout_model")

    test_env = make_atari_env(env_id, n_envs=1, seed=42)
    test_env = VecFrameStack(test_env, n_stack=4)

    obs = test_env.reset()
    done = [False]
    total_reward = 0

    while not done[0]:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, done, info = test_env.step(action)
        total_reward += rewards

    print(f"Testowy reward: {total_reward}")

if __name__ == "__main__":
    main()
