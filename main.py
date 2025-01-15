import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                            QDialog, QVBoxLayout, QLabel, QLineEdit,
                            QComboBox, QPushButton, QWidget, QTextEdit,
                            QMainWindow, QTextBrowser)
from PyQt5.QtCore import Qt, QPoint, QTimer, QEvent
from PyQt5.QtGui import QIcon, QCursor
import keyboard
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool)  # Hide from taskbar
        self.hide()  # Keep window hidden
        self.writing_tools_windows = []  # Keep track of all writing tools windows
        
    def closeEvent(self, event):
        # Prevent the window from being closed
        event.ignore()
        self.hide()

class MainApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_window = MainWindow()
        self.floating_button = None
        self.init_ui()
        self.setQuitOnLastWindowClosed(False)  # Prevent auto-quit when closing windows
        
    def init_ui(self):
        # Create system tray icon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("icon.png"))
        
        # Create tray menu
        menu = QMenu()
        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings)
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
        # Create floating button (no parent)
        self.floating_button = FloatingButton()
        
        # Setup clipboard monitoring
        self.last_text = ""
        
        # Setup timer for clipboard checking
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(100)  # Check every 100ms
        
    def show_settings(self):
        dialog = SettingsDialog(self.main_window)
        dialog.exec_()
        
    def quit(self):
        # Clean up and quit properly
        self.timer.stop()
        if self.floating_button:
            self.floating_button.hide()
        self.tray.hide()
        super().quit()
        
    def check_clipboard(self):
        try:
            if keyboard.is_pressed('ctrl+c'):
                time.sleep(0.1)  # Small delay to ensure clipboard is updated
                text = self.clipboard().text()
                if text.strip():  # Only check if text is not empty
                    self.last_text = text
                    # Get cursor position and show button
                    pos = QCursor.pos()
                    # Adjust position to account for padding and button size
                    self.floating_button.move(pos.x() - 60, pos.y() - 60)
                    self.floating_button.show()
                    # print("Showing floating button at:", pos.x() - 60, pos.y() - 60)  # Debug print
        except Exception as e:
            # print(f"Error in check_clipboard: {e}")  # Debug print
            pass
        
    def create_writing_tools_window(self, text):
        # Create new writing tools window
        window = WritingToolsWindow(text, self.main_window)
        self.main_window.writing_tools_windows.append(window)
        window.show()
        return window

class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.01)  # Almost invisible
        self.setGeometry(QApplication.desktop().geometry())
        self.hide()

    def mousePressEvent(self, event):
        # Hide the overlay and the floating button when clicked
        self.hide()
        if self.parent() and isinstance(self.parent(), FloatingButton):
            self.parent().hide()

class FloatingButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(None)  # No parent to ensure independent window
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |  # Keep on top
            Qt.FramelessWindowHint |   # No window frame
            Qt.Tool |                  # No taskbar icon
            Qt.NoDropShadowWindowHint  # No shadow
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.StrongFocus)  # Enable strong focus
        
        # Create layout with padding on top and left
        self.layout = QVBoxLayout()
        # Add padding: left, top, right, bottom
        self.layout.setContentsMargins(60, 60, 0, 0)
        
        # Create button
        self.button = QPushButton("✏️")
        self.button.setFixedSize(40, 40)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                border-radius: 20px;
                color: white;
                font-size: 16px;
                border: 2px solid #357abd;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        # Make the overall widget larger to accommodate the padding
        self.setFixedSize(100, 100)
        
        # Connect the button click and widget click
        self.button.clicked.connect(self.show_writing_tools)
        
        # Timer for checking cursor distance
        self.distance_timer = QTimer()
        self.distance_timer.timeout.connect(self.check_cursor_distance)
        self.distance_timer.setInterval(100)  # Check every 100ms
        self.max_distance = 50  # Maximum distance in pixels before hiding

    def check_cursor_distance(self):
        if not self.isVisible():
            return
            
        cursor_pos = QCursor.pos()
        widget_pos = self.geometry().topLeft()
        
        # Calculate button center (button is at bottom-right with 60px padding)
        button_center_x = widget_pos.x() + 80  # 60px padding + 20px (half of button width)
        button_center_y = widget_pos.y() + 80  # 60px padding + 20px (half of button height)
        
        # Calculate distance between cursor and button center
        distance = ((cursor_pos.x() - button_center_x) ** 2 + 
                   (cursor_pos.y() - button_center_y) ** 2) ** 0.5
                   
        # print(f"Distance to button center: {distance:.2f}")  # Debug print
        
        if distance > self.max_distance:
            # print("Cursor too far, hiding button")  # Debug print
            self.hide()

    def mousePressEvent(self, event):
        # Handle clicks anywhere in the widget
        self.show_writing_tools()

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
        self.distance_timer.start()  # Start checking cursor distance

    def show_writing_tools(self):
        clipboard = QApplication.instance().clipboard()
        selected_text = clipboard.text()
        if selected_text.strip():
            app = QApplication.instance()
            app.create_writing_tools_window(selected_text)
        self.hide()

    def hide(self):
        self.distance_timer.stop()  # Stop the distance checking timer
        super().hide()

