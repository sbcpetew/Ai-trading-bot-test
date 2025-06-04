"""Minimal PySide6 GUI placeholder."""
try:
    from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
except ModuleNotFoundError as exc:
    raise RuntimeError("PySide6 must be installed to use the AlphaFive GUI") from exc
import subprocess
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlphaFive Control Console")
        layout = QVBoxLayout()
        self.status = QLabel("idle")
        train_btn = QPushButton("Train Model")
        paper_btn = QPushButton("Paper Trade")
        live_btn = QPushButton("Live Trade")
        train_btn.clicked.connect(self.train)
        paper_btn.clicked.connect(self.paper)
        live_btn.clicked.connect(self.live)
        layout.addWidget(train_btn)
        layout.addWidget(paper_btn)
        layout.addWidget(live_btn)
        layout.addWidget(self.status)
        self.setLayout(layout)

    def _run(self, cmd):
        proc = subprocess.Popen([sys.executable, "-m", cmd])
        self.status.setText(f"{cmd} running...")
        proc.wait()
        self.status.setText("idle")

    def train(self):
        self._run("alphafive.train")

    def paper(self):
        self._run("alphafive.paper")

    def live(self):
        self._run("alphafive.live")


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
