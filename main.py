import sys
from pydantic import ValidationError
from LangTranslate import LangTranslateAPIWrapper, LangTranslateRun, InvalidLanguageCodeError
from rich import print
from difflib import get_close_matches

LANG_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Swedish": "sv",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Turkish": "tr",
    "Hebrew": "he",
    "Greek": "el",
    "Hindi": "hi",
    "Thai": "th",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Polish": "pl",
    "Czech": "cs",
    "Danish": "da",
    "Finnish": "fi",
    "Hungarian": "hu",
    "Romanian": "ro",
    "Ukrainian": "uk",
}

def suggest_language(lang_name):
    suggestions = get_close_matches(lang_name, LANG_CODES.keys(), n=3, cutoff=0.6)
    if suggestions:
        print("[bold yellow]Did you mean one of these languages?[/bold yellow]")
        for lang in suggestions:
            print(f"  - {lang}")
    else:
        print("[bold red]No similar languages found.[/bold red]")

def show_menu():
    print("\n[bold cyan]Menu:[/bold cyan]")
    print("  [bold green]0[/bold green] - Home")
    print("  [bold green]1[/bold green] - Set Language")
    print("Type 'exit' to quit\n")

def main():
    print("[bold blue]Welcome to LangTranslate![/bold blue]")
    print("This tool translates text from one language to another using the Translator library.")
    
    while True:
        show_menu()
        choice = input("Please choose an option: ").strip()

        if choice == "0":
            continue
        elif choice == "1":
            while True:
                lang_name = input("Enter the name of the language you want to translate to: ").strip()
                lang_name = lang_name.title()  # Capitalize the first letter of each word in the input
                lang_code = LANG_CODES.get(lang_name, None)

                if lang_code is None:
                    print("[bold red]Error: Language not found. Please try again.[/bold red]")
                    suggest_language(lang_name)
                else:
                    break
                
            api_wrapper = LangTranslateAPIWrapper(output_lang=lang_code)
            tool = LangTranslateRun(api_wrapper=api_wrapper)

            while True:
                input_text = input("Enter the text you want to translate or type 'back' to return to the menu: ").strip()
                if input_text.lower() == "back":
                    break
                
                try:
                    translated_text = tool.run(input_text)
                    print(translated_text)
                except InvalidLanguageCodeError as e:
                    print(str(e))
        elif choice.lower() == "exit":
            break
        else:
            print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == "__main__":
    main()
