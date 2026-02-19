"""
CTools Design System - Professional Theme

Color Palette:
- Primary (Dark Navy): #0f2242
- Primary Light: #1d2e4c
- Accent (Orange): #ef8a18
- Background: #f8f9fa
- Surface: #ffffff
- Text Primary: #1a1a2e
- Text Secondary: #6c757d
- Border: #dee2e6
- Success: #28a745
- Error: #dc3545
"""

# Color Palette
COLORS = {
    'primary': '#0f2242',
    'primary_light': '#1d2e4c',
    'primary_hover': '#162d52',
    'accent': '#ef8a18',
    'accent_hover': '#d67a14',
    'background': '#f8f9fa',
    'surface': '#ffffff',
    'surface_alt': '#f1f3f4',
    'text_primary': '#1a1a2e',
    'text_secondary': '#6c757d',
    'text_light': '#ffffff',
    'border': '#dee2e6',
    'border_light': '#e9ecef',
    'success': '#28a745',
    'error': '#dc3545',
    'warning': '#ffc107',
}

# Typography
FONTS = {
    'family': 'Segoe UI, Arial, sans-serif',
    'size_xs': '11px',
    'size_sm': '12px',
    'size_base': '14px',
    'size_lg': '16px',
    'size_xl': '20px',
    'size_2xl': '24px',
    'size_3xl': '32px',
    'weight_normal': '400',
    'weight_medium': '500',
    'weight_semibold': '600',
    'weight_bold': '700',
}

# Spacing
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
    '2xl': '48px',
}

# Dimensions
DIMENSIONS = {
    'sidebar_width': 280,
    'sidebar_collapsed': 70,
    'header_height': 60,
    'input_height': 44,
    'button_height': 44,
    'border_radius': '8px',
    'border_radius_sm': '4px',
    'border_radius_lg': '12px',
}

# Main Application Stylesheet
APP_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}

/* Sidebar */
#sidebar {{
    background-color: {COLORS['primary']};
    border: none;
}}

#sidebar_header {{
    background-color: {COLORS['primary']};
    padding: 20px;
}}

#app_title {{
    color: {COLORS['text_light']};
    font-size: {FONTS['size_xl']};
    font-weight: {FONTS['weight_bold']};
}}

#app_subtitle {{
    color: {COLORS['accent']};
    font-size: {FONTS['size_sm']};
    font-weight: {FONTS['weight_medium']};
}}

/* Navigation Buttons */
.nav_button {{
    background-color: transparent;
    border: none;
    border-radius: {DIMENSIONS['border_radius']};
    color: rgba(255, 255, 255, 0.7);
    font-size: {FONTS['size_base']};
    font-weight: {FONTS['weight_medium']};
    padding: 12px 16px;
    text-align: left;
}}

.nav_button:hover {{
    background-color: {COLORS['primary_light']};
    color: {COLORS['text_light']};
}}

.nav_button:checked {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_light']};
}}

/* Section Headers in Sidebar */
.nav_section {{
    color: rgba(255, 255, 255, 0.5);
    font-size: {FONTS['size_xs']};
    font-weight: {FONTS['weight_semibold']};
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 16px 16px 8px 16px;
}}

/* Main Content Area */
#content_area {{
    background-color: {COLORS['background']};
}}

#content_header {{
    background-color: {COLORS['surface']};
    border-bottom: 1px solid {COLORS['border']};
    padding: 20px 32px;
}}

#page_title {{
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_2xl']};
    font-weight: {FONTS['weight_bold']};
}}

#page_description {{
    color: {COLORS['text_secondary']};
    font-size: {FONTS['size_base']};
    margin-top: 4px;
}}

/* Cards */
.card {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius_lg']};
    padding: 24px;
}}

.card_title {{
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_lg']};
    font-weight: {FONTS['weight_semibold']};
    margin-bottom: 16px;
}}

/* Form Elements */
QLabel {{
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_sm']};
    font-weight: {FONTS['weight_medium']};
}}

QLineEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius_sm']};
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_base']};
    padding: 10px 12px;
    min-height: 24px;
}}

QLineEdit:focus {{
    border-color: {COLORS['accent']};
    outline: none;
}}

QLineEdit:disabled {{
    background-color: {COLORS['surface_alt']};
    color: {COLORS['text_secondary']};
}}

QTextEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius_sm']};
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_sm']};
    font-family: 'Consolas', 'Monaco', monospace;
    padding: 12px;
}}

QCheckBox {{
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_base']};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['surface']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

/* Primary Button */
.btn_primary {{
    background-color: {COLORS['accent']};
    border: none;
    border-radius: {DIMENSIONS['border_radius']};
    color: {COLORS['text_light']};
    font-size: {FONTS['size_base']};
    font-weight: {FONTS['weight_semibold']};
    padding: 12px 24px;
    min-height: 20px;
}}

.btn_primary:hover {{
    background-color: {COLORS['accent_hover']};
}}

.btn_primary:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

/* Secondary Button */
.btn_secondary {{
    background-color: transparent;
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']};
    color: {COLORS['text_primary']};
    font-size: {FONTS['size_base']};
    font-weight: {FONTS['weight_medium']};
    padding: 12px 24px;
    min-height: 20px;
}}

.btn_secondary:hover {{
    background-color: {COLORS['surface_alt']};
    border-color: {COLORS['text_secondary']};
}}

/* Output/Console Area */
#output_area {{
    background-color: {COLORS['primary']};
    border-radius: {DIMENSIONS['border_radius']};
    color: {COLORS['text_light']};
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: {FONTS['size_sm']};
    padding: 16px;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {COLORS['surface_alt']};
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 4px;
    min-height: 40px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_secondary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {COLORS['surface_alt']};
    height: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 4px;
    min-width: 40px;
}}

/* Status indicators */
.status_success {{
    color: {COLORS['success']};
}}

.status_error {{
    color: {COLORS['error']};
}}

.status_warning {{
    color: {COLORS['warning']};
}}
"""
