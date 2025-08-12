"""PDF generation utilities for the Varroa detector project."""

import os
from matplotlib.backends.backend_pdf import PdfPages


class PDFGenerator:
    """Handles PDF generation from matplotlib figures."""
    
    def __init__(self):
        pass
    
    def create_recording_pdf(self, figures, output_path):
        """Create a PDF with multiple figures."""
        # Guard clause
        if not figures:
            raise ValueError("No figures provided for PDF generation")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with PdfPages(output_path) as pdf:
            for fig in figures:
                if fig is not None:
                    pdf.savefig(fig)
        
        print(f"PDF successfully saved to: {output_path}")
    
    def save_single_figure_pdf(self, figure, output_path):
        """Save a single figure to PDF."""
        if figure is None:
            raise ValueError("No figure provided for PDF generation")
        
        self.create_recording_pdf([figure], output_path)
