import csv
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from usps import USPSApi, Address
import os
from dotenv import load_dotenv

load_dotenv()
USPS_USER_ID = os.getenv("USPS_USER_ID")  # Make sure to set this in your .env file
RETURN_ADDRESS_STREET = os.getenv("RETURN_ADDRESS_STREET")
RETURN_ADDRESS_CITY_STATE_ZIP = os.getenv("RETURN_ADDRESS_CITY_STATE_ZIP")

def verify_address_with_usps(address_dict):
    address = Address(
        name=f"{address_dict['FirstName']} {address_dict['LastName']}",
        address_1=address_dict['Address1'],
        address_2=address_dict['Address2'],
        city=address_dict['City'],
        state=address_dict['State'],
        zipcode=address_dict['PostalCode'][:5]
    )
    usps = USPSApi(USPS_USER_ID, test=False)
    try:
        response = usps.validate_address(address)
        return not response.result.get("Error")
    except Exception as e:
        print(f"[⚠️] USPS address verification failed: {e}")
        return False

# Define #10 envelope size: 9.5" x 4.125"
envelope_width = 9.5 * inch
envelope_height = 4.125 * inch

RETURN_ADDRESS_LINES = [
    USPS_USER_ID,
    RETURN_ADDRESS_STREET,
    RETURN_ADDRESS_CITY_STATE_ZIP
]

RETURN_ADDRESS_FONT = "Trebuchet MS"
RETURN_ADDRESS_SIZE = 14
RETURN_ADDRESS_LINE_HEIGHT = 14
RETURN_ADDRESS_X = 10  # points from left edge
RETURN_ADDRESS_Y_START = 270  # points from top (297 - 275 = 22 pts margin)

# Optional image next to return address
LOGO_PATH = "evil-wizard-logo.png"  # replace with your image path
LOGO_SIZE = 32  # height in points; image will scale to match this

def draw_envelope(c, first_name, last_name, address1, address2, city, state, postal_code):
    line_height = 14
    font_name = "Helvetica"
    font_size = 16

    # Return address
    c.setFont(RETURN_ADDRESS_FONT, RETURN_ADDRESS_SIZE)

    for i, line in enumerate(RETURN_ADDRESS_LINES):
        y = RETURN_ADDRESS_Y_START - i * RETURN_ADDRESS_LINE_HEIGHT
        c.drawString(RETURN_ADDRESS_X + LOGO_SIZE + 5, y, line)

    # Draw logo (if exists)
    try:
        logo = ImageReader(LOGO_PATH)
        # Get original image size
        img_width, img_height = logo.getSize()
        aspect_ratio = img_width / img_height

        # Scale by height only
        scaled_height = LOGO_SIZE
        scaled_width = aspect_ratio * scaled_height

        # Draw image with correct aspect ratio
        c.drawImage(logo,
                    RETURN_ADDRESS_X,
                    RETURN_ADDRESS_Y_START - scaled_height + 2,
                    width=scaled_width,
                    height=scaled_height,
                    mask='auto')
    except Exception as e:
        print(f"[⚠️] Could not load logo image: {e}")

    # Build the address lines
    c.setFont(font_name, font_size)
    address_lines = [
        f"{first_name.capitalize()} {last_name.capitalize()}",
        address1.upper(),
    ]
    if address2.strip():
        address_lines.append(address2)
    address_lines.append(f"{city.upper()} {state.upper()} {postal_code}")

    # Calculate total height of text block
    total_height = len(address_lines) * line_height

    # Calculate the width of the widest line
    max_line_width = max(c.stringWidth(line, font_name, font_size) for line in address_lines)

    # Set top-left starting point for the block so it’s centered as a block
    x_left = (envelope_width - max_line_width) / 2
    y_start = (envelope_height + total_height) / 2

    # Draw left-aligned lines starting from (x_left, y_start)
    for i, line in enumerate(address_lines):
        y = y_start - i * line_height
        c.drawString(x_left, y, line)


def generate_envelopes(csv_file_path, output_pdf_path='/Users/joelwilliams/Documents/envelopes.pdf'):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        c = canvas.Canvas(output_pdf_path, pagesize=(envelope_width, envelope_height))

        for row in reader:
            draw_envelope(
                c,
                first_name=row['FirstName'],
                last_name=row['LastName'],
                address1=row['Address1'],
                address2=row['Address2'],
                city=row['City'],
                state=row['State'],
                postal_code=row['PostalCode'],
            )
            c.showPage()

        c.save()
        print(f"✅ Envelopes saved to {output_pdf_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_envelopes.py input.csv")
    else:
        generate_envelopes(sys.argv[1])
