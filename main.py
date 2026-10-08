import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from datetime import datetime


# ============================================================
# APPLICATION SETTINGS
# ============================================================

root = tk.Tk()
root.title("Secure File Transfer Simulator")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = min(1100, screen_width - 80)
window_height = min(850, screen_height - 100)

root.geometry(f"{window_width}x{window_height}")
root.minsize(800, 600)

is_maximized = False


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#F4F6F8"
CARD_COLOR = "#FFFFFF"

HEADER_COLOR = "#172B4D"

TEXT_COLOR = "#172B4D"
SECONDARY_TEXT = "#667085"

BORDER_COLOR = "#D9DEE7"

BUTTON_COLOR = "#2563EB"
BUTTON_HOVER = "#1D4ED8"

SUCCESS_COLOR = "#15803D"
DANGER_COLOR = "#DC2626"

FTP_COLOR = "#DC2626"
SFTP_COLOR = "#15803D"
SCP_COLOR = "#2563EB"


# ============================================================
# VARIABLES
# ============================================================

selected_file = tk.StringVar()
protocol = tk.StringVar(value="FTP")


# ============================================================
# PROTOCOL INFORMATION
# ============================================================

protocol_info = {

    "FTP": {
        "encryption": "NO",
        "security": "LOW",
        "description":
            "FTP does not encrypt data or credentials by default.",
        "color": FTP_COLOR
    },

    "SFTP": {
        "encryption": "YES",
        "security": "HIGH",
        "description":
            "SFTP provides secure file transfer through SSH.",
        "color": SFTP_COLOR
    },

    "SCP": {
        "encryption": "YES",
        "security": "HIGH",
        "description":
            "SCP securely copies files using SSH.",
        "color": SCP_COLOR
    }
}


# ============================================================
# TKINTER STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Treeview",
    background="white",
    foreground=TEXT_COLOR,
    rowheight=35,
    fieldbackground="white",
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=HEADER_COLOR,
    foreground="white",
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Treeview",
    background=[
        ("selected", "#DCE8FF")
    ],
    foreground=[
        ("selected", TEXT_COLOR)
    ]
)


# ============================================================
# CREATE SCROLLABLE WINDOW
# ============================================================

def create_scrollable_window(
    parent,
    title,
    width=1000,
    height=700
):

    window = tk.Toplevel(parent)

    window.title(title)

    window.geometry(
        f"{width}x{height}"
    )

    window.minsize(
        750,
        500
    )

    window.configure(
        bg=BG_COLOR
    )

    window.transient(parent)
    window.lift()
    window.focus_force()

    # Canvas
    canvas = tk.Canvas(
        window,
        bg=BG_COLOR,
        highlightthickness=0
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        window,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    # Scrollable frame
    frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    frame_window = canvas.create_window(
        (0, 0),
        window=frame,
        anchor="nw"
    )

    # Update scroll region
    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    frame.bind(
        "<Configure>",
        update_scroll_region
    )

    # Fit frame width
    def update_frame_width(event):

        canvas.itemconfig(
            frame_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        update_frame_width
    )

    # Mouse wheel
    def mouse_wheel(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind(
        "<MouseWheel>",
        mouse_wheel
    )

    return window, frame


# ============================================================
# CREATE CARD
# ============================================================

def create_card(parent, title):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 10)
    )

    return card


# ============================================================
# MAXIMIZE / RESTORE
# ============================================================

def maximize_window():

    global is_maximized

    if not is_maximized:

        root.state("zoomed")

        is_maximized = True

        maximize_button.config(
            text="RESTORE"
        )

    else:

        root.state("normal")

        root.geometry(
            f"{window_width}x{window_height}"
        )

        is_maximized = False

        maximize_button.config(
            text="MAXIMIZE"
        )


# ============================================================
# SELECT FILE
# ============================================================

def select_file():

    file_path = filedialog.askopenfilename()

    if file_path:

        selected_file.set(
            file_path
        )


# ============================================================
# TRANSFER FILE
# ============================================================

