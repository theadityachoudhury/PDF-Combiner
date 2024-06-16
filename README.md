
# PDF Merger Application



## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)
- [Contact](#contact)
## Overview
This Python application allows you to merge multiple PDF files into a single PDF document. It provides a simple graphical interface using `tkinter` for selecting input files and specifying the output file path.

## Installation
To use this application, follow these steps:

#### Clone the repository
```bash
git clone https://github.com/theadityachoudhury/pdf-merger.git
cd pdf-merger
```

#### Install Dependencies
Ensure you have Python installed. Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```
This installs `PyPDF2` which is used for PDF manipulation.
## Usage/Examples

#### Run the Application:
```bash
python main.py
```
This command launches the PDF merger Application
#### Select Input Directory
Click on the "Browse..." button next to "Select Directory" to choose the directory containing the PDF files you want to merge.

#### Specify output files
Click on the "Browse..." button next to "Output File" to choose the location and name of the output merged PDF file.


#### Merge PDFs
Click on the "Merge PDFs" button to start the merging process. The application will log the merging progress and notify you upon completion.

#### View history
Switch to the "History" tab to view a list of previously merged PDF files. Double-click on any entry to open its location in your file explorer.
## Authors

- Name: Aditya Choudhury
- [@theadityachoudhury](https://www.github.com/theadityachoudhury)
- Email: [aditya@adityachoudhury.com](email:aditya@adityachoudhury.com)


## Additional Notes

- Modify paths and file names (main.py, requirements.txt, etc.) as per your project structure.
- Provide clear and concise instructions for users to easily understand and use your application.
- Include any additional sections or details specific to your project that would benefit users.