# BYteCruncher
Byte Cruncher
Advanced Huffman Compression Tool with GUI

Byte Cruncher is a modern, user-friendly desktop application for compressing and decompressing text files using the Huffman coding algorithm. It features a sleek dark-themed interface, real-time progress and statistics, and simple file management-all powered by Python and Tkinter.

Features
Huffman Compression & Decompression: Efficiently compress .txt files to binary and restore them back.

Modern GUI: Intuitive, dark-themed interface built with Tkinter.

Drag-and-Drop File Selection: Easily browse and select files.

Live Progress Bar: Visual feedback during compression and decompression.

Detailed Stats: View original size, compressed size, and compression ratio.

Safe File Handling: Download/save compressed or decompressed files to your chosen location.

Error Handling: Clear error messages for invalid operations or file issues.

Installation
Prerequisites:

Python 3.7 or newer

Install required packages (Tkinter is included with most Python installations):

bash
pip install --upgrade pip
Clone the repository:

cd byte-cruncher
Usage
Run the application:

bash
python main.py
Select a file:

Click "Browse" and choose a .txt file to compress, or a .bin file to decompress.

Compress or Decompress:

Click "Compress" to create a compressed .bin file, or "Decompress" to restore a .txt file.

Save the result:

After a successful operation, click "Save As" to choose where to store the output file.
