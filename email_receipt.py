import smtplib
from email.message import EmailMessage


def build_receipt_text(transaction):
    lines = [
        "SALE RECEIPT",
        "-" * 30,
        f"Sold to                : {transaction['sold_to_name']}",
        f"Customer phone  : {transaction['sold_to_phone']}",
        f"Customer email    : {transaction.get('sold_to_email', 'N/A')}",
        f"Sold by                : {transaction['sold_by']}",
        f"Time                : {transaction['timestamp']}",
        "-" * 30,
        "ITEMS",
    ]

    total = 0.0

    for item in transaction["items"]:
        item_name = item["item"]
        price = item["price"]
        lines.append(f"{item_name:<15} ${price:.2f}")
        total += price

    lines.extend([
        "-" * 30,
        f"Total          : ${total:.2f}",
        "-" * 30,
        "Thank you for your purchase!"
    ])

    return "\n".join(lines)


def looks_like_email(email):
    return "@" in email and "." in email and " " not in email


def send_receipt_email(customer_email, transaction, sender_email, app_password):
    if not looks_like_email(customer_email):
        raise ValueError("Invalid customer email address.")

    msg = EmailMessage()
    msg["Subject"] = "Your Purchase Receipt"
    msg["From"] = sender_email
    msg["To"] = customer_email
    msg.set_content(build_receipt_text(transaction))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    return True
