from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# JavaScript functions for alignment, flexbox, and spacing consistency checks
js_code = """
function checkAlignmentCounts() {
    const elements = document.querySelectorAll('*');
    const alignmentCounts = { total: elements.length, left: 0, center: 0, right: 0 };

    elements.forEach(element => {
        const styles = window.getComputedStyle(element);
        const textAlign = styles.textAlign;

        if (textAlign === 'left' || textAlign === 'start') alignmentCounts.left += 1;
        else if (textAlign === 'center') alignmentCounts.center += 1;
        else if (textAlign === 'right' || textAlign === 'end') alignmentCounts.right += 1;
    });

    return alignmentCounts;
}

function checkFlexboxConsistency() {
    const elements = document.querySelectorAll('*');
    const flexboxCounts = { total: elements.length, matching: 0 };
    const flexboxValues = new Set();

    elements.forEach(element => {
        const styles = window.getComputedStyle(element);
        if (styles.display === 'flex') {
            const flexSettings = `${styles.justifyContent}-${styles.alignItems}`;
            flexboxValues.add(flexSettings);
        }
    });

    flexboxCounts.matching = flexboxValues.size === 1 ? elements.length : 0;
    return flexboxCounts;
}

function checkSpacingConsistency() {
    const elements = document.querySelectorAll('*');
    const spacingCounts = { total: elements.length, matching: 0 };
    const spacingValues = new Set();

    elements.forEach(element => {
        const styles = window.getComputedStyle(element);
        const margin = `${styles.marginTop}-${styles.marginRight}-${styles.marginBottom}-${styles.marginLeft}`;
        const padding = `${styles.paddingTop}-${styles.paddingRight}-${styles.paddingBottom}-${styles.paddingLeft}`;
        spacingValues.add(`${margin}-${padding}`);
    });

    spacingCounts.matching = spacingValues.size === 1 ? elements.length : 0;
    return spacingCounts;
}

function checkConsistency() {
    return {
        alignment: checkAlignmentCounts(),
        flexbox: checkFlexboxConsistency(),
        spacing: checkSpacingConsistency()
    };
}
checkConsistency();
"""

# Function to run JavaScript checks in the browser and retrieve results
async def run_js_consistency_checks(html_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch browser in headless mode
        page = await browser.new_page()

        # Load HTML content into the page
        await page.set_content(html_content)

        # Run JavaScript consistency checks and get the results
        consistency_report = await page.evaluate(js_code)

        await browser.close()  # Close browser after getting the results
        return consistency_report


# Font harmony calculation remains in Python
def evaluate_visual_harmony(font_families):
    serif_fonts = ['Times New Roman', 'Georgia', 'Garamond', 'Palatino', 'Book Antiqua']
    sans_serif_fonts = ['Arial', 'Helvetica', 'Verdana', 'Tahoma', 'Trebuchet MS']
    serif_count = sum(1 for font in font_families if any(serif in font for serif in serif_fonts))
    sans_serif_count = sum(1 for font in font_families if any(sans_serif in font for sans_serif in sans_serif_fonts))
    
    typeface_counts = {}
    for font in font_families:
        base_font = font.split(',')[0].strip()
        typeface_counts[base_font] = typeface_counts.get(base_font, 0) + 1
    
    harmony_score = min(serif_count, sans_serif_count) + sum(1 for count in typeface_counts.values() if count > 1)
    return harmony_score

def font_harmony(elements_properties):
    font_families = [properties.get("font-family") for _, properties in elements_properties.items() if properties.get("font-family")]
    return {"font_harmony_score": evaluate_visual_harmony(font_families)}

# Main function to generate the visual consistency report
async def visual_consistency_report(html_content, elements_properties):
    # Consistency checks from JavaScript
    js_checks = await run_js_consistency_checks(html_content)
    
    # Font harmony score from Python
    font_harmony_score = font_harmony(elements_properties).get("font_harmony_score", 0)

    total_elements = js_checks['alignment']['total']
    left_alignment_count = js_checks['alignment']['left']
    center_alignment_count = js_checks['alignment']['center']
    right_alignment_count = js_checks['alignment']['right']
    matching_flexbox = js_checks['flexbox']['matching']
    matching_spacing = js_checks['spacing']['matching']

    numerical_data = {
        "total_elements": {"title": "Total Elements", "value": total_elements},
        "left_alignment": {"title": "Left Alignment Count", "value": left_alignment_count},
        "center_alignment": {"title": "Center Alignment Count", "value": center_alignment_count},
        "right_alignment": {"title": "Right Alignment Count", "value": right_alignment_count},
        "matching_flexbox": {"title": "Matching Flexbox", "value": matching_flexbox},
        "matching_spacing": {"title": "Matching Spacing", "value": matching_spacing},
        "font_harmony_score": {"title": "Font Harmony Score", "value": font_harmony_score},
    }

    one_liner_data = [
        {"title": "Alignment Consistency", "details": f"Total elements checked: {total_elements}. Left aligned: {left_alignment_count}, Center aligned: {center_alignment_count}, Right aligned: {right_alignment_count}."},
        {"title": "Flexbox Consistency", "details": f"Number of elements with matching flexbox properties: {matching_flexbox}."},
        {"title": "Spacing Consistency", "details": f"Number of elements with matching spacing properties: {matching_spacing}."},
        {"title": "Font Harmony", "details": f"The overall font harmony score is {font_harmony_score}."},
    ]

    return {
        "alignment_counts": js_checks['alignment'],
        "flexbox_counts": js_checks['flexbox'],
        "spacing_counts": js_checks['spacing'],
        "font_harmony_score": font_harmony_score,
        "numerical_data": numerical_data,
        "one_liner_data": one_liner_data
    }
