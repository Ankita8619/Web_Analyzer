from colorsys import rgb_to_hsv

def hex_to_rgb(hex_color):
    if hex_color.startswith('#'):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6 and all(c in '0123456789abcdefABCDEF' for c in hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3 and all(c in '0123456789abcdefABCDEF' for c in hex_color):
            hex_color = ''.join([c*2 for c in hex_color])  # Convert 3-digit to 6-digit hex
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    elif hex_color.startswith('rgba(') and hex_color.endswith(')'):
        rgba = hex_color[5:-1].split(',')
        if len(rgba) == 4:
            try:
                return tuple(map(int, rgba[:3]))  # Ignore alpha value for contrast
            except ValueError:
                pass

def luminance(r, g, b):
    a = [v / 255.0 for v in (r, g, b)]
    a = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in a]
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]

def contrast_ratio(color1, color2):
    L1 = luminance(*color1)
    L2 = luminance(*color2)
    if L1 > L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)

from colorsys import rgb_to_hsv

def is_complementary(color1, color2):
    h1 = rgb_to_hsv(*color1)[0]
    h2 = rgb_to_hsv(*color2)[0]
    return abs(h1 - h2) > 0.5

def is_analogous(color1, color2):
    h1 = rgb_to_hsv(*color1)[0]
    h2 = rgb_to_hsv(*color2)[0]
    return abs(h1 - h2) < 0.1

def is_triadic(color1, color2):
    h1 = rgb_to_hsv(*color1)[0]
    h2 = rgb_to_hsv(*color2)[0]
    return abs((h1 - h2) * 3) % 1 < 0.1  # Rough check for triadic harmony

def color_harmony_score(color1, color2):
    if is_complementary(color1, color2):
        return 10
    elif is_analogous(color1, color2):
        return 7
    elif is_triadic(color1, color2):
        return 5
    else:
        return 2  # Clashing colors

def color_harmony(elements_properties):
    results = {}
    body_bg_color = elements_properties.get("body", {}).get("background-color")
    body_text_color = elements_properties.get("body", {}).get("color")
    
    if body_bg_color and body_text_color:
        body_bg_rgb = hex_to_rgb(body_bg_color)
        body_text_rgb = hex_to_rgb(body_text_color)
        
        if body_bg_rgb and body_text_rgb:
            harmony_score = color_harmony_score(body_bg_rgb, body_text_rgb)
            results["body_harmony_score"] = harmony_score

    for element, properties in elements_properties.items():
        if element != "body":
            bg_color = properties.get("background-color")
            text_color = properties.get("color")
            
            if bg_color and text_color:
                bg_rgb = hex_to_rgb(bg_color)
                text_rgb = hex_to_rgb(text_color)
                
                if bg_rgb and text_rgb:
                    harmony_score = color_harmony_score(bg_rgb, text_rgb)
                    results[f"{element}_harmony_score"] = harmony_score
                
                if body_text_color and bg_color:
                    body_text_rgb = hex_to_rgb(body_text_color)
                    if body_text_rgb and bg_rgb:
                        harmony_score = color_harmony_score(body_text_rgb, bg_rgb)
                        results[f"{element}_with_body_harmony_score"] = harmony_score
                        
    return results

def color_consistency(elements_properties):
    color_usage = {}

    for element, properties in elements_properties.items():
        bg_color = properties.get("background-color")
        text_color = properties.get("color")

        if bg_color and bg_color.startswith('#'):
            color_usage.setdefault(bg_color, []).append(f"{element}_background")
        
        if text_color and text_color.startswith('#'):
            color_usage.setdefault(text_color, []).append(f"{element}_text")
    
    return color_usage

def color_grading(elements_properties):
    results = {}
    color_usage = color_consistency(elements_properties)

    body_bg_color = elements_properties.get("body", {}).get("background-color")
    body_text_color = elements_properties.get("body", {}).get("color")

    if body_bg_color and body_text_color:
        body_bg_rgb = hex_to_rgb(body_bg_color)
        body_text_rgb = hex_to_rgb(body_text_color)
        if body_bg_rgb and body_text_rgb:
            results["body_contrast"] = contrast_ratio(body_bg_rgb, body_text_rgb)
            results["body_harmony_score"] = color_harmony_score(body_bg_rgb, body_text_rgb)

    # Check other visual elements
    for element, properties in elements_properties.items():
        if element != "body":
            bg_color = properties.get("background-color")
            text_color = properties.get("color")

            if bg_color and text_color:
                bg_rgb = hex_to_rgb(bg_color)
                text_rgb = hex_to_rgb(text_color)
                if bg_rgb and text_rgb:
                    results[f"{element}_contrast"] = contrast_ratio(bg_rgb, text_rgb)
                    results[f"{element}_harmony_score"] = color_harmony_score(bg_rgb, text_rgb)

            if body_text_color and bg_color:
                body_text_rgb = hex_to_rgb(body_text_color)
                if body_text_rgb and bg_rgb:
                    results[f"{element}_with_body_contrast"] = contrast_ratio(body_text_rgb, bg_rgb)
                    results[f"{element}_with_body_harmony_score"] = color_harmony_score(body_text_rgb, bg_rgb)

    results["color_consistency"] = color_usage
    return results

