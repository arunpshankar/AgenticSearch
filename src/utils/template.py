from pathlib import Path
from typing import Dict

# src/utils/template_loader.py

class TemplateLoader:
    def __init__(self, template_dir: str = "./templates/ui"):
        self.template_dir = Path(template_dir)
        self.templates: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        if not self.template_dir.exists():
            self.template_dir.mkdir(parents=True)
            
        for template_file in self.template_dir.glob("*.html"):
            with open(template_file, "r", encoding="utf-8") as f:
                template_name = template_file.stem
                # Extract only the CSS content between <style> tags
                content = f.read()
                css_start = content.find("<style>") + 7
                css_end = content.find("</style>")
                if css_start >= 7 and css_end != -1:
                    self.templates[template_name] = content[css_start:css_end].strip()

    def get_template(self, name: str) -> str:
        return f"<style>{self.templates.get(name, '')}</style>"

    def get_combined_styles(self) -> str:
        all_styles = "\n".join(self.templates.values())
        return f"<style>{all_styles}</style>"