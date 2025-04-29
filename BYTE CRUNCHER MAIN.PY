import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import heapq
from collections import defaultdict

# Huffman Node class
class Node:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Huffman Compression Handler
class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        freq = defaultdict(int)
        for char in text:
            freq[char] += 1
        return freq

    def build_heap(self, frequency):
        heap = [Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)
        return heap

    def merge_nodes(self, heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)
        return heap[0]

    def make_codes_helper(self, node, current_code):
        if node:
            if node.char is not None:
                self.codes[node.char] = current_code
                self.reverse_mapping[current_code] = node.char
            self.make_codes_helper(node.left, current_code + "0")
            self.make_codes_helper(node.right, current_code + "1")

    def make_codes(self, root):
        self.make_codes_helper(root, "")

    def get_encoded_text(self, text):
        return ''.join(self.codes[char] for char in text)

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = f"{extra_padding:08b}"
        return padded_info + encoded_text

    def get_byte_array(self, padded_encoded_text):
        return bytearray(int(padded_encoded_text[i:i+8], 2) for i in range(0, len(padded_encoded_text), 8))

    def compress(self, input_path, output_path):
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        freq = self.make_frequency_dict(text)
        heap = self.build_heap(freq)
        tree_root = self.merge_nodes(heap)
        self.make_codes(tree_root)

        encoded = self.get_encoded_text(text)
        padded = self.pad_encoded_text(encoded)
        byte_data = self.get_byte_array(padded)

        with open(output_path, 'wb') as out:
            out.write(bytes(byte_data))

        return len(text), len(byte_data)

    def remove_padding(self, padded_text):
        pad_info = int(padded_text[:8], 2)
        return padded_text[8:-pad_info]

    def decode_text(self, encoded_text):
        current_code = ""
        decoded = []
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded.append(self.reverse_mapping[current_code])
                current_code = ""
        return ''.join(decoded)

    def decompress(self, input_path, output_path):
        with open(input_path, 'rb') as file:
            bit_string = ''.join(f"{byte:08b}" for byte in file.read())

        encoded = self.remove_padding(bit_string)
        decoded = self.decode_text(encoded)

        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(decoded)

        return len(decoded)

