import argparse
from src.agentic.agent import run_demo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='gemma3:1b', help='Model name to use')
    parser.add_argument('--prompt', default='Generate an original TV episode script inspired by The Expanse', help='Prompt to send')
    parser.add_argument('--episodes', type=int, default=1, help='Number of episodes to generate')
    parser.add_argument('--save', action='store_true', help='Save generated episodes to files')
    parser.add_argument('--out-dir', default='episodes', help='Directory to save episodes')
    args = parser.parse_args()

    run_demo(model=args.model, prompt=args.prompt, episodes=args.episodes, save_dir=(args.out_dir if args.save else None))


if __name__ == '__main__':
    main()
