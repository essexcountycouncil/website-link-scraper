import pandas
import requests

urls = pandas.read_csv("output/output.csv")
urls["status"] = 0
urls["final_status"] = 0
urls["final_location"] = ""

try:
    for idx, domain in urls.to_dict(orient="index").items():
        url = domain["url"]
        print(f"Checking {url}...")

        # First don't follow redirects
        # Setting verify=False means it won't check validity of TLS certificates
        # We need this because the site doesn't have a valid TLS certificate yet
        # You should change this under most circumstances
        original_response = requests.get(
            url, allow_redirects=False, timeout=5, verify=False
        )
        # Update dataframe with the original status code
        urls.at[idx, "status"] = original_response.status_code

        # Now follow redirects
        if 300 <= original_response.status_code < 400:
            try:
                # Setting verify=False means it won't check validity of TLS certificates
                # You should change this under most circumstances
                final_response = requests.get(url, timeout=5, verify=False)
                urls.at[idx, "final_location"] = final_response.url
            # record errors with code of 0
            except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
                urls.at[idx, "final_status"] = 0
                continue

        else:
            final_response = original_response

        urls.at[idx, "final_status"] = final_response.status_code

# Export to an excel sheet if you interrupt the program
# So you don't always have to run the whole program
except KeyboardInterrupt:
    urls.to_excel("output/redirect_test_output.xlsx")

urls.to_excel("output/redirect_test_output.xlsx")
