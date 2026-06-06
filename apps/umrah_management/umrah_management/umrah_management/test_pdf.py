import pypdf
import os
import frappe

def run():
    bench_path = frappe.utils.get_bench_path()
    pdf_path = os.path.join(bench_path, "payment vouchers", "IICC - Payment Voucher 19-25.pdf")
    
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Bench Path: {bench_path}")
    print(f"Looking for PDF at: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print("File not found!")
        return
        
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total Pages: {len(reader.pages)}")
    for i, page in enumerate(reader.pages):
        print(f"\n--- PAGE {i+1} ---")
        print(page.extract_text()[:1500])
