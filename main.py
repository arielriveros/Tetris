from tetris.tetris import Tetris
import sys

if __name__ == "__main__":
    app = Tetris(test=sys.argv[1] if len(sys.argv) > 1 else None)
    app.run()