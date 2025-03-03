#imports
#library that allows interaction with operating system and its data
import os
import sys
#library that enables the copying, moving, deleting of files etc.
import shutil

#import GUI library components
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFileDialog, QComboBox, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Filer(QWidget):
    #define constructor method of the class
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stylesheet()

    def stylesheet(self):
        qss_file = "style.qss"
        if os.path.exists(qss_file):
            with open(qss_file, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print("qss file not found")

    #define and setup the layout
    def initUI(self):
        layout = QVBoxLayout()

        self.title = QLabel("piler")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        self.title.setObjectName("title")

        self.description = QLabel("Organize any type of your files😉.\nIt's easy, quick and seamless.")
        self.description.setObjectName("description")
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setWordWrap(True)
        layout.addWidget(self.description)

        #function to create line separators for sections
        def separator():
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("color: #D1D5DB ; background-color: #D1D5DB ; height: 3px;")
            layout.addWidget(line)
            return line

        separator()

    
        #button to select the source directory
        self.src_btn = QPushButton("Select Source", self)
        self.src_btn.clicked.connect(self.select_src_dir)
        self.src_btn.setFixedWidth(300)
        layout.addWidget(self.src_btn, alignment=Qt.AlignCenter)

        #label for the source dir 
        self.src_label = QLabel("Source Directory : Not Selected", self)
        layout.addWidget(self.src_label, alignment=Qt.AlignCenter)

        separator()

        #category label and dropdown
        self.category_layout = QHBoxLayout()
        self.category_layout.setObjectName("cl")

        self.category = QLabel("Select File Category", self)

        self.category_menu = QComboBox(self)
        self.category_menu.addItems(["Text", "Image", "Audio", "Video", "Archive"])
        self.category_menu.currentTextChanged.connect(self.update_file_types)  # Connect signal to method

        #add to main layout
        self.category_layout.addWidget(self.category_menu)
        self.category_layout.addWidget(self.category)
        self.category_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(self.category_layout)

        #file type label & dropdown
        self.file_type_layout = QHBoxLayout()

        self.file_type_label = QLabel("Select File Type(s)...", self)
        self.file_type_menu = QComboBox(self)
        self.file_type_layout.setAlignment(Qt.AlignCenter)

        self.file_type_layout.addWidget(self.file_type_menu)
        self.file_type_layout.addWidget(self.file_type_label)
        layout.addLayout(self.file_type_layout)

        separator()

        #target dir button
        self.tgt_btn = QPushButton("Select Target", self)
        self.tgt_btn.clicked.connect(self.select_tgt_dir)
        self.tgt_btn.setFixedWidth(300)
        layout.addWidget(self.tgt_btn, alignment=Qt.AlignCenter)

        #target directory
        self.tgt_label = QLabel("Target Directory : Not Selected", self)
        layout.addWidget(self.tgt_label, alignment=Qt.AlignCenter)

        separator()

        #organize button
        self.org_btn = QPushButton("Organize", self)
        self.org_btn.clicked.connect(self.organize_files)
        self.org_btn.setFixedWidth(300)
        layout.addWidget(self.org_btn, alignment=Qt.AlignCenter)

        #layout
        self.setLayout(layout)
        self.setWindowIcon(QIcon('Pi.jpg'))
        self.setWindowTitle("Pi-Filer : Ultimate File Organizer")
        self.setGeometry(500, 100, 800, 800)
        self.setWindowOpacity(0.97)
        self.update_file_types()

    #function for the selection of the source directory
    def select_src_dir(self):
        #open dialog to select
        self.src_dir = QFileDialog.getExistingDirectory(self, "Select Source Directory")

        if self.src_dir:
            self.src_label.setText(f"Source Directory : {self.src_dir}")

    #function to select the target directory
    def select_tgt_dir(self):
        self.tgt_dir = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        
        if self.tgt_dir:
            self.tgt_label.setText(f"Target Directory : {self.tgt_dir}")

    #function to update file types based on selected category
    def update_file_types(self):
        #set categories and their corresponding file ext
        category = {
            "Text": [".txt", ".docx", ".pdf", ".xls", ".pptx", ".log", ".csv"],
            "Image": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf"],
            "Audio": [".mp3", ".aac", ".wav", ".m4a", ".opus"],
            "Video": [".mp4", ".mkv", ".mov", ".wmv", ".webm"],
            "Archive": [".zip", ".rar", ".7z", ".tar", ".iso", ".dmg"]
        }

        selected_category = self.category_menu.currentText()

        #updating file type with the extensions for the currently selected category
        self.file_type_menu.clear()
        self.file_type_menu.addItems(category.get(selected_category, []))

    def organize_files(self):
        #check if directories are selected
        if not hasattr(self, 'src_dir') or not hasattr(self, 'tgt_dir'):
            QMessageBox.warning(self, "Error", "Please select both Source and Target directories to proceed")
            return

        file_type = self.file_type_menu.currentText()

        if not file_type:
            QMessageBox.warning(self, "Error", "You have not selected any File Extension.")
            return

        #Organize files with error handling
        try:
            files = [f for f in os.listdir(self.src_dir) if f.endswith(file_type)]

            if not files:
                QMessageBox.information(self, "No Files", f"No {file_type} files were found in the Source Directory")
                return
            
            tgt_folder = os.path.join(self.tgt_dir, self.category_menu.currentText())

            if not os.path.exists(tgt_folder):
                os.makedirs(tgt_folder)

            #move files
            for file in files:
                shutil.move(
                    os.path.join(self.src_dir, file),
                    os.path.join(tgt_folder, file)
                )
            
            QMessageBox.information(self, "Success", f"All {self.category_menu.currentText()} Files have been moved to {tgt_folder}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Filer()
    window.show()
    sys.exit(app.exec())