def transfer_file():

    file_path = selected_file.get()

    if not file_path:

        messagebox.showwarning(
            "No File Selected",
            "Please select a file first."
        )

        return

    if not os.path.exists(file_path):

        messagebox.showerror(
            "File Error",
            "The selected file does not exist."
        )

        return

    selected_protocol = protocol.get()

    info = protocol_info[
        selected_protocol
    ]

    received_folder = os.path.join(
        os.getcwd(),
        "received"
    )

    os.makedirs(
        received_folder,
        exist_ok=True
    )

    original_name = os.path.basename(
        file_path
    )

    new_filename = (
        selected_protocol
        + "_"
        + original_name
    )

    destination = os.path.join(
        received_folder,
        new_filename
    )

    try:

        shutil.copy2(
            file_path,
            destination
        )

        file_size = os.path.getsize(
            file_path
        )

        time_now = datetime.now().strftime(
            "%H:%M:%S"
        )

        # Result
        result_text.delete(
            "1.0",
            tk.END
        )

        result_text.insert(
            tk.END,
            "TRANSFER SUCCESSFUL\n\n"
        )

        result_text.insert(
            tk.END,
            f"Protocol       : {selected_protocol}\n"
        )

        result_text.insert(
            tk.END,
            f"Encryption     : {info['encryption']}\n"
        )

        result_text.insert(
            tk.END,
            f"Security Level : {info['security']}\n"
        )

        result_text.insert(
            tk.END,
            f"File           : {original_name}\n"
        )

        result_text.insert(
            tk.END,
            f"File Size      : {file_size} bytes\n"
        )

        result_text.insert(
            tk.END,
            f"Saved Location : {destination}\n"
        )

        result_text.insert(
            tk.END,
            f"Time           : {time_now}\n\n"
        )

        result_text.insert(
            tk.END,
            "SECURITY INFORMATION\n"
        )

        result_text.insert(
            tk.END,
            "-----------------------------\n"
        )

        result_text.insert(
            tk.END,
            info["description"]
        )

        # History
        history_text.insert(
            tk.END,
            f"{time_now} | "
            f"{selected_protocol} | "
            f"{original_name} | "
            f"Encryption: {info['encryption']} | "
            f"Security: {info['security']} | SUCCESS\n"
        )

        history_text.see(
            tk.END
        )

        status_label.config(
            text="● Transfer completed successfully",
            fg=SUCCESS_COLOR
        )

        messagebox.showinfo(
            "Transfer Complete",
            f"{selected_protocol} simulation completed successfully."
        )

    except Exception as error:

        status_label.config(
            text="● Transfer failed",
            fg=DANGER_COLOR
        )

        messagebox.showerror(
            "Transfer Error",
            str(error)
        )


# ============================================================
# CLEAR
# ============================================================

def clear_data():

    selected_file.set("")

    protocol.set("FTP")

    result_text.delete(
        "1.0",
        tk.END
    )

    history_text.delete(
        "1.0",
        tk.END
    )

    status_label.config(
        text="● Ready for transfer",
        fg=SECONDARY_TEXT
    )


# ============================================================
# SECURITY COMPARISON
# ============================================================