# Improved GUI Setup
class ByteCruncherApp:
    def __init__(self, root):
        self.huffman = HuffmanCoding()
        self.root = root
        self.root.title("Byte Cruncher")
        self.root.geometry("600x500")
        self.setup_theme()
        
        # Main layout
        self.create_main_frame()
        self.create_header()
        self.create_file_section()
        self.create_action_buttons()
        self.create_result_section()
        
        # Instance variables
        self.file_path = None
        self.output_path = None
        self.is_compressed = False
        
    def setup_theme(self):
        # Set a dark theme
        bg_color = "#1e1e1e"
        text_color = "#f0f0f0"
        highlight_color = "#007acc"
        
        self.root.configure(bg=bg_color)
        self.theme = {
            "bg": bg_color,
            "fg": text_color,
            "button_bg": "#333333",
            "button_fg": text_color,
            "highlight": highlight_color,
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336"
        }
        
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.theme["bg"], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        logo_label = tk.Label(
            header_frame, 
            text="🗜️", 
            font=("Arial", 30),
            bg=self.theme["bg"],
            fg=self.theme["highlight"]
        )
        logo_label.pack(side=tk.LEFT, padx=10)
        
        title_frame = tk.Frame(header_frame, bg=self.theme["bg"])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            title_frame,
            text="Byte Cruncher",
            font=("Arial", 24, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["highlight"]
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            title_frame,
            text="Advanced Huffman Compression Tool",
            font=("Arial", 12),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )
        subtitle_label.pack(anchor="w")
        
    def create_file_section(self):
        file_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        file_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            file_frame,
            text="Selected File:",
            font=("Arial", 12),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 12),
            bg=self.theme["bg"],
            fg=self.theme["warning"]
        )
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_btn = tk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file,
            bg=self.theme["button_bg"],
            fg=self.theme["button_fg"],
            font=("Arial", 10),
            padx=10,
            relief=tk.RAISED,
            borderwidth=1
        )
        self.browse_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_action_buttons(self):
        buttons_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Create a better looking button
        def create_button(text, command, icon, color):
            btn_frame = tk.Frame(buttons_frame, bg=self.theme["bg"])
            btn_frame.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
            
            btn = tk.Button(
                btn_frame,
                text=f"{icon} {text}",
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 12, "bold"),
                padx=15,
                pady=8,
                relief=tk.RAISED,
                borderwidth=1
            )
            btn.pack(fill=tk.X)
            return btn
        
        self.compress_btn = create_button("Compress", self.compress_file, "🗜️", self.theme["highlight"])
        self.decompress_btn = create_button("Decompress", self.decompress_file, "📂", "#9c27b0")
        self.download_btn = create_button("Save As", self.save_file, "💾", self.theme["success"])
        self.download_btn.config(state=tk.DISABLED)
        
    def create_result_section(self):
        result_frame = tk.Frame(self.main_frame, bg=self.theme["bg"], pady=10)
        result_frame.pack(fill=tk.X)
        
        # Status indicator
        self.status_frame = tk.Frame(result_frame, bg=self.theme["bg"], padx=10, pady=10)
        self.status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready for compression",
            font=("Arial", 12),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )
        self.status_label.pack(anchor="w")
        
        # Progress and stats
        self.stats_frame = tk.Frame(self.main_frame, bg=self.theme["bg"], padx=10, pady=5)
        self.stats_frame.pack(fill=tk.X)
        
        # Progress bar 
        self.progress = ttk.Progressbar(
            self.stats_frame, 
            orient="horizontal", 
            length=300, 
            mode="determinate"
        )
        self.progress.pack(pady=10, fill=tk.X)
        
        # Stats display
        self.stats_display = tk.Frame(self.stats_frame, bg=self.theme["bg"])
        self.stats_display.pack(fill=tk.X)
        
        # Original size
        size_frame = tk.Frame(self.stats_display, bg=self.theme["bg"])
        size_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            size_frame,
            text="Original Size:",
            font=("Arial", 10),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(anchor="w")
        
        self.original_size_label = tk.Label(
            size_frame,
            text="-- KB",
            font=("Arial", 12, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["highlight"]
        )
        self.original_size_label.pack(anchor="w")
        
        # Compressed size
        comp_frame = tk.Frame(self.stats_display, bg=self.theme["bg"])
        comp_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            comp_frame,
            text="Compressed Size:",
            font=("Arial", 10),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(anchor="w")
        
        self.compressed_size_label = tk.Label(
            comp_frame,
            text="-- KB",
            font=("Arial", 12, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["success"]
        )
        self.compressed_size_label.pack(anchor="w")
        
        # Ratio
        ratio_frame = tk.Frame(self.stats_display, bg=self.theme["bg"])
        ratio_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            ratio_frame,
            text="Compression Ratio:",
            font=("Arial", 10),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(anchor="w")
        
        self.ratio_label = tk.Label(
            ratio_frame,
            text="--%",
            font=("Arial", 12, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["warning"]
        )
        self.ratio_label.pack(anchor="w")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File", 
            filetypes=[
                ("Text files", "*.txt"), 
                ("Compressed files", "*.bin"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            
            # Check if it's likely a compressed file
            if file_path.endswith('.bin'):
                self.status_label.config(text="Ready for decompression")
                self.compress_btn.config(state=tk.DISABLED)
                self.decompress_btn.config(state=tk.NORMAL)
            else:
                self.status_label.config(text="Ready for compression")
                self.compress_btn.config(state=tk.NORMAL)
                self.decompress_btn.config(state=tk.DISABLED)
            
            self.download_btn.config(state=tk.DISABLED)
            self.reset_stats()

    def compress_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return
        
        # Generate temporary output path
        self.output_path = self.file_path.replace(".txt", "_compressed.bin")
        
        try:
            self.progress["value"] = 20
            self.root.update_idletasks()
            
            # Perform compression
            original_size, compressed_size = self.huffman.compress(self.file_path, self.output_path)
            
            self.progress["value"] = 100
            self.root.update_idletasks()
            
            # Calculate the ratio and sizes in KB
            ratio = round((compressed_size / original_size) * 100, 2)
            original_kb = round(original_size / 1024, 2)
            compressed_kb = round(compressed_size / 1024, 2)
            
            # Update stats
            self.original_size_label.config(text=f"{original_kb} KB ({original_size} bytes)")
            self.compressed_size_label.config(text=f"{compressed_kb} KB ({compressed_size} bytes)")
            self.ratio_label.config(text=f"{ratio}%")
            
            # Update status and enable download
            self.status_label.config(
                text="✅ Compression successful! Click 'Save As' to download.",
                fg=self.theme["success"]
            )
            self.download_btn.config(state=tk.NORMAL)
            self.is_compressed = True
            
        except Exception as e:
            self.progress["value"] = 0
            self.status_label.config(text=f"❌ Error: {str(e)}", fg=self.theme["error"])
            messagebox.showerror("Compression Error", str(e))

    def decompress_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return
        
        # Generate temporary output path
        self.output_path = self.file_path.replace("_compressed.bin", "_decompressed.txt")
        if self.output_path == self.file_path:  # In case the file doesn't follow naming convention
            self.output_path = os.path.splitext(self.file_path)[0] + "_decompressed.txt"
        
        try:
            self.progress["value"] = 20
            self.root.update_idletasks()
            
            # Perform decompression
            decompressed_size = self.huffman.decompress(self.file_path, self.output_path)
            
            self.progress["value"] = 100
            self.root.update_idletasks()
            
            # Calculate sizes
            compressed_size = os.path.getsize(self.file_path)
            ratio = round((compressed_size / decompressed_size) * 100, 2) if decompressed_size > 0 else 0
            
            # Update stats
            self.original_size_label.config(text=f"{round(compressed_size/1024, 2)} KB (compressed)")
            self.compressed_size_label.config(text=f"{round(decompressed_size/1024, 2)} KB (decompressed)")
            self.ratio_label.config(text=f"{ratio}%")
            
            # Update status and enable download
            self.status_label.config(
                text="✅ Decompression successful! Click 'Save As' to download.",
                fg=self.theme["success"]
            )
            self.download_btn.config(state=tk.NORMAL)
            self.is_compressed = False
            
        except Exception as e:
            self.progress["value"] = 0
            self.status_label.config(text=f"❌ Error: {str(e)}", fg=self.theme["error"])
            messagebox.showerror("Decompression Error", str(e))

    def save_file(self):
        if not self.output_path or not os.path.exists(self.output_path):
            messagebox.showerror("Error", "No output file to save.")
            return
        
        file_types = [("Compressed files", "*.bin")] if self.is_compressed else [("Text files", "*.txt")]
        default_ext = ".bin" if self.is_compressed else ".txt"
        
        save_path = filedialog.asksaveasfilename(
            title="Save File As",
            filetypes=file_types,
            defaultextension=default_ext,
            initialfile=os.path.basename(self.output_path)
        )
        
        if save_path:
            try:
                # Copy the file to the new location
                with open(self.output_path, 'rb') as src_file:
                    data = src_file.read()
                    
                with open(save_path, 'wb') as dst_file:
                    dst_file.write(data)
                
                messagebox.showinfo("Success", f"File saved successfully to:\n{save_path}")
                
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def reset_stats(self):
        self.original_size_label.config(text="-- KB")
        self.compressed_size_label.config(text="-- KB")
        self.ratio_label.config(text="--%")
        self.progress["value"] = 0

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = ByteCruncherApp(root)
    root.mainloop()