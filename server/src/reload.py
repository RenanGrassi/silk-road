from watchfiles import run_process


def run_server():
    run_process(["python", "src/main.py"], target="/app")


if __name__ == "__main__":
    run_server()