class WritingToolsWindow(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ollama Writing Tools")
        # Remove the help button from the title bar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.text = text
        self.functions = self.load_functions()
        self.setup_ui()
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowModality(Qt.NonModal)
        
    def load_functions(self):
        try:
            with open('functions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('functions', [])
        except Exception as e:
            # print(f"Error loading functions: {e}")
            return []
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create buttons for each function
        button_layout = QVBoxLayout()
        
        for func in self.functions:
            button = QPushButton(f"{func['icon']} {func['name']}")
            button.setToolTip(func['description'])
            button.clicked.connect(lambda checked, f=func: self.process_text(f))
            button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px;
                    font-size: 12pt;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
            """)
            button_layout.addWidget(button)
        
        # Add loading indicator
        self.loading_label = QLabel("Generating result...")
        self.loading_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-style: italic;
            }
        """)
        self.loading_label.hide()
        button_layout.addWidget(self.loading_label)
        
        layout.addLayout(button_layout)
        
        # Result area with markdown support and buttons
        result_header_layout = QVBoxLayout()
        result_label = QLabel("Result:")
        
        # Button layout for copy and paste - changed to horizontal
        button_container = QVBoxLayout()
        button_row = QVBoxLayout()  # Container for buttons in a row
        
        # Add copy button
        copy_button = QPushButton("📋 Copy")
        copy_button.setToolTip("Copy result to clipboard")
        copy_button.clicked.connect(self.copy_result)
        copy_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        
        # Add paste button
        paste_button = QPushButton("📝 Replace")  # Changed text from Paste to Replace
        paste_button.setToolTip("Replace selected text with result")  # Updated tooltip
        paste_button.clicked.connect(self.paste_result)
        paste_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        
        # Add buttons horizontally
        button_row.addWidget(copy_button)
        button_row.addWidget(paste_button)
        button_row.setDirection(QVBoxLayout.LeftToRight)  # Make layout horizontal
        
        result_header_layout.addWidget(result_label)
        result_header_layout.addLayout(button_row)
        layout.addLayout(result_header_layout)
        
        # Result text browser
        self.result_text = QTextBrowser()
        self.result_text.setOpenExternalLinks(True)
        self.result_text.setMinimumHeight(300)
        
        # Apply font size from settings
        font = self.result_text.font()
        font.setPointSize(Settings.get_font_size())
        self.result_text.setFont(font)
        
        self.result_text.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
            }
        """)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
        
    def copy_result(self):
        text = self.result_text.toPlainText()
        if text:
            clipboard = QApplication.instance().clipboard()
            clipboard.setText(text)
            
    def paste_result(self):
        # Copy the result to clipboard
        text = self.result_text.toPlainText()
        if text:
            clipboard = QApplication.instance().clipboard()
            clipboard.setText(text)
            # Hide the window first
            self.hide()
            # Add a delay to ensure window is hidden and clipboard is updated
            QTimer.singleShot(100, lambda: keyboard.send('ctrl+v'))
            
    def process_text(self, function):
        # Show loading indicator and disable all buttons
        self.loading_label.show()
        for button in self.findChildren(QPushButton):
            button.setEnabled(False)
            
        # Clear previous result
        self.result_text.clear()
        QApplication.processEvents()  # Force UI update
        
        try:
            # Format the prompt with the actual text
            prompt = function['prompt'].format(selection=self.text)
            
            response = requests.post(
                f"http://{Settings.get_api_url()}/api/generate",
                json={
                    "model": Settings.get_selected_model(),
                    "prompt": prompt,
                    "temperature": function.get('temperature', 0.7),
                    "stream": False
                }
            )
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'response' in result:
                        # Set markdown text
                        self.result_text.setMarkdown(result['response'])
                    else:
                        self.result_text.setPlainText("Error: Invalid response format from API")
                except json.JSONDecodeError:
                    self.result_text.setPlainText("Error: Invalid JSON response from API")
            else:
                self.result_text.setPlainText(f"Error: Server returned status code {response.status_code}")
        except Exception as e:
            self.result_text.setPlainText(f"Error: {str(e)}")
        finally:
            # Hide loading indicator and enable all buttons
            self.loading_label.hide()
            for button in self.findChildren(QPushButton):
                button.setEnabled(True)

    def closeEvent(self, event):
        # Hide the window instead of closing it
        event.ignore()
        self.hide()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # API URL
        layout.addWidget(QLabel("Ollama API URL:"))
        self.api_url = QLineEdit(Settings.get_api_url())
        layout.addWidget(self.api_url)
        
        # Model selection
        layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.refresh_models()
        layout.addWidget(self.model_combo)
        
        # Refresh models button
        refresh_button = QPushButton("Refresh Models")
        refresh_button.clicked.connect(self.refresh_models)
        layout.addWidget(refresh_button)
        
        # Font size selection
        layout.addWidget(QLabel("Font Size:"))
        self.font_size_combo = QComboBox()
        for size in [8, 10, 12, 14, 16, 18, 20]:
            self.font_size_combo.addItem(f"{size}pt", size)
        # Set current font size
        current_size = Settings.get_font_size()
        index = self.font_size_combo.findData(current_size)
        if index >= 0:
            self.font_size_combo.setCurrentIndex(index)
        layout.addWidget(self.font_size_combo)
        
        # Button layout
        button_layout = QVBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def refresh_models(self):
        try:
            response = requests.get(f"http://{Settings.get_api_url()}/api/tags")
            models = response.json()
            self.model_combo.clear()
            for model in models.get('models', []):
                self.model_combo.addItem(model['name'])
            if self.model_combo.count() > 0:
                current_model = Settings.get_selected_model()
                index = self.model_combo.findText(current_model)
                if index >= 0:
                    self.model_combo.setCurrentIndex(index)
        except Exception as e:
            # print(f"Error fetching models: {e}")
            pass
    
    def save_settings(self):
        Settings.save_api_url(self.api_url.text())
        if self.model_combo.currentText():
            Settings.save_selected_model(self.model_combo.currentText())
        Settings.save_font_size(self.font_size_combo.currentData())
        self.close()  # Use close() instead of accept()

    def closeEvent(self, event):
        # Just close the dialog without affecting the main application
        event.accept()  # Use accept() to allow the dialog to close normally

class Settings:
    @staticmethod
    def get_api_url():
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return settings.get('api_url', '127.0.0.1:11434')
        except:
            return '127.0.0.1:11434'
    
    @staticmethod
    def get_selected_model():
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return settings.get('model', 'llama2')
        except:
            return 'llama2'
            
    @staticmethod
    def get_font_size():
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return settings.get('font_size', 12)
        except:
            return 12
    
    @staticmethod
    def save_api_url(url):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {}
        settings['api_url'] = url
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    
    @staticmethod
    def save_selected_model(model):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {}
        settings['model'] = model
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
            
    @staticmethod
    def save_font_size(size):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {}
        settings['font_size'] = size
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

def main():
    app = MainApplication(sys.argv)
    # This ensures the app stays running
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 