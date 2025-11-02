import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import binascii

class ZayuEncoder:
    def __init__(self):
        # 编码表
        self.charset = "可是杂鱼哦🥵♥~"
        self.char_to_index = {char: idx for idx, char in enumerate(self.charset)}
    
    def encode(self, text):
        """将文本编码为杂鱼编码"""
        try:
            # 将文本转换为UTF-8字节
            utf8_bytes = text.encode('utf-8')
            binary_str = ''.join(f'{byte:08b}' for byte in utf8_bytes)
            
            # 填充到3的倍数
            padding_bits = (3 - len(binary_str) % 3) % 3
            binary_str += '0' * padding_bits
            
            # 每3位一组进行编码
            encoded_chars = []
            for i in range(0, len(binary_str), 3):
                chunk = binary_str[i:i+3]
                index = int(chunk, 2)
                encoded_chars.append(self.charset[index])
            
            # 添加填充标识
            if padding_bits == 1:
                encoded_chars.append('~')
            elif padding_bits == 2:
                encoded_chars.append('~~')
            
            return ''.join(encoded_chars)
            
        except Exception as e:
            raise Exception(f"编码失败: {str(e)}")
    
    def decode(self, encoded_text):
        """将杂鱼编码解码为原始文本"""
        try:
            # 检查并移除填充
            padding_count = 0
            if encoded_text.endswith('~~'):
                padding_count = 2
                encoded_text = encoded_text[:-2]
            elif encoded_text.endswith('~'):
                padding_count = 1
                encoded_text = encoded_text[:-1]
            
            # 转换为二进制字符串
            binary_str = ''
            for char in encoded_text:
                if char not in self.char_to_index:
                    raise ValueError(f"无效字符: {char}")
                index = self.char_to_index[char]
                binary_str += f'{index:03b}'
            
            # 移除填充位
            if padding_count > 0:
                binary_str = binary_str[:-padding_count * 2]  # 每个填充位对应2个0
            
            # 将二进制转换为字节
            bytes_list = []
            for i in range(0, len(binary_str), 8):
                if i + 8 <= len(binary_str):
                    byte_chunk = binary_str[i:i+8]
                    bytes_list.append(int(byte_chunk, 2))
            
            # 解码为UTF-8文本
            decoded_bytes = bytes(bytes_list)
            return decoded_bytes.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"解码失败: {str(e)}")

class ZayuEncoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("杂鱼编码器 - 可是杂鱼哦🥵♥~")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.encoder = ZayuEncoder()
        
        self.setup_ui()
    
    def setup_ui(self):
        # 标题
        title_label = tk.Label(
            self.root, 
            text="杂鱼编码器", 
            font=("Microsoft YaHei", 20, "bold"),
            fg="#ff6b6b",
            bg='#f0f0f0'
        )
        title_label.pack(pady=20)
        
        # 字符集显示
        charset_label = tk.Label(
            self.root,
            text=f"编码字符集: {self.encoder.charset}",
            font=("Microsoft YaHei", 12),
            bg='#f0f0f0',
            fg="#333"
        )
        charset_label.pack(pady=5)
        
        # 创建选项卡
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 加密选项卡
        encrypt_frame = ttk.Frame(notebook)
        notebook.add(encrypt_frame, text="加密")
        self.setup_encrypt_tab(encrypt_frame)
        
        # 解密选项卡
        decrypt_frame = ttk.Frame(notebook)
        notebook.add(decrypt_frame, text="解密")
        self.setup_decrypt_tab(decrypt_frame)
        
        # 关于信息
        about_text = """使用说明:
• 加密: 输入任何文本(支持中文)，点击加密按钮
• 解密: 输入杂鱼编码，点击解密按钮
• 字符集: 可是杂鱼哦🥵♥~
• 原理: 基于Base64思想的Base8编码"""
        
        about_label = tk.Label(
            self.root,
            text=about_text,
            font=("Microsoft YaHei", 9),
            bg='#f0f0f0',
            fg="#666",
            justify=tk.LEFT
        )
        about_label.pack(pady=10)
    
    def setup_encrypt_tab(self, parent):
        # 输入标签
        input_label = tk.Label(
            parent,
            text="输入原文:",
            font=("Microsoft YaHei", 11, "bold"),
            bg='#f0f0f0'
        )
        input_label.pack(anchor='w', pady=(10, 5), padx=20)
        
        # 输入文本框
        self.input_text = scrolledtext.ScrolledText(
            parent,
            height=8,
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD
        )
        self.input_text.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # 加密按钮
        encrypt_btn = tk.Button(
            parent,
            text="加密 🔒",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.encrypt_text,
            relief='flat',
            padx=20,
            pady=10
        )
        encrypt_btn.pack(pady=10)
        
        # 输出标签
        output_label = tk.Label(
            parent,
            text="杂鱼编码结果:",
            font=("Microsoft YaHei", 11, "bold"),
            bg='#f0f0f0'
        )
        output_label.pack(anchor='w', pady=(10, 5), padx=20)
        
        # 输出文本框
        self.output_encoded = scrolledtext.ScrolledText(
            parent,
            height=8,
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD,
            bg='#f8f8f8'
        )
        self.output_encoded.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # 复制按钮
        copy_btn = tk.Button(
            parent,
            text="复制结果 📋",
            font=("Microsoft YaHei", 10),
            bg="#2196F3",
            fg="white",
            command=self.copy_encoded,
            relief='flat'
        )
        copy_btn.pack(pady=5)
    
    def setup_decrypt_tab(self, parent):
        # 输入标签
        input_label = tk.Label(
            parent,
            text="输入杂鱼编码:",
            font=("Microsoft YaHei", 11, "bold"),
            bg='#f0f0f0'
        )
        input_label.pack(anchor='w', pady=(10, 5), padx=20)
        
        # 输入文本框
        self.encoded_input = scrolledtext.ScrolledText(
            parent,
            height=8,
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD
        )
        self.encoded_input.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # 解密按钮
        decrypt_btn = tk.Button(
            parent,
            text="解密 🔓",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.decrypt_text,
            relief='flat',
            padx=20,
            pady=10
        )
        decrypt_btn.pack(pady=10)
        
        # 输出标签
        output_label = tk.Label(
            parent,
            text="解码结果:",
            font=("Microsoft YaHei", 11, "bold"),
            bg='#f0f0f0'
        )
        output_label.pack(anchor='w', pady=(10, 5), padx=20)
        
        # 输出文本框
        self.output_decoded = scrolledtext.ScrolledText(
            parent,
            height=8,
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD,
            bg='#f8f8f8'
        )
        self.output_decoded.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # 复制按钮
        copy_btn = tk.Button(
            parent,
            text="复制结果 📋",
            font=("Microsoft YaHei", 10),
            bg="#2196F3",
            fg="white",
            command=self.copy_decoded,
            relief='flat'
        )
        copy_btn.pack(pady=5)
    
    def encrypt_text(self):
        """加密文本"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入要加密的文本")
            return
        
        try:
            encoded_result = self.encoder.encode(input_text)
            self.output_encoded.delete("1.0", tk.END)
            self.output_encoded.insert("1.0", encoded_result)
            
            # 显示统计信息
            original_len = len(input_text)
            encoded_len = len(encoded_result)
            messagebox.showinfo("加密成功", 
                              f"加密完成！\n"
                              f"原文长度: {original_len} 字符\n"
                              f"编码长度: {encoded_len} 字符\n"
                              f"膨胀率: {encoded_len/original_len:.2f}x")
                              
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def decrypt_text(self):
        """解密文本"""
        encoded_text = self.encoded_input.get("1.0", tk.END).strip()
        if not encoded_text:
            messagebox.showwarning("警告", "请输入要解密的杂鱼编码")
            return
        
        try:
            decoded_result = self.encoder.decode(encoded_text)
            self.output_decoded.delete("1.0", tk.END)
            self.output_decoded.insert("1.0", decoded_result)
            messagebox.showinfo("解密成功", "解码完成！")
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def copy_encoded(self):
        """复制加密结果"""
        encoded_text = self.output_encoded.get("1.0", tk.END).strip()
        if encoded_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(encoded_text)
            messagebox.showinfo("成功", "已复制到剪贴板")
    
    def copy_decoded(self):
        """复制解密结果"""
        decoded_text = self.output_decoded.get("1.0", tk.END).strip()
        if decoded_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(decoded_text)
            messagebox.showinfo("成功", "已复制到剪贴板")

def main():
    root = tk.Tk()
    app = ZayuEncoderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()