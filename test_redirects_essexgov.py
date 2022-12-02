import pandas
import requests
import json

with open("output/essexgov_redirs.json") as f:
    redirects = json.load(f)

urls = pandas.DataFrame()
urls["original_url"] = ""
urls["final_status"] = 0
urls["final_location"] = ""

try:
    for idx, url in enumerate(redirects.keys()):
        url = url.replace("*", "foo").replace("http://www.essex.gov.uk", "/").replace("https://www.essex.gov.uk", "/")
        urls.at[idx, "original_url"] = url
        url = "https://portal.whitemoss-5a7067b3.uksouth.azurecontainerapps.io" + url


        print(f"Checking {url}...")

        # First don't follow redirects
        # original_response = requests.get(
        #     url, allow_redirects=False, timeout=5)
        # # Update dataframe with the original status code
        # urls.at[idx, "status"] = original_response.status_code

        # Now follow redirects
        # if 300 <= original_response.status_code < 400:
        try:
            final_response = requests.get(url, timeout=5)
            urls.at[idx, "final_location"] = final_response.url
        # record errors with code of 0
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError, requests.exceptions.ReadTimeout):
            urls.at[idx, "final_status"] = 0
            continue

        # else:
        #     final_response = original_response

        urls.at[idx, "final_status"] = final_response.status_code

# Export to an excel sheet if anything bad happens
# So you don't always have to run the whole program
except:
    urls.to_excel("output/essexgov_redirect_test_output.xlsx")

urls.to_excel("output/essexgov_redirect_test_output.xlsx")
