from pathlib import Path
from typing import Dict

class TemplateLoader:
    """
    Loads HTML templates from a directory and extracts CSS styles.

    Attributes:
        template_dir (Path): The directory containing the HTML templates.
        templates (Dict[str, str]): A dictionary mapping template names to their CSS content.
    """

    def __init__(self, template_dir: str = "./templates/ui"):
        """
        Initializes the TemplateLoader with a given template directory.

        Args:
            template_dir (str): The path to the directory containing HTML templates. 
                                 Defaults to "./templates/ui".
        """
        self.template_dir = Path(template_dir)
        self.templates: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """
        Loads all HTML templates from the template directory and extracts CSS styles.
        Creates the template directory if it doesn't exist.
        """
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
        """
        Retrieves the CSS styles for a given template name.

        Args:
            name (str): The name of the template.

        Returns:
            str: The CSS styles wrapped in <style> tags, or an empty string if the template is not found.
        """
        return f"<style>{self.templates.get(name, '')}</style>"

    def get_combined_styles(self) -> str:
        """
        Combines the CSS styles from all templates.

        Returns:
            str: All CSS styles combined and wrapped in <style> tags.
        """
        all_styles = "\n".join(self.templates.values())
        return f"<style>{all_styles}</style>"