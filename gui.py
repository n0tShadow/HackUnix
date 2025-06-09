from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget,
    QToolBar, QAction, QFileDialog, QMessageBox, QLabel, QInputDialog
)
from PyQt6.QtCore import Qt
import threading

import network_tools
import requests_tools

class HackUnixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HackUnix 1.0")
        self.resize(900, 600)
        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        self.script_editor = QTextEdit()
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter domain or IP address...")
        self.input_line.returnPressed.connect(self.resolve_ip_action)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Input (URL/IP):"))
        layout.addWidget(self.input_line)
        layout.addWidget(QLabel("Script Editor (.hcka):"))
        layout.addWidget(self.script_editor)
        layout.addWidget(QLabel("Output Console:"))
        layout.addWidget(self.output_console)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        settings_menu = menubar.addMenu("Settings")
        dev_menu = menubar.addMenu("Dev")
        about_menu = menubar.addMenu("About")

        file_menu.addAction(self.new_script_action())
        file_menu.addAction(self.load_script_action())
        file_menu.addAction(self.example_script_action())

        edit_menu.addAction(self.undo_action())
        edit_menu.addAction(self.redo_action())

        settings_menu.addAction(self.settings_action())

        dev_menu.addAction(self.dev_tools_action())

        about_menu.addAction(self.about_action())
        about_menu.addAction(self.github_action())
        about_menu.addAction(self.exit_action())

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        toolbar.addAction(self.run_script_action())
        toolbar.addAction(self.resolve_ip_action_btn())
        toolbar.addAction(self.ping_host_action())
        toolbar.addAction(self.ip_info_action())
        toolbar.addAction(self.reverse_dns_action())
        toolbar.addAction(self.scan_ports_action())
        toolbar.addAction(self.http_headers_action())

    # --- Actions ---

    def new_script_action(self):
        action = QAction("New Script", self)
        action.triggered.connect(self.new_script)
        return action

    def load_script_action(self):
        action = QAction("Load Script", self)
        action.triggered.connect(self.load_script)
        return action

    def example_script_action(self):
        action = QAction("Example Script", self)
        action.triggered.connect(self.load_example_script)
        return action

    def undo_action(self):
        action = QAction("Undo", self)
        action.triggered.connect(self.script_editor.undo)
        return action

    def redo_action(self):
        action = QAction("Redo", self)
        action.triggered.connect(self.script_editor.redo)
        return action

    def settings_action(self):
        action = QAction("Settings", self)
        action.triggered.connect(self.show_settings)
        return action

    def dev_tools_action(self):
        action = QAction("Dev tools (in development)", self)
        return action

    def about_action(self):
        action = QAction("About HackUnix", self)
        action.triggered.connect(self.show_about)
        return action

    def github_action(self):
        action = QAction("GitHub", self)
        action.triggered.connect(lambda: QMessageBox.information(self, "GitHub", "Open your GitHub link manually"))
        return action

    def exit_action(self):
        action = QAction("Exit", self)
        action.triggered.connect(self.close)
        return action

    def run_script_action(self):
        action = QAction("Run Script", self)
        action.triggered.connect(self.run_script)
        return action

    def resolve_ip_action_btn(self):
        action = QAction("Resolve IP", self)
        action.triggered.connect(self.resolve_ip_action)
        return action

    def ping_host_action(self):
        action = QAction("Ping Host", self)
        action.triggered.connect(self.ping_host_dialog)
        return action

    def ip_info_action(self):
        action = QAction("Get IP Info", self)
        action.triggered.connect(self.ip_info_dialog)
        return action

    def reverse_dns_action(self):
        action = QAction("Reverse DNS", self)
        action.triggered.connect(self.reverse_dns_dialog)
        return action

    def scan_ports_action(self):
        action = QAction("Port Scan", self)
        action.triggered.connect(self.port_scan_dialog)
        return action

    def http_headers_action(self):
        action = QAction("HTTP Headers", self)
        action.triggered.connect(self.http_headers_dialog)
        return action

    # --- Functions ---

    def append_output(self, text):
        self.output_console.append(text)

    def resolve_ip_action(self):
        domain = self.input_line.text().strip()
        if domain:
            self.append_output(f"Resolving IP for: {domain}")
            ip = network_tools.resolve_ip(domain)
            self.append_output(f"IP: {ip}\n")

    def ping_host_dialog(self):
        host, ok = QInputDialog.getText(self, "Ping Host", "Enter domain or IP:")
        if ok and host:
            def ping():
                self.append_output(f"Pinging {host}...")
                result = network_tools.ping_host(host)
                self.append_output(result)
            threading.Thread(target=ping).start()

    def ip_info_dialog(self):
        ip, ok = QInputDialog.getText(self, "Get IP Info", "Enter IP address:")
        if ok and ip:
            def info():
                self.append_output(f"Getting IP info for {ip}...")
                result = requests_tools.get_ip_info(ip)
                self.append_output(result)
            threading.Thread(target=info).start()

    def reverse_dns_dialog(self):
        ip, ok = QInputDialog.getText(self, "Reverse DNS", "Enter IP address:")
        if ok and ip:
            self.append_output(f"Reverse DNS lookup for {ip}")
            result = network_tools.reverse_dns(ip)
            self.append_output(f"Result: {result}\n")

    def port_scan_dialog(self):
        host, ok = QInputDialog.getText(self, "Port Scan", "Enter domain or IP:")
        if ok and host:
            self.append_output(f"Scanning ports on {host}...")
            def scan():
                open_ports = network_tools.scan_ports(host)
                if open_ports:
                    self.append_output(f"Open ports: {', '.join(map(str, open_ports))}")
                else:
                    self.append_output("No open ports found.")
            threading.Thread(target=scan).start()

    def http_headers_dialog(self):
        url, ok = QInputDialog.getText(self, "HTTP Headers", "Enter URL:")
        if ok and url:
            self.append_output(f"Fetching HTTP headers for {url}...")
            def fetch():
                result = requests_tools.get_http_headers(url)
                self.append_output(result)
            threading.Thread(target=fetch).start()

    def new_script(self):
        self.script_editor.clear()

    def load_script(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Script", "", "HackAutomation Scripts (*.hcka);;All Files (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.script_editor.setPlainText(f.read())
            self.append_output(f"Loaded script: {path}")

    def load_example_script(self):
        example = "# Example HackAutomation (.hcka) script\nprint('Hello from HackUnix!')"
        self.script_editor.setPlainText(example)
        self.append_output("Loaded example script.")

    def run_script(self):
        script = self.script_editor.toPlainText()
        # Простая имитация интерпретатора .hcka — выполняем на Python
        try:
            exec(script, {"__builtins__": __builtins__, "print": self.append_output})
        except Exception as e:
            self.append_output(f"Script error: {e}")

    def show_settings(self):
        QMessageBox.information(self, "Settings", "Settings dialog coming soon!")

    def show_about(self):
        QMessageBox.information(self, "About HackUnix", "HackUnix by Shadow\nEthical hacking toolkit\nMore features coming soon!")

    def apply_dark_theme(self):
        dark_stylesheet = """
        QMainWindow { background-color: #121212; color: #eeeeee; }
        QTextEdit, QLineEdit { background-color: #1e1e1e; color: #ffffff; }
        QToolBar { background-color: #222222; border: none; }
        QMenuBar { background-color: #222222; color: #eeeeee; }
        QMenu { background-color: #222222; color: #eeeeee; }
        """
        self.setStyleSheet(dark_stylesheet)