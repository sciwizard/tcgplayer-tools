# TCGPlayer Tools - Envelope Generator

This repository provides a command-line tool for generating printable PDF envelopes from a CSV file containing recipient addresses. It includes a return address block with logo support and USPS address validation.

---

## ✨ Features

- Generates standard #10 envelopes (9.5" x 4.125")
- Customizable return address with optional logo
- Left-aligned recipient address block centered on the envelope
- USPS address verification via Web Tools API (optional)
- Environment configuration via `.env`

---

## 📦 Requirements

- Python 3.7+
- Packages listed in `requirements.txt`:
  - `reportlab`
  - `usps-api`
  - `python-dotenv`

Install them with:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup

1. **Clone the repository and navigate into it**:

```bash
git clone https://github.com/your-username/tcgplayer-tools.git
cd tcgplayer-tools
```

2. **Create a `.env` file** in the root directory with your USPS Web Tools user ID:

```
USPS_USER_ID=your_usps_user_id_here
RETURN_ADDRESS_STREET="your street address"
RETURN_ADDRESS_CITY_STATE_ZIP="your return city state zip"
```

3. **Prepare a CSV file** with this format:

Go to TCGPlayer seller portal, select all orders, then click "Export Shipping". This outputs a CSV shipping info in
this format:

```csv
FirstName,LastName,Address1,Address2,City,State,PostalCode
Jane,Doe,123 Main St,,Springfield,IL,62704
John,Smith,456 Oak Ave,Apt 2B,Seattle,WA,98101
```

4. **Run the script**:

```bash
python generate_envelopes.py your_addresses.csv
```

This will create `envelopes.pdf` (default path: `~/Documents/envelopes.pdf`) with one envelope per page.

---

## 🧙‍ Return Address Customization

To customize the sender/return address and logo:

- Open `generate_envelopes.py`
- Create your own .env file like above and set your return address to match your address:

- Replace the image at `LOGO_PATH` with your own logo:

```python
LOGO_PATH = "evil-wizard-logo.png"
```

Make sure your image file is present in the working directory.

---

## 📝 Notes

- If an address fails USPS validation, it will be skipped and a warning will be printed.
- Set `test=True` when initializing the USPS API to use their sandbox:

```python
usps = USPSApi(USPS_USER_ID, test=True)
```

---

## 📂 Output

The output is a single PDF file containing one envelope per page, formatted for easy printing and envelope feeding.

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).