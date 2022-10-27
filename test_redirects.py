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
        # try:
        original_response = requests.get(
            url, allow_redirects=False, timeout=5, verify=False
        )
        print(original_response.status_code)
        urls.at[idx, "status"] = original_response.status_code

        # except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
        #     raise ConnectionError(e)
        #     urls.at[idx, "status"] = 0
        #     continue

        print("Got here!")
        # Now follow redirects
        if 300 <= original_response.status_code < 400:
            try:
                final_response = requests.get(url, timeout=5, verify=False)
                urls.at[idx, "final_location"] = final_response.url
            except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
                urls.at[idx, "final_status"] = 0
                continue

        else:
            final_response = original_response

        print(final_response.status_code)
        urls.at[idx, "final_status"] = final_response.status_code

except KeyboardInterrupt:
    urls.to_excel("output/redirect_test_output.xlsx")

urls.to_excel("output/redirect_test_output.xlsx")
