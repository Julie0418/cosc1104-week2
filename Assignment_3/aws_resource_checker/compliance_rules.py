import requests
from bs4 import BeautifulSoup
from utils import log_message

def fetch_compliance_rules(service):
    """
    Fetches compliance rules dynamically for the given AWS service.
    """
    urls = {
        "s3": "https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/",
        "ec2": "https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/EC2/"
    }

    if service not in urls:
        log_message(f"No compliance rules URL for service: {service}", level="ERROR")
        return []

    try:
        response = requests.get(urls[service])
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract compliance rules (example: headings and descriptions)
        rules = []
        for item in soup.find_all("div", class_="compliance-rule"):
            title = item.find("h3").get_text(strip=True)
            description = item.find("p").get_text(strip=True)
            rules.append({"title": title, "description": description})

        log_message(f"Fetched {len(rules)} compliance rules for {service}.")
        return rules
    except Exception as e:
        log_message(f"Failed to fetch compliance rules for {service}: {e}", level="ERROR")
        return []