def generate_report(data, contrast_threshold=7, harmony_threshold=5):
    # Initialize counters
    total_elements = 0
    passing_elements = 0

    # Loop through the data and count elements above contrast or harmony threshold
    for key, value in data.items():
        if 'contrast' in key or 'harmony' in key:
            total_elements += 1
            element_report = {}  # To track if the element passes

            # Check if contrast and harmony are above respective thresholds
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key == 'contrast' and sub_value > contrast_threshold:
                        element_report['contrast'] = sub_value
                    elif sub_key == 'harmony' and sub_value > harmony_threshold:
                        element_report['harmony'] = sub_value
            else:
                if 'contrast' in key and value > contrast_threshold:
                    element_report['contrast'] = value
                elif 'harmony' in key and value > harmony_threshold:
                    element_report['harmony'] = value
            
            # If any threshold is passed, count it as a passing element
            if element_report:
                passing_elements += 1
    
    # Calculate the percentage of passing elements
    final_score = (passing_elements / total_elements) * 100 if total_elements > 0 else 0

    return passing_elements, total_elements, final_score

def color_grading_report(elements_properties):
    results = color_grading(elements_properties)

    # Extracting relevant data from results
    body_contrast_score = results.get("body_contrast", 0)
    body_harmony_score = results.get("body_harmony_score", 0)
    link_contrast_score = results.get("link_contrast", 0)
    link_harmony_score = results.get("link_harmony_score", 0)
    a_contrast_score = results.get("a_contrast", 0)
    a_harmony_score = results.get("a_harmony_score", 0)
    nav_contrast_score = results.get("nav_contrast", 0)
    nav_harmony_score = results.get("nav_harmony_score", 0)

    # Numerical data entries
    numerical_data = {
        "body_contrast": {"value": round(body_contrast_score, 2), "title": "Body Contrast"},
        "body_harmony_score": {"value": round(body_harmony_score, 2), "title": "Body Harmony Score"},
        "link_contrast": {"value": round(link_contrast_score, 2), "title": "Link Contrast"},
        "link_harmony_score": {"value": round(link_harmony_score, 2), "title": "Link Harmony Score"},
        "a_contrast": {"value": round(a_contrast_score, 2), "title": "Anchor Contrast"},
        "a_harmony_score": {"value": round(a_harmony_score, 2), "title": "Anchor Harmony Score"},
        "nav_contrast": {"value": round(nav_contrast_score, 2), "title": "Navigation Contrast"},
        "nav_harmony_score": {"value": round(nav_harmony_score, 2), "title": "Navigation Harmony Score"}
    }

    # One-liner data entries (Explanation of key concepts)
    one_liner_data = [
        {"title": "Contrast", "details": "Contrast ratio measures the difference in luminance between background and text colors, ensuring readability."},
        {"title": "Harmony", "details": "Color harmony score evaluates how visually pleasing color combinations are, contributing to the design’s aesthetic appeal."},
        {"title": "Color Consistency", "details": "Color consistency ensures that colors are applied uniformly across different elements, enhancing design cohesion."},
        {"title": "Body Contrast Importance", "details": "High body contrast ensures text is legible against the background, improving user experience."},
        {"title": "Average Harmony Score", "details": "A higher average harmony score suggests a more aesthetically balanced design, promoting visual appeal."},
        {"title": "Navigation Contrast", "details": "Navigation contrast helps in distinguishing navigational elements, making site structure clear and accessible."}
    ]

    # Generate the passing score based on thresholds
    passing_elements, total_elements, final_score = generate_report(results)

    # Returning final structured data with added score
    return {
        "numerical_data": numerical_data,
        "one_liner_data": one_liner_data,
        "color_usage_details": [f"Color {color} used in: {', '.join(usages)}" for color, usages in results.get("color_consistency", {}).items()],
        "total_score": round(final_score, 2),
        "score_report": {
            "passing_elements": passing_elements,
            "total_elements": total_elements,
            "total_score": round(final_score, 2)
        }
    }