def show_comparison():

    window, main = create_scrollable_window(
        root,
        "FTP vs SFTP vs SCP - Security Comparison",
        1000,
        700
    )

    header = tk.Frame(
        main,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="SECURITY COMPARISON",
        font=("Segoe UI", 22, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=(20, 3)
    )

    tk.Label(
        header,
        text="FTP  •  SFTP  •  SCP",
        font=("Segoe UI", 11, "bold"),
        bg=HEADER_COLOR,
        fg="#D9E2EC"
    ).pack(
        pady=(0, 20)
    )

    content = tk.Frame(
        main,
        bg=BG_COLOR
    )

    content.pack(
        fill="x",
        padx=30,
        pady=25
    )

    tk.Label(
        content,
        text="Protocol Comparison",
        font=("Segoe UI", 14, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        pady=(0, 10)
    )

    table_container = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    table_container.pack(
        fill="x"
    )

    columns = (
        "feature",
        "ftp",
        "sftp",
        "scp"
    )

    tree = ttk.Treeview(
        table_container,
        columns=columns,
        show="headings",
        height=9
    )

    tree.heading(
        "feature",
        text="Feature"
    )

    tree.heading(
        "ftp",
        text="FTP"
    )

    tree.heading(
        "sftp",
        text="SFTP"
    )

    tree.heading(
        "scp",
        text="SCP"
    )

    tree.column(
        "feature",
        width=260,
        anchor="w"
    )

    tree.column(
        "ftp",
        width=200,
        anchor="center"
    )

    tree.column(
        "sftp",
        width=200,
        anchor="center"
    )

    tree.column(
        "scp",
        width=200,
        anchor="center"
    )

    comparison_data = [

        ("Encryption", "NO", "YES", "YES"),

        ("Uses SSH", "NO", "YES", "YES"),

        ("Security Level", "LOW", "HIGH", "HIGH"),

        ("Authentication", "Basic", "SSH", "SSH"),

        ("Data Protection", "Low", "High", "High"),

        ("Sensitive Data", "Not Ideal", "Suitable", "Suitable"),

        ("Main Purpose",
         "File Transfer",
         "Secure Transfer",
         "Secure Copy"),

        ("Recommended", "NO", "YES", "YES")
    ]

    for row in comparison_data:

        tree.insert(
            "",
            "end",
            values=row
        )

    tree.pack(
        fill="x",
        padx=1,
        pady=1
    )

    explanation = tk.LabelFrame(
        content,
        text="Quick Explanation",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    explanation.pack(
        fill="x",
        pady=20
    )

    explanation_text = (
        "FTP\n"
        "Traditional FTP does not encrypt data or credentials "
        "by default, so it provides lower security.\n\n"

        "SFTP\n"
        "SFTP means SSH File Transfer Protocol. It uses SSH "
        "to provide encrypted and secure file transfer.\n\n"

        "SCP\n"
        "SCP uses SSH to securely copy files between systems "
        "using encrypted communication."
    )

    tk.Label(
        explanation,
        text=explanation_text,
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=850
    ).pack(
        fill="x"
    )

    tk.Button(
        content,
        text="CLOSE",
        font=("Segoe UI", 10, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        relief="flat",
        width=15,
        height=2,
        cursor="hand2",
        command=window.destroy
    ).pack(
        pady=10
    )


# ============================================================
# SECURITY ANALYSIS
# ============================================================

def show_security_analysis():

    window, main = create_scrollable_window(
        root,
        "Security Analysis",
        950,
        700
    )

    header = tk.Frame(
        main,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="SECURITY ANALYSIS",
        font=("Segoe UI", 22, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=(20, 3)
    )

    tk.Label(
        header,
        text="FTP vs SFTP vs SCP",
        font=("Segoe UI", 11),
        bg=HEADER_COLOR,
        fg="#D9E2EC"
    ).pack(
        pady=(0, 20)
    )

    content = tk.Frame(
        main,
        bg=BG_COLOR
    )

    content.pack(
        fill="x",
        padx=30,
        pady=25
    )

    score = tk.LabelFrame(
        content,
        text="Security Score",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    score.pack(
        fill="x"
    )

    score_data = [

        ("FTP", "2 / 10", "LOW SECURITY", FTP_COLOR),

        ("SFTP", "9 / 10", "HIGH SECURITY", SFTP_COLOR),

        ("SCP", "9 / 10", "HIGH SECURITY", SCP_COLOR)
    ]

    for name, value, level, color in score_data:

        row = tk.Frame(
            score,
            bg=CARD_COLOR
        )

        row.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            row,
            text=name,
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=color,
            width=12
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=level,
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=color
        ).pack(
            side="left"
        )

    detail = tk.LabelFrame(
        content,
        text="Detailed Analysis",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    detail.pack(
        fill="x",
        pady=15
    )

    detail_text = (
        "FTP\n"
        "• No encryption by default.\n"
        "• Credentials and data may be exposed.\n"
        "• Less suitable for sensitive information.\n\n"

        "SFTP\n"
        "• Uses SSH for secure communication.\n"
        "• Data is encrypted during transfer.\n"
        "• Suitable for sensitive information.\n\n"

        "SCP\n"
        "• Uses SSH for secure file copying.\n"
        "• Provides encrypted communication.\n"
        "• Suitable for secure file transfer."
    )

    tk.Label(
        detail,
        text=detail_text,
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=850
    ).pack(
        fill="x"
    )

    recommendation = tk.LabelFrame(
        content,
        text="Recommendation",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    recommendation.pack(
        fill="x"
    )

    tk.Label(
        recommendation,
        text=(
            "✓ Prefer SFTP or SCP for sensitive information.\n\n"
            "✗ Avoid traditional FTP when encryption is required."
        ),
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        justify="left",
        anchor="w"
    ).pack(
        fill="x"
    )

    tk.Label(
        content,
        text=(
            "Note: The security scores are illustrative scores "
            "used for this academic simulation."
        ),
        font=("Segoe UI", 9),
        bg=BG_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=15
    )

    tk.Button(
        content,
        text="CLOSE",
        font=("Segoe UI", 10, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        relief="flat",
        width=15,
        height=2,
        cursor="hand2",
        command=window.destroy
    ).pack(
        pady=10
    )


# ============================================================
# REAL-WORLD CASE STUDY
# ============================================================

def show_case_study():

    window, main = create_scrollable_window(
        root,
        "MOVEit 2023 Case Study",
        1000,
        750
    )

    header = tk.Frame(
        main,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="REAL-WORLD CASE STUDY",
        font=("Segoe UI", 21, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=(20, 3)
    )

    tk.Label(
        header,
        text="MOVEit Transfer Vulnerability - 2023",
        font=("Segoe UI", 11),
        bg=HEADER_COLOR,
        fg="#D9E2EC"
    ).pack(
        pady=(0, 20)
    )

    content = tk.Frame(
        main,
        bg=BG_COLOR
    )

    content.pack(
        fill="x",
        padx=30,
        pady=25
    )

    sections = [

        (
            "01  Incident",
            "In 2023, MOVEit Transfer, a managed file-transfer "
            "software product from Progress, was affected by a "
            "serious security vulnerability.\n\n"
            "The main vulnerability discussed in this case study "
            "was CVE-2023-34362."
        ),

        (
            "02  Vulnerability",
            "CVE-2023-34362 was an SQL injection vulnerability. "
            "It could allow an attacker to gain unauthorized "
            "access to the MOVEit Transfer database and "
            "information stored in the environment."
        ),

        (
            "03  Attack",
            "The CL0P ransomware group exploited the MOVEit "
            "vulnerability. Attackers targeted internet-facing "
            "MOVEit Transfer applications and used the "
            "vulnerability to gain unauthorized access and "
            "steal data."
        ),

        (
            "04  Impact",
            "• Sensitive information could be accessed.\n"
            "• Data could be stolen from affected systems.\n"
            "• Organizations had to investigate and patch "
            "vulnerable systems.\n"
            "• The incident highlighted the importance of "
            "secure file-transfer systems."
        ),

        (
            "05  Security Lesson",
            "• Use secure communication protocols.\n"
            "• Keep file-transfer software updated.\n"
            "• Apply security patches quickly.\n"
            "• Monitor logs and unusual activity.\n"
            "• Protect sensitive information during transfer."
        ),

        (
            "06  Connection With This Project",
            "Our project compares FTP, SFTP and SCP based on "
            "security features.\n\n"
            "FTP provides no encryption by default, while SFTP "
            "and SCP use SSH-based encrypted communication.\n\n"
            "The MOVEit case demonstrates why protecting file "
            "transfer systems and sensitive data is important."
        ),

        (
            "07  Important Note",
            "MOVEit Transfer is a managed file-transfer product. "
            "This case study relates to the broader security of "
            "file-transfer systems. It does not mean that MOVEit "
            "itself is FTP, SFTP or SCP."
        )
    ]

    for title, text in sections:

        card = create_card(
            content,
            title
        )

        card.pack(
            fill="x",
            pady=7
        )

        tk.Label(
            card,
            text=text,
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

    tk.Button(
        content,
        text="CLOSE",
        font=("Segoe UI", 10, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        relief="flat",
        width=15,
        height=2,
        cursor="hand2",
        command=window.destroy
    ).pack(
        pady=20
    )


# ============================================================
# RESULTS DASHBOARD
# ============================================================

def show_results_dashboard():

    window, main = create_scrollable_window(
        root,
        "Project Results Dashboard",
        1000,
        720
    )

    header = tk.Frame(
        main,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="PROJECT RESULTS DASHBOARD",
        font=("Segoe UI", 22, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=(20, 3)
    )

    tk.Label(
        header,
        text="Final Results - FTP vs SFTP vs SCP",
        font=("Segoe UI", 11),
        bg=HEADER_COLOR,
        fg="#D9E2EC"
    ).pack(
        pady=(0, 20)
    )

    content = tk.Frame(
        main,
        bg=BG_COLOR
    )

    content.pack(
        fill="x",
        padx=30,
        pady=25
    )

    tk.Label(
        content,
        text="Final Comparison Results",
        font=("Segoe UI", 14, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        pady=(0, 10)
    )

    table_container = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    table_container.pack(
        fill="x"
    )

    columns = (
        "parameter",
        "ftp",
        "sftp",
        "scp"
    )

    tree = ttk.Treeview(
        table_container,
        columns=columns,
        show="headings",
        height=9
    )

    tree.heading(
        "parameter",
        text="Parameter"
    )

    tree.heading(
        "ftp",
        text="FTP"
    )

    tree.heading(
        "sftp",
        text="SFTP"
    )

    tree.heading(
        "scp",
        text="SCP"
    )

    tree.column(
        "parameter",
        width=260,
        anchor="w"
    )

    tree.column(
        "ftp",
        width=200,
        anchor="center"
    )

    tree.column(
        "sftp",
        width=200,
        anchor="center"
    )

    tree.column(
        "scp",
        width=200,
        anchor="center"
    )

    results_data = [

        ("Encryption", "NO", "YES", "YES"),

        ("SSH Protection", "NO", "YES", "YES"),

        ("Security Score", "2 / 10", "9 / 10", "9 / 10"),

        ("Security Level", "LOW", "HIGH", "HIGH"),

        (
            "Sensitive Data",
            "Not Recommended",
            "Recommended",
            "Recommended"
        ),

        ("Authentication", "Basic", "SSH", "SSH"),

        ("Data Protection", "Low", "High", "High"),

        (
            "Overall Result",
            "Weak Security",
            "Strong Security",
            "Strong Security"
        )
    ]

    for row in results_data:

        tree.insert(
            "",
            "end",
            values=row
        )

    tree.pack(
        fill="x",
        padx=1,
        pady=1
    )

    finding = tk.LabelFrame(
        content,
        text="Main Finding",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    finding.pack(
        fill="x",
        pady=15
    )

    tk.Label(
        finding,
        text=(
            "FTP provides the lowest security because it does "
            "not encrypt data by default.\n\n"
            "SFTP and SCP provide stronger protection because "
            "they use SSH-based encrypted communication.\n\n"
            "Therefore, SFTP and SCP are more suitable for "
            "transferring sensitive information."
        ),
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=850
    ).pack(
        fill="x"
    )

    conclusion = tk.LabelFrame(
        content,
        text="Project Conclusion",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    conclusion.pack(
        fill="x",
        pady=5
    )

    tk.Label(
        conclusion,
        text=(
            "The simulation demonstrates that security is an "
            "important factor when selecting a file-transfer "
            "protocol.\n\n"
            "Traditional FTP should be avoided when encryption "
            "is required. SFTP and SCP provide better security "
            "through SSH-based protection."
        ),
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=850
    ).pack(
        fill="x"
    )

    recommendation = tk.LabelFrame(
        content,
        text="Final Recommendation",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=20,
        pady=15
    )

    recommendation.pack(
        fill="x",
        pady=15
    )

    tk.Label(
        recommendation,
        text=(
            "BEST CHOICE FOR SECURE FILE TRANSFER\n\n"
            "SFTP / SCP\n\n"
            "For sensitive information, use a secure protocol "
            "with encryption and strong authentication."
        ),
        font=("Segoe UI", 11, "bold"),
        bg=CARD_COLOR,
        fg=SUCCESS_COLOR,
        justify="left",
        anchor="w",
        wraplength=850
    ).pack(
        fill="x"
    )

    tk.Label(
        content,
        text=(
            "Note: This project is a local simulation. "
            "It demonstrates protocol security characteristics "
            "but does not establish real FTP, SFTP or SCP "
            "network connections."
        ),
        font=("Segoe UI", 9),
        bg=BG_COLOR,
        fg=SECONDARY_TEXT,
        wraplength=850,
        justify="center"
    ).pack(
        pady=5
    )

    tk.Button(
        content,
        text="CLOSE",
        font=("Segoe UI", 10, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        relief="flat",
        width=15,
        height=2,
        cursor="hand2",
        command=window.destroy
    ).pack(
        pady=15
    )


# ============================================================
# VISUAL TRANSFER SIMULATION
# ============================================================

def show_transfer_simulation():

    file_path = selected_file.get()

    if not file_path:

        messagebox.showwarning(
            "No File Selected",
            "Please select a file first."
        )

        return

    if not os.path.exists(file_path):

        messagebox.showerror(
            "File Error",
            "The selected file does not exist."
        )

        return

    selected_protocol = protocol.get()

    info = protocol_info[
        selected_protocol
    ]

    original_name = os.path.basename(
        file_path
    )

    simulation_window, main = create_scrollable_window(
        root,
        "File Transfer Simulation",
        1000,
        750
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header = tk.Frame(
        main,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="FILE TRANSFER SIMULATION",
        font=("Segoe UI", 22, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        header,
        text=f"{selected_protocol} Transfer Process",
        font=("Segoe UI", 11),
        bg=HEADER_COLOR,
        fg="#D9E2EC"
    ).pack(
        pady=(0, 20)
    )

    content = tk.Frame(
        main,
        bg=BG_COLOR
    )

    content.pack(
        fill="x",
        padx=30,
        pady=25
    )

    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    info_card = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    info_card.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        info_card,
        text="TRANSFER INFORMATION",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    tk.Label(
        info_card,
        text=f"Source File       : {original_name}",
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=2
    )

    tk.Label(
        info_card,
        text=f"Protocol          : {selected_protocol}",
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=2
    )

    tk.Label(
        info_card,
        text=f"Encryption        : {info['encryption']}",
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=2
    )

    tk.Label(
        info_card,
        text=f"Security Level    : {info['security']}",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=info["color"]
    ).pack(
        anchor="w",
        padx=20,
        pady=(2, 15)
    )

    # --------------------------------------------------------
    # VISUAL FLOW
    # --------------------------------------------------------

    flow_card = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    flow_card.pack(
        fill="x",
        pady=10
    )

    tk.Label(
        flow_card,
        text="TRANSFER FLOW",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(15, 5)
    )

    flow_canvas = tk.Canvas(
        flow_card,
        height=220,
        bg="#F8FAFC",
        highlightthickness=0
    )

    flow_canvas.pack(
        fill="x",
        padx=20,
        pady=15
    )

    source_x = 120
    protocol_x = 450
    destination_x = 780

    center_y = 90

    # Source
    flow_canvas.create_rectangle(
        source_x - 70,
        center_y - 40,
        source_x + 70,
        center_y + 40,
        fill="white",
        outline=HEADER_COLOR,
        width=2
    )

    flow_canvas.create_text(
        source_x,
        center_y - 12,
        text="SOURCE FILE",
        font=("Segoe UI", 10, "bold"),
        fill=TEXT_COLOR
    )

    flow_canvas.create_text(
        source_x,
        center_y + 12,
        text=original_name[:18],
        font=("Segoe UI", 9),
        fill=SECONDARY_TEXT
    )

    # Protocol
    flow_canvas.create_rectangle(
        protocol_x - 80,
        center_y - 40,
        protocol_x + 80,
        center_y + 40,
        fill="white",
        outline=info["color"],
        width=3
    )

    flow_canvas.create_text(
        protocol_x,
        center_y - 12,
        text=selected_protocol,
        font=("Segoe UI", 12, "bold"),
        fill=info["color"]
    )

    encryption_text = (
        "ENCRYPTED"
        if info["encryption"] == "YES"
        else "NOT ENCRYPTED"
    )

    flow_canvas.create_text(
        protocol_x,
        center_y + 14,
        text=encryption_text,
        font=("Segoe UI", 8, "bold"),
        fill=info["color"]
    )

    # Destination
    flow_canvas.create_rectangle(
        destination_x - 70,
        center_y - 40,
        destination_x + 70,
        center_y + 40,
        fill="white",
        outline=HEADER_COLOR,
        width=2
    )

    flow_canvas.create_text(
        destination_x,
        center_y - 12,
        text="RECEIVED",
        font=("Segoe UI", 10, "bold"),
        fill=TEXT_COLOR
    )

    flow_canvas.create_text(
        destination_x,
        center_y + 12,
        text="File Saved",
        font=("Segoe UI", 9),
        fill=SECONDARY_TEXT
    )

    # Arrows
    flow_canvas.create_line(
        source_x + 70,
        center_y,
        protocol_x - 80,
        center_y,
        arrow=tk.LAST,
        width=3,
        fill=HEADER_COLOR
    )

    flow_canvas.create_line(
        protocol_x + 80,
        center_y,
        destination_x - 70,
        center_y,
        arrow=tk.LAST,
        width=3,
        fill=HEADER_COLOR
    )

    packet_text = flow_canvas.create_text(
        450,
        165,
        text="Ready to transfer...",
        font=("Segoe UI", 10, "bold"),
        fill=TEXT_COLOR
    )

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    progress_card = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    progress_card.pack(
        fill="x",
        pady=10
    )

    tk.Label(
        progress_card,
        text="TRANSFER PROGRESS",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )

    progress_value = tk.DoubleVar(
        value=0
    )

    progress_bar = ttk.Progressbar(
        progress_card,
        variable=progress_value,
        maximum=100,
        mode="determinate"
    )

    progress_bar.pack(
        fill="x",
        padx=20,
        pady=5
    )

    progress_label = tk.Label(
        progress_card,
        text="0%",
        font=("Segoe UI", 11, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    progress_label.pack(
        pady=(5, 15)
    )

    # --------------------------------------------------------
    # ACTIVITY LOG
    # --------------------------------------------------------

    log_card = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    log_card.pack(
        fill="x",
        pady=10
    )

    tk.Label(
        log_card,
        text="SIMULATION ACTIVITY",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )

    log_frame = tk.Frame(
        log_card,
        bg=CARD_COLOR
    )

    log_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    log_scrollbar = ttk.Scrollbar(
        log_frame,
        orient="vertical"
    )

    log_scrollbar.pack(
        side="right",
        fill="y"
    )

    simulation_log = tk.Text(
        log_frame,
        height=8,
        font=("Consolas", 9),
        bg="#F8FAFC",
        fg=TEXT_COLOR,
        relief="flat",
        wrap="word",
        yscrollcommand=log_scrollbar.set
    )

    simulation_log.pack(
        side="left",
        fill="both",
        expand=True
    )

    log_scrollbar.config(
        command=simulation_log.yview
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = tk.Label(
        content,
        text="● Ready to start simulation",
        font=("Segoe UI", 11, "bold"),
        bg=BG_COLOR,
        fg=SECONDARY_TEXT
    )

    status.pack(
        pady=10
    )

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    current_progress = 0
    packet_position = source_x

    # --------------------------------------------------------
    # ADD LOG
    # --------------------------------------------------------

    def add_log(message):

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        simulation_log.insert(
            tk.END,
            f"[{current_time}] {message}\n"
        )

        simulation_log.see(
            tk.END
        )

    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------

    def animate():

        nonlocal current_progress
        nonlocal packet_position

        current_progress += 2

        progress_value.set(
            current_progress
        )

        progress_label.config(
            text=f"{current_progress}%"
        )

        packet_position += 8

        if packet_position > destination_x:

            packet_position = source_x

        flow_canvas.delete(
            "packet"
        )

        flow_canvas.create_oval(
            packet_position - 7,
            center_y - 7,
            packet_position + 7,
            center_y + 7,
            fill=info["color"],
            outline="",
            tags="packet"
        )

        if current_progress == 2:

            add_log(
                f"Starting {selected_protocol} transfer simulation."
            )

            add_log(
                f"Source file: {original_name}"
            )

        elif current_progress == 10:

            status.config(
                text="● Preparing file...",
                fg=BUTTON_COLOR
            )

            add_log(
                "File prepared for transfer."
            )

        elif current_progress == 30:

            status.config(
                text="● Sending data packets...",
                fg=BUTTON_COLOR
            )

            add_log(
                "Data packets are being simulated."
            )

        elif current_progress == 50:

            status.config(
                text="● Processing transfer...",
                fg=BUTTON_COLOR
            )

            if info["encryption"] == "YES":

                add_log(
                    "SSH-based encrypted communication simulated."
                )

            else:

                add_log(
                    "FTP transfer simulated without encryption."
                )

        elif current_progress == 70:

            status.config(
                text="● Transferring to destination...",
                fg=BUTTON_COLOR
            )

            add_log(
                "Data is moving toward destination."
            )

        elif current_progress == 90:

            status.config(
                text="● Finalizing transfer...",
                fg=BUTTON_COLOR
            )

            add_log(
                "Finalizing simulated transfer."
            )

        if current_progress >= 100:

            progress_value.set(
                100
            )

            progress_label.config(
                text="100%"
            )

            flow_canvas.delete(
                "packet"
            )

            flow_canvas.itemconfig(
                packet_text,
                text="✓ TRANSFER COMPLETED"
            )

            status.config(
                text="● Transfer simulation completed successfully",
                fg=SUCCESS_COLOR
            )

            add_log(
                "✓ Transfer completed successfully."
            )

            add_log(
                f"✓ Protocol: {selected_protocol}"
            )

            add_log(
                "✓ Simulation finished."
            )

            start_button.config(
                state="disabled",
                text="SIMULATION COMPLETE"
            )

            return

        flow_canvas.itemconfig(
            packet_text,
            text=f"Transferring data... {current_progress}%"
        )

        simulation_window.after(
            60,
            animate
        )

    # --------------------------------------------------------
    # START SIMULATION
    # --------------------------------------------------------

    def start_simulation():

        nonlocal current_progress
        nonlocal packet_position

        current_progress = 0

        packet_position = source_x

        progress_value.set(
            0
        )

        progress_label.config(
            text="0%"
        )

        simulation_log.delete(
            "1.0",
            tk.END
        )

        status.config(
            text="● Starting simulation...",
            fg=BUTTON_COLOR
        )

        flow_canvas.itemconfig(
            packet_text,
            text="Starting transfer..."
        )

        start_button.config(
            state="disabled",
            text="SIMULATION RUNNING..."
        )

        animate()

    # --------------------------------------------------------
    # START BUTTON
    # --------------------------------------------------------

    start_button = tk.Button(
        content,
        text="START SIMULATION",
        font=("Segoe UI", 11, "bold"),
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        width=22,
        height=2,
        cursor="hand2",
        command=start_simulation
    )

    start_button.pack(
        pady=10
    )

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    tk.Button(
        content,
        text="CLOSE",
        font=("Segoe UI", 10, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        relief="flat",
        width=15,
        height=2,
        cursor="hand2",
        command=simulation_window.destroy
    ).pack(
        pady=15
    )


# ============================================================
# MAIN WINDOW SCROLLBAR
# ============================================================

main_canvas = tk.Canvas(
    root,
    bg=BG_COLOR,
    highlightthickness=0
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

main_scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)

main_scrollbar.pack(
    side="right",
    fill="y"
)

main_canvas.configure(
    yscrollcommand=main_scrollbar.set
)


# ============================================================
# MAIN FRAME
# ============================================================

main_frame = tk.Frame(
    main_canvas,
    bg=BG_COLOR
)

main_frame_window = main_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


def configure_main_canvas(event):

    main_canvas.itemconfig(
        main_frame_window,
        width=event.width
    )

    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


main_canvas.bind(
    "<Configure>",
    configure_main_canvas
)


# ============================================================
# MAIN HEADER
# ============================================================

header = tk.Frame(
    main_frame,
    bg=HEADER_COLOR
)

header.pack(
    fill="x"
)

tk.Label(
    header,
    text="SECURE FILE TRANSFER",
    font=("Segoe UI", 26, "bold"),
    bg=HEADER_COLOR,
    fg="white"
).pack(
    pady=(25, 3)
)

tk.Label(
    header,
    text="FTP  •  SFTP  •  SCP",
    font=("Segoe UI", 13, "bold"),
    bg=HEADER_COLOR,
    fg="#D9E2EC"
).pack(
    pady=2
)

tk.Label(
    header,
    text="Comparative Security Analysis & Simulation",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#B8C7D9"
).pack(
    pady=(2, 25)
)


# ============================================================
# MAIN CONTENT
# ============================================================

content = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

content.pack(
    fill="x",
    padx=40,
    pady=25
)


# ============================================================
# FILE CARD
# ============================================================

file_card = create_card(
    content,
    "01  Select File"
)

file_card.pack(
    fill="x",
    pady=(0, 15)
)

file_row = tk.Frame(
    file_card,
    bg=CARD_COLOR
)

file_row.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

file_row.columnconfigure(
    0,
    weight=1
)

file_entry = tk.Entry(
    file_row,
    textvariable=selected_file,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT_COLOR,
    relief="solid",
    bd=1
)

file_entry.grid(
    row=0,
    column=0,
    sticky="ew",
    ipady=8,
    padx=(0, 12)
)

browse_button = tk.Button(
    file_row,
    text="BROWSE",
    font=("Segoe UI", 10, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=9,
    cursor="hand2",
    command=select_file
)

browse_button.grid(
    row=0,
    column=1
)


# ============================================================
# PROTOCOL CARD
# ============================================================

protocol_card = create_card(
    content,
    "02  Select Transfer Protocol"
)

protocol_card.pack(
    fill="x",
    pady=15
)

protocol_row = tk.Frame(
    protocol_card,
    bg=CARD_COLOR
)

protocol_row.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

for column in range(3):

    protocol_row.columnconfigure(
        column,
        weight=1
    )


def create_protocol_card(
    name,
    color,
    column
):

    card = tk.Frame(
        protocol_row,
        bg="#F8FAFC",
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=5
    )

    tk.Radiobutton(
        card,
        text=name,
        variable=protocol,
        value=name,
        font=("Segoe UI", 12, "bold"),
        bg="#F8FAFC",
        fg=color,
        activebackground="#F8FAFC",
        activeforeground=color,
        selectcolor="#E8EEF7",
        cursor="hand2"
    ).pack(
        pady=(15, 5)
    )

    tk.Label(
        card,
        text=(
            "LOW SECURITY"
            if name == "FTP"
            else "HIGH SECURITY"
        ),
        font=("Segoe UI", 8, "bold"),
        bg="#F8FAFC",
        fg=color
    ).pack(
        pady=(0, 15)
    )


create_protocol_card(
    "FTP",
    FTP_COLOR,
    0
)

create_protocol_card(
    "SFTP",
    SFTP_COLOR,
    1
)

create_protocol_card(
    "SCP",
    SCP_COLOR,
    2
)


# ============================================================
# TRANSFER BUTTON
# ============================================================

transfer_button = tk.Button(
    content,
    text="TRANSFER FILE",
    font=("Segoe UI", 12, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    padx=45,
    pady=12,
    cursor="hand2",
    command=transfer_file
)

transfer_button.pack(
    pady=15
)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    content,
    text="● Ready for transfer",
    font=("Segoe UI", 9, "bold"),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

status_label.pack(
    pady=(0, 15)
)


# ============================================================
# TRANSFER RESULT
# ============================================================

result_card = create_card(
    content,
    "03  Transfer Result"
)

result_card.pack(
    fill="x",
    pady=15
)

result_text = tk.Text(
    result_card,
    height=11,
    font=("Consolas", 10),
    bg="#F8FAFC",
    fg=TEXT_COLOR,
    relief="flat",
    wrap="word",
    padx=15,
    pady=15
)

result_text.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


# ============================================================
# HISTORY
# ============================================================

history_card = create_card(
    content,
    "04  Transfer History / Activity Log"
)

history_card.pack(
    fill="x",
    pady=15
)

history_scrollbar = ttk.Scrollbar(
    history_card,
    orient="vertical"
)

history_scrollbar.pack(
    side="right",
    fill="y",
    padx=(0, 20),
    pady=(0, 20)
)

history_text = tk.Text(
    history_card,
    height=7,
    font=("Consolas", 9),
    bg="#F8FAFC",
    fg=TEXT_COLOR,
    relief="flat",
    wrap="none",
    yscrollcommand=history_scrollbar.set
)

history_text.pack(
    fill="both",
    expand=True,
    padx=(20, 0),
    pady=(0, 20)
)

history_scrollbar.config(
    command=history_text.yview
)


# ============================================================
# SECURITY & ANALYSIS TOOLS
# ============================================================

tools_card = create_card(
    content,
    "05  Security & Analysis Tools"
)

tools_card.pack(
    fill="x",
    pady=15
)

tools_frame = tk.Frame(
    tools_card,
    bg=CARD_COLOR
)

tools_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

for column in range(2):

    tools_frame.columnconfigure(
        column,
        weight=1
    )


def create_tool_button(
    text,
    command,
    row,
    column
):

    button = tk.Button(
        tools_frame,
        text=text,
        font=("Segoe UI", 9, "bold"),
        bg="#EEF2F7",
        fg=TEXT_COLOR,
        activebackground="#DDE5EF",
        activeforeground=TEXT_COLOR,
        relief="flat",
        height=2,
        cursor="hand2",
        command=command
    )

    button.grid(
        row=row,
        column=column,
        sticky="ew",
        padx=5,
        pady=5
    )


create_tool_button(
    "SECURITY COMPARISON",
    show_comparison,
    0,
    0
)

create_tool_button(
    "SECURITY ANALYSIS",
    show_security_analysis,
    0,
    1
)

create_tool_button(
    "REAL-WORLD CASE STUDY",
    show_case_study,
    1,
    0
)

create_tool_button(
    "RESULTS DASHBOARD",
    show_results_dashboard,
    1,
    1
)

create_tool_button(
    "TRANSFER SIMULATION",
    show_transfer_simulation,
    2,
    0
)


# ============================================================
# CONTROL BUTTONS
# ============================================================

control_frame = tk.Frame(
    content,
    bg=BG_COLOR
)

control_frame.pack(
    pady=20
)

clear_button = tk.Button(
    control_frame,
    text="CLEAR",
    font=("Segoe UI", 9, "bold"),
    width=15,
    height=2,
    bg="#E5E7EB",
    fg=TEXT_COLOR,
    activebackground="#D1D5DB",
    relief="flat",
    cursor="hand2",
    command=clear_data
)

clear_button.grid(
    row=0,
    column=0,
    padx=5
)

maximize_button = tk.Button(
    control_frame,
    text="MAXIMIZE",
    font=("Segoe UI", 9, "bold"),
    width=15,
    height=2,
    bg="#E5E7EB",
    fg=TEXT_COLOR,
    activebackground="#D1D5DB",
    relief="flat",
    cursor="hand2",
    command=maximize_window
)

maximize_button.grid(
    row=0,
    column=1,
    padx=5
)

exit_button = tk.Button(
    control_frame,
    text="EXIT",
    font=("Segoe UI", 9, "bold"),
    width=15,
    height=2,
    bg="#FEE2E2",
    fg=DANGER_COLOR,
    activebackground="#FECACA",
    relief="flat",
    cursor="hand2",
    command=root.destroy
)

exit_button.grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# FOOTER
# ============================================================

tk.Label(
    content,
    text=(
        "Secure File Transfer Simulator  •  "
        "Python + Tkinter  •  Academic Microproject"
    ),
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(0, 25)
)


# ============================================================
# MAIN MOUSE WHEEL
# ============================================================

def main_mouse_wheel(event):

    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


main_canvas.bind(
    "<MouseWheel>",
    main_mouse_wheel
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()