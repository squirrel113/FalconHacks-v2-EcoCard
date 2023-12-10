import pytesseract
from PIL import Image
from textblob import TextBlob
import re
import cv2



def receiptScanner():
    # Load the receipt image
    image_path = 'receipt.jpeg'
    img = cv2.imread(image_path)

    # Perform OCR on the receipt image
    text = pytesseract.image_to_string(img)

    # Split the OCR text into lines
    lines = text.split('\n')

    # Define a regular expression pattern to match lines with potential food item names
    item_pattern = r'\b[A-Z][A-Z0-9&\'\s]+[A-Z0-9]\b'

    # Initialize an empty array to store the extracted food items
    food_items = []

    # Define a list of patterns to exclude specific lines
    excluded_patterns = ['XXXX', 'O7511', 'CA \d', 'VISA', 'AUTH CODE',
                        'RETURN CREDIT', 'PROMOTIONAL DISCOUNT', 'NOTICE', 'CUENTENOS EN ESPANOL']

    # Iterate through each line and check for potential food items using the pattern
    for line in lines:
        match = re.search(item_pattern, line)
        if match:
            food_item = match.group().strip()
            food_items.append(food_item)

    # Filter out common non-food items and excluded patterns
    non_food_items = ["Transaction #", "Date:", "Cher:", "Register #",
                    "Sub Total", "Total", "Credit Card Tendered", "Card:", "Change Due"]
    food_items = [item for item in food_items if all(keyword not in item for keyword in non_food_items) and all(
        not re.search(pattern, item) for pattern in excluded_patterns)]

    subtotal_index = None
    for i, item in enumerate(food_items):
        if "SUBTOTAL" in item:
            subtotal_index = i
            break
    if subtotal_index is not None:
        food_items = food_items[:subtotal_index]

    # Correct the misspelled words in the food_items list
    corrected_food_items = []
    for item in food_items:
        corrected_item = str(TextBlob(item).correct())
        corrected_food_items.append(corrected_item)

    # Replace the original food_items list with the corrected version
    food_items = corrected_food_items

    completedString = ""

    # Print the corrected food items
    for item in food_items:
        completedString += item + "\n"
        print(item)

    return completedString

print(receiptScanner())