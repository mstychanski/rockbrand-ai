from typing import List

class Guardrails:
    def __init__(self):
        # Przykładowe zasady do sprawdzenia tekstów
        self.forbidden_words = {"drugs", "violence", "hate", "racism"}
        self.required_keywords = {"rock", "band", "music"}
        self.max_length = 300  # maksymalna długość tekstu
        
    def check_forbidden(self, text: str) -> bool:
        """Sprawdza czy tekst zawiera zabronione słowa."""
        lowered = text.lower()
        for word in self.forbidden_words:
            if word in lowered:
                return False
        return True
    
    def check_required_keywords(self, text: str) -> bool:
        """Sprawdza czy tekst zawiera wymagane słowa kluczowe."""
        lowered = text.lower()
        return any(keyword in lowered for keyword in self.required_keywords)
    
    def check_length(self, text: str) -> bool:
        """Sprawdza czy tekst nie przekracza maksymalnej długości."""
        return len(text) <= self.max_length
    
    def validate_text(self, text: str) -> List[str]:
        """Zwraca listę błędów, jeśli są, lub pustą listę jeśli tekst jest OK."""
        errors = []
        if not self.check_forbidden(text):
            errors.append("Tekst zawiera zabronione słowa.")
        if not self.check_required_keywords(text):
            errors.append("Tekst powinien zawierać słowa związane z muzyką lub zespołem.")
        if not self.check_length(text):
            errors.append(f"Tekst jest zbyt długi (max {self.max_length} znaków).")
        return errors

if __name__ == "__main__":
    gr = Guardrails()
    test_text = "This is a rock band promo text with no hate or drugs."
    result = gr.validate_text(test_text)
    if result:
        print("Błędy w tekście:", result)
    else:
        print("Tekst przeszedł walidację.")