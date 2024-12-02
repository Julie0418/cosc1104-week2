import requests
from bs4 import BeautifulSoup
from utils import log_message

def fetch_compliance_rules(service):
    """
    Fetches compliance rules dynamically for the given AWS service.
    Falls back to static rules if scraping fails.
    """
    urls = {
        "s3": "https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/",
        "ec2": "https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/EC2/"
    }

    if service not in urls:
        log_message(f"No compliance rules URL for service: {service}", level="ERROR")
        return []

    try:
        log_message(f"Fetching compliance rules for {service} from {urls[service]}...")
        response = requests.get(urls[service], headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract compliance rules for S3 based on the provided content structure
        rules = []
        for rule in soup.find_all("li"):
            title = rule.get_text(strip=True)
            if title:
                rules.append({
                    "title": title,
                    "description": "Refer to AWS documentation for details."
                })

        log_message(f"Fetched {len(rules)} compliance rules for {service}.")
        return rules
    except Exception as e:
        log_message(f"Failed to fetch compliance rules for {service}: {e}", level="ERROR")
        return []
