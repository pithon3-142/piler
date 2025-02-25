#imports
#library that allows interaction with operating system and its data
import os
import sys
#library that enables the copying, moving, deleting of files etc.
import shutil

#import GUI library components
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox
)

class Filer(QWidget):
    #define constructor method of the class
    def __init__(self):
        super().__init__()
        self.initUI()

    #define and setup the layout
    def initUI(self):
        layout = QVBoxLayout()

        #label for the source dir 
        self.src_label = QLabel("Source Directory : Not Selected", self)
        layout.addWidget(self.src_label)
    
        #button to select the source directory
        self.src_btn = QPushButton("Select Source", self)
        self.src_btn.clicked.connect(self.select_src_dir)
        layout.addWidget(self.src_btn)

        #select category label
        self.category = QLabel("Select File Category", self)
        layout.addWidget(self.category)

        #category dropdown
        self.category_menu = QComboBox(self)
        self.category_menu.addItems(["Text", "Image", "Audio", "Video", "Archive"])
        self.category_menu.currentTextChanged.connect(self.update_file_types)  # Connect signal to method
        layout.addWidget(self.category_menu)

        #file type label & dropdown
        self.file_type_label = QLabel("Select File Type(s)", self)
        layout.addWidget(self.file_type_label)  
        self.file_type_menu = QComboBox(self)
        layout.addWidget(self.file_type_menu)

        #target directory
        self.tgt_label = QLabel("Target Directory : Not Selected", self)
        layout.addWidget(self.tgt_label)

        self.tgt_btn = QPushButton("Select Target", self)
        self.tgt_btn.clicked.connect(self.select_tgt_dir)
        layout.addWidget(self.tgt_btn)

        #organize button
        self.org_btn = QPushButton("Organize", self)
        self.org_btn.clicked.connect(self.organize_files)  # Corrected connection
        layout.addWidget(self.org_btn)

        #layout
        self.setLayout(layout)
        self.setWindowTitle("Pi-Filer : Ultimate File Organizer")
        self.setGeometry(500, 200, 800, 800)

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