def resume_text_to_latex(resume_text: str) -> str:
    def escape_latex(text: str) -> str:
        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "\\": r"\textbackslash{}",
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    escaped = escape_latex(resume_text)

    latex_body = escaped.replace("\n", r"\\")

    latex = f"""
\\documentclass[11pt]{{article}}
\\usepackage[a4paper,margin=1in]{{geometry}}
\\usepackage{{enumitem}}
\\pagenumbering{{gobble}}

\\begin{{document}}

{latex_body}

\\end{{document}}
""".strip()

    return latex
