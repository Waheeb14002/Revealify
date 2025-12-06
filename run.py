from app.converter import SlideConverter
import os

def main():
    pptx_path = "example.pptx" # replace with your file path
    if not os.path.exists(pptx_path):
        print(f"Error: '{pptx_path}' not found.")
        return
    try:
        converter = SlideConverter(pptx_path)  
        converter.convert()
        converter.save("slides.html")
        print("Slides converted and saved.")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